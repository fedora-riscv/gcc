#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Sanity/test-m32-m64-options
#   Description: Try -m32 and -m64 options.
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

# This is for Toolset.
#
# In this test, we try to compile and run programs using -m32 and -m64.
# We compile C, C++ and Fortran Hello World programs.  Also, there are two 
# proglets which are exercising some C++11 features.  Furthermore, we try
# -fgnu-tm,  -fopenmp options.  We also use libquadmath a little bit.
# We call a function from libgcc.  We also use the __thread keyword.
# Everything should be ok when running under e.g.:
#   scl enable devtoolset-1.0 bash
# Note, that gfortran is not a part of 1.0 release.

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGES=(gcc gcc-c++ gcc-gfortran glibc-common libgcc libgomp libgfortran glibc-devel libitm)

PACKAGES_X86_64=(libgomp libgfortran glibc-devel libgcc libitm)

# Choose the compiler.
GCC=${GCC:-gcc}
GXX=${GXX:-g++}
GFORTRAN=${GFORTRAN:-gfortran}

PACKAGE=$GCC

# Set the variabile UNDER_DTS on non-empty string, when run under devtoolset
if $( echo `which gcc` | grep -qE '/opt/rh/' ); then
  UNDER_DTS="true"
  # Set the actual version of DTS
  DTS=`which gcc | awk 'BEGIN { FS="/" } { print $4 }'`
fi

rlJournalStart
  rlPhaseStartSetup
    for p in "${PACKAGES[@]}"; do
      rpm -q "$p" || yum install -y $p
      rlAssertRpm "$p"
    done; unset p
    yum update -y libitm # this is a hack, since libitm is a troublemaker
    if [ -n "`rlGetSecondaryArch`" ]; then
      rlCheckRpm "libitm.`rlGetSecondaryArch`" || yum install -y libitm.`rlGetSecondaryArch`
      rlAssertRpm "libitm.`rlGetSecondaryArch`"
    fi

    rlCheckRpm "libstdc++-devel.`rlGetPrimaryArch`" || yum install -y libstdc++-devel.`rlGetPrimaryArch`
    rlAssertRpm "libstdc++-devel.`rlGetPrimaryArch`"
    # RHEL-8 CI debugging hack (to be removed when not needed):
    rlRun "rpmquery -l libstdc++-devel.`rlGetPrimaryArch` | grep -e bits/c++config"
    rlRun "rpmquery -l libstdc++-devel.`rlGetPrimaryArch` | grep -e iostream"

    if [ -n "`rlGetSecondaryArch`" ]; then
      rlCheckRpm "libitm.`rlGetSecondaryArch`" || yum install -y libitm.`rlGetSecondaryArch`
      rlAssertRpm "libitm.`rlGetSecondaryArch`"
    fi

    if [ ! -z ${UNDER_DTS} ]; then
      rlCheckRpm "$DTS-libstdc++-devel" || yum install -y $DTS-libstdc++-devel
      rlAssertRpm "$DTS-libstdc++-devel"
      if [ "`arch`" = 'x86_64' ]; then
        rlCheckRpm "$DTS-libquadmath-devel" || yum install -y $DTS-libquadmath-devel
        rlAssertRpm "$DTS-libquadmath-devel"
      fi
      if rlIsRHEL '<=7'; then # no libgfortran[45] on RHEL8+
        rlCheckRpm "libgfortran4" || yum install -y libgfortran4
        if [ -n "`rlGetSecondaryArch`" ]; then
          rlCheckRpm "libgfortran4.`rlGetSecondaryArch`" || yum install -y libgfortran4.`rlGetSecondaryArch`
          rlAssertRpm "libgfortran4.`rlGetSecondaryArch`"
        fi
        rlCheckRpm "libgfortran5" || yum install -y libgfortran5
        rlAssertRpm "libgfortran5" && yum -y update libgfortran5
        if [ -n "`rlGetSecondaryArch`" ]; then
          rlCheckRpm "libgfortran5.`rlGetSecondaryArch`" || yum install -y libgfortran5.`rlGetSecondaryArch`
          rlAssertRpm "libgfortran5.`rlGetSecondaryArch`"
        fi
      fi
    fi

    # Check whether on rhel6 x86_64 i686-packages are installed too.
    # On rhel5 i386-packages should be already installed.
    if [ "$(uname -i)" == "x86_64" ]; then
      for pack in "${PACKAGES_X86_64[@]}"; do
        rpm -q ${pack}.i?86 || yum install -y ${pack}.i?86
      done; unset pack

      if [ ! -z ${UNDER_DTS} ]; then
        yum install -y $DTS-libstdc++-devel.i?86
        yum install -y $DTS-libquadmath-devel.i?86
      fi
    fi

    rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
    # We need some files.
    rlRun "cp -v hello.{c,cpp,f90} tm.c quad.c thr-init-2.c \
    clear_cache.c omphello.c lambda-template.C cpp11.cpp $TmpDir"
    rlRun "pushd $TmpDir"
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

ARCH="$(uname -i)"
case "$ARCH" in
  "aarch64") export SWITCHES="-mlittle-endian" # we don't have -m64, so let's use some dummy switch that is enabled by default
    ;;
  "i386") export SWITCHES="-m32"
    ;;
  "ppc64") export SWITCHES="-m32 -m64"
    ;;
  "ppc64le") export SWITCHES="-m64"
    ;;
  "s390x") export SWITCHES="-m31 -m64"
    ;;
  "x86_64") export SWITCHES="-m32 -m64"
    ;;
esac

# Always try both -m32 and -m64.
for m in $SWITCHES; do
  rlPhaseStartTest "Compile and run [$m]"
    rlRun "$GCC $m hello.c -o hello_c"
    rlRun "./hello_c"

    rlRun "$GXX $m hello.cpp -o hello_cpp"
    rlRun "./hello_cpp"

    # Now try a few C++11 features.
    $GXX -xc++ -std=c++11 - <<< "int main(){}"
    if test $? -eq 0; then
      rlRun "$GXX $m -std=c++11 lambda-template.C -o lambda"
      rlRun "./lambda"

      rlRun "$GXX $m -std=c++11 cpp11.cpp -o cpp11"
      rlRun "./cpp11"
    fi

    rlRun "$GFORTRAN $m hello.f90 -o hello_fortran"
    rlRun "./hello_fortran"

    # TM support is GCC >=4.7 only.
    $GCC -xc -O2 -std=gnu99 -fgnu-tm - <<< "int main(){}"
    if test $? -eq 0; then
	rlRun "$GCC $m -O2 -std=gnu99 -fgnu-tm tm.c -o tm"
	rlRun "./tm"
    fi

    # Test OpenMP.
    rlRun "$GCC $m omphello.c -O2 -std=gnu99 -fopenmp -o omp"
    rlRun "./omp"

    # Test __thread.
    rlRun "$GCC $m thr-init-2.c -O2 -std=gnu99 -ftls-model=initial-exec -o thr" 
    rlRun "./thr"

    # Now test some libquadmath stuff (__float128 support).
    # libquadmath is mising on RHEL machines, usually.
    # But with DTS, this should be available.
    if [ ! -z ${UNDER_DTS} ]; then
      if [ "`arch`" = 'x86_64' ]; then
        rlRun "$GCC $m quad.c -O2 -std=gnu99 -lquadmath -o quad -lm"
        rlRun "./quad"
      else
        rlLog "quadmath test skipped (needs x86_64)"
      fi
    fi

    # And now something from libgcc, e.g. __builtin___clear_cache.
    rlRun "$GCC $m clear_cache.c -O2 -std=gnu99 -o cache"
    rlRun "./cache"
  rlPhaseEnd
done; unset m

  rlPhaseStartCleanup
    rlRun "popd"
    rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
