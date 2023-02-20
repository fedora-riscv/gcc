#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Sanity/smoke-test
#   Description: Basic smoke test.
#   Author: Marek Polacek <polacek@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# A testing change.

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGES=(gcc gcc-c++ gcc-gfortran glibc-common libgomp libgcc glibc-devel libstdc++ libstdc++-devel)

# Choose the compiler.
GCC=${GCC:-gcc}
GXX=${GXX:-g++}
GFORTRAN=${GFORTRAN:-gfortran}

PACKAGE=gcc

rlJournalStart
  rlPhaseStartSetup
    export PRI_ARCH=`rlGetPrimaryArch`
    export SEC_ARCH=`rlGetSecondaryArch`
    # don't assert anything under devtoolset
    if type gcc | grep -q -v devtoolset
    then
      for p in "${PACKAGES[@]}"; do
        rpm -q "$p.$PRI_ARCH" || yum install -y "$p.$PRI_ARCH"
        rlAssertRpm "$p.$PRI_ARCH"
      done; unset p
    fi
    rlLog "GCC = $GCC"
    rlLog "Installed within `rpmquery -f $(which $GCC)`"
    rlLog "GXX = $GXX"
    rlLog "Installed within `rpmquery -f $(which $GXX)`"
    rlLog "GFORTRAN = $GFORTRAN"
    rlLog "Installed within `rpmquery -f $(which $GFORTRAN)`"
    rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
    # We need some files.
    rlRun "cp -v hello.{c,cpp,f90} tm.c quad.c thr-init-2.c clear_cache.c omphello.c $TmpDir"
    rlRun "pushd $TmpDir"
    rlRun "rpmquery -l libstdc++-devel.$PRI_ARCH"
    test -n "$SEC_ARCH" && rpmquery "libstdc++-devel.$SEC_ARCH" && rlRun "rpmquery -l libstdc++-devel.$SEC_ARCH"
  rlPhaseEnd

  rlPhaseStartSetup "Showing compiler versions"
    for compiler in $GCC $GXX $GFORTRAN
    do
      rlLog "Version of compiler: $compiler"
      eval "$compiler --version 2>&1" | while read line
      do
        rlLog "  $line"
      done
    done
  rlPhaseEnd

  rlPhaseStartTest "Compile"
    rlRun "$GCC hello.c -o hello_c"
    rlRun "$GXX hello.cpp -o hello_cpp"
    rlRun "$GFORTRAN hello.f90 -o hello_fortran"

    # TM support is GCC >=4.7 only.
    $GCC -xc -O2 -std=gnu99 -fgnu-tm - <<< "int main(){}"
    if test $? -eq 0; then
      rlRun "$GCC -O2 -std=gnu99 -fgnu-tm tm.c -o tm"
      rlRun "./tm"
    fi

    # Test OpenMP.
    rlRun "$GCC omphello.c -O2 -std=gnu99 -fopenmp -o omp"
    rlRun "./omp"

    # Test __thread.
    rlRun "$GCC thr-init-2.c -O2 -std=gnu99 -ftls-model=initial-exec -o thr" 
    rlRun "./thr"

    # Now test some libquadmath stuff (__float128 support).
    # libquadmath is mising on RHEL machines, usually.
    test "`rpmquery --qf '%{version}-%{release}' libquadmath`" = "`rpmquery --qf '%{version}-%{release}' $GCC`"
    if test $? -eq 0 -a "$GCC" = "gcc"; then
      rlRun "$GCC quad.c -O2 -std=gnu99 -lquadmath -lm -o quad"
      rlRun "./quad"
    fi

    # And now something from libgcc, e.g. __builtin___clear_cache.
    # But not on RHEL5.
    if ! rlIsRHEL 5; then
      rlRun "$GCC clear_cache.c -O2 -std=gnu99 -o cache"
	  rlRun "./cache"
    fi
  rlPhaseEnd

  rlPhaseStartTest "Check dependant libraries"
    rlRun "ldd hello_{c,cpp,fortran} &> ldd.out"
    # Nothing should be linked against anything in /opt.
    rlAssertNotGrep "/opt" ldd.out
  rlPhaseEnd

  rlPhaseStartCleanup
    rlRun "popd"
    rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
