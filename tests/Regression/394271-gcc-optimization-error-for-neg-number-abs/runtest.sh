#!/bin/bash

# Copyright (c) 2008, 2012 Red Hat, Inc. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Author: Michal Nowak <mnowak@redhat.com>
#	  Marek Polacek <polacek@redhat.com>

# Include rhts environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

GCC="${GCC:-$(type -P gcc)}"
PACKAGE=$(rpm --qf '%{name}' -qf $GCC)

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "cp -v abs.c $TmpDir"
        rlRun "pushd $TmpDir"
        gcc -dumpversion | grep -q '^4\.4' && export OLDGCC="true"
    rlPhaseEnd

    rlPhaseStartTest "Testing the executable"
    OPTS="-O0 -O1 -O2 -O3 -Os -Ofast -Og"
    if [ "$OLDGCC" = "true" ]; then
        OPTS=${OPTS/ -Ofast -Og/}
    fi
    for opt in "" $OPTS; do
        rlRun "$GCC -g $opt -o abs$opt abs.c" 0 "Compiling the test case [ $opt ]"
        rlRun "./abs$opt" 0 "Checking whether we have an working executable [ $opt ]"
    done
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
