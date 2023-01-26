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

# In this test, we try to compile and run programs using -m32 and -m64.
# We compile C, C++ and Fortran Hello World programs.  Also, there are two 
# proglets which are exercising some C++11 features.  Furthermore, we try
# -fgnu-tm,  -fopenmp options.  We also use libquadmath a little bit.
# We call a function from libgcc.  We also use the __thread keyword.

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

GCC=${GCC:-$(type -P gcc)}
GCC_RPM_NAME=$(rpm --qf '%{name}' -qf $GCC)

[[ "$GCC_RPM_NAME" == *toolset* ]] && TOOLSET=${GCC_RPM_NAME%-gcc} || TOOLSET=''

if [ -n "`rlGetPrimaryArch`" ]; then
    PRI_ARCH=$(rlGetPrimaryArch)
else
    PRI_ARCH="$(uname -i)"
fi

# State applicable -m<bits> switches
SWITCHES='-m64 -m32'
case "$PRI_ARCH" in
    i686)
        SWITCHES=-m32 # just base RHEL-6/i386
        ;;
    ppc64le) # we never had 32 support there
        SWITCHES=-m64
        ;;
    aarch64)
        # Not only we never had 32-bit support there, GCC on this architecture
        # doesn't accept the -m64 switch either. This test isn't applicable
        # at all and should be excluded by its relevancy, e.g. in TCMS:
        #   arch = aarch64: False
        exit 1
        ;;
    ppc64|s390x) # 32-bit support present only in system GCC of RHEL <8
        if [[ -z "$TOOLSET" ]] && rlIsRHEL '<8'; then
            if [[ "$PRI_ARCH" != s390x ]]; then
                SWITCHES='-m64 -m32'
            else
                SWITCHES='-m64 -m31'
            fi
        else
            SWITCHES=-m64
        fi
        ;;
esac

rlJournalStart
    rlPhaseStartSetup
        rlLogInfo "COLLECTIONS=$COLLECTIONS"
        rlLogInfo "GCC=$GCC"
        rlLogInfo "SKIP_COLLECTION_METAPACKAGE_CHECK=$SKIP_COLLECTION_METAPACKAGE_CHECK"

        # We optionally need to skip checking for the presence of the metapackage
        # because that would pull in all the dependent toolset subrpms.  We do not
        # always want that, especially in CI.
        _COLLECTIONS="$COLLECTIONS"
        if ! test -z $SKIP_COLLECTION_METAPACKAGE_CHECK; then
            for c in $SKIP_COLLECTION_METAPACKAGE_CHECK; do
                rlLogInfo "ignoring metapackage check for collection $c"
                export COLLECTIONS=$(shopt -s extglob && echo ${COLLECTIONS//$c/})
            done
        fi
        rlLogInfo "(without skipped) COLLECTIONS=$COLLECTIONS"
        export COLLECTIONS="$_COLLECTIONS"

        rlRun "TmpDir=\$(mktemp -d)"
        rlRun "cp -v hello.{c,cpp,f90} tm.c quad.c thr-init-2.c clear_cache.c omphello.c lambda-template.C cpp11.cpp $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartSetup "Showing compiler versions"
        for compiler in gcc g++ gfortran; do
            rlLogInfo "Version of compiler: $compiler"
            eval "$compiler --version 2>&1" | while read line; do
                rlLogInfo "  $line"
            done
        done
    rlPhaseEnd

    for m in $SWITCHES; do
        rlPhaseStartTest "Compile and run [$m]"

            # Test C
            rlRun "gcc $m hello.c -o hello_c"
            rlRun ./hello_c

            # Test C++
            rlRun "g++ $m hello.cpp -o hello_cpp"
            rlRun ./hello_cpp

            # C++11 features. Not available in system GCC of RHEL-6
            if ! rlIsRHEL 6 || [[ -n "$TOOLSET" ]]; then
                rlRun "g++ $m -std=c++11 lambda-template.C -o lambda"
                rlRun ./lambda

                rlRun "g++ $m -std=c++11 cpp11.cpp -o cpp11"
                rlRun ./cpp11
            fi

            # Test Fortran
            rlRun "gfortran $m hello.f90 -o hello_fortran"
            rlRun "./hello_fortran"

            # Test TM. Not available in system GCC of RHEL-6
            if ! rlIsRHEL 6 || [[ -n "$TOOLSET" ]]; then
                rlRun "gcc $m -O2 -std=gnu99 -fgnu-tm tm.c -o tm"
                rlRun ./tm
            fi

            # Test OpenMP
            rlRun "gcc $m omphello.c -O2 -std=gnu99 -fopenmp -o omp"
            rlRun ./omp

            # Test __thread
            rlRun "gcc $m thr-init-2.c -O2 -std=gnu99 -ftls-model=initial-exec -o thr"
            rlRun ./thr

            # Now test some libquadmath stuff (__float128 support).
            if rpm -q ${GCC_RPM_NAME%%gcc}libquadmath-devel &>/dev/null; then
                rlRun "gcc $m quad.c -O2 -std=gnu99 -lquadmath -o quad -lm"
                rlRun ./quad
            fi

            # And now something from libgcc, e.g. __builtin___clear_cache.
            rlRun "gcc $m clear_cache.c -O2 -std=gnu99 -o cache"
            rlRun ./cache

        rlPhaseEnd
    done

    rlPhaseStartCleanup
        rlRun popd
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
