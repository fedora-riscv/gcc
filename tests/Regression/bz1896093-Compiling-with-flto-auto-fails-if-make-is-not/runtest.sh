#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Regression/bz1896093-Compiling-with-flto-auto-fails-if-make-is-not
#   Description: Test for BZ#1896093 (Compiling with -flto=auto fails if make is not)
#   Author: Alexandra Hájková <ahajkova@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2020 Red Hat, Inc.
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

PACKAGE="gcc"

rlJournalStart
    rlPhaseStartSetup
        MAKE_WAS_PRESENT=false
        rpm -q make &>/dev/null && MAKE_WAS_PRESENT=true
        rlAssertRpm $PACKAGE
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        rlRun "rpm -e --nodeps make" 0,1
    rlPhaseEnd

    rlPhaseStartTest
        echo "void main() { }" | gcc -x c -flto=auto - &> log
        rlAssertNotGrep "lto-wrapper: fatal error: execvp: No such file or directory" log
    rlPhaseEnd

    rlPhaseStartCleanup
        if $MAKE_WAS_PRESENT; then
            rpm -q make &>/dev/null || rlRun "yum -y install make"
        fi
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
