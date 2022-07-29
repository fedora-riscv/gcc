#!/bin/bash
# vim: dict=/usr/share/rhts-library/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Regression/gcc/515799-RHEL5-gcc-if-more-than-one-fno-builtin
#   Description: Test for bz515799 ([RHEL5] gcc: if more than one -fno-builtin-*)
#   Author: Jeffrey Bastian <jbastian@redhat.com>
#           Marek Polacek <polacek@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2009, 2012 Red Hat, Inc. All rights reserved.
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

# Include rhts environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGES=(gcc)

GCC=${GCC:-gcc}

rlJournalStart
    rlPhaseStartSetup
        for p in "${PACKAGES[@]}"; do
            rlAssertRpm "$p"
        done; unset p
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "cp -v builtin.c $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest 
        rlRun "$GCC -fno-builtin-isascii -fno-builtin-isalnum -o builtin builtin.c"
        rlAssertExists "builtin"
        rlRun "./builtin"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
