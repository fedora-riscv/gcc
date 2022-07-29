#!/bin/bash
# vim: dict=/usr/share/rhts-library/dictionary.vim cpt=.,w,b,u,t,i,k
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
#
# g++ - check for unused parameter warning
# expected exit code is 0
#
# Author: Sachin Prabhu <sprabhu@redhat.com>
# Maintainer: Marek Polacek <polacek@redhat.com>


# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGES=(gcc gcc-c++ grep)

GXX=${GXX:-g++}

rlJournalStart
    rlPhaseStartSetup
        for p in "${PACKAGES[@]}"; do
            rlAssertRpm "$p"
        done; unset p
        rlLog "GXX = $GXX"
        rlLog "Installed within `rpmquery -f $(which $GXX)`"
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "cp -v test.cpp $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "$GXX -W -Wall -o test.bin test.cpp &> output"
        cat output
        rlRun "grep -E 'warning:\W+unused\W+parameter' -q output" 1 "'warning: unused parameter' not present"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
