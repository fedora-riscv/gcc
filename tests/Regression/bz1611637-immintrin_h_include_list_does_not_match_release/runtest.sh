#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Regression/bz1611637-immintrin_h_include_list_does_not_match_release
#   Description: Test for BZ#1611637 (devtoolset-8-gcc includes avx512vbmi2intrin.h but)
#   Author: Michael Petlan <mpetlan@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2018 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

GCC=${GCC:-gcc}

rlJournalStart
    rlPhaseStartSetup
        cat > a.c <<EOF
#include <immintrin.h>
int main(void)
{
  return 0;
}
EOF
        rlAssertExists "a.c"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "$GCC -o a a.c"
        rlAssertExists "a"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "rm -f a a.c"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
