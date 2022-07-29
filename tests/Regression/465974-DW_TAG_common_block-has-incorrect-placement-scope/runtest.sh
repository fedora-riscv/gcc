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
#         Marek Polacek <polacek@redhat.com>

# Include rhts environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGES=(gcc gcc-gfortran) 

GFORTRAN=${GFORTRAN:-gfortran}

rlJournalStart
    rlPhaseStartSetup
        if type gcc | grep -q -v toolset; then
            # assert only of not devtoolset/gcc-toolset
            for p in "${PACKAGES[@]}"; do
                rlAssertRpm "$p"
            done; unset p
        fi
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "cp -v abc.f90 $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest "Testing the executable via readelf -w"
        # Compile
        rlRun "$GFORTRAN -g -o abc abc.f90" 0 "Compiling the test case: abc.f90"
        rlRun "./abc" 0 "Checking whether we have an working executable"
        rlWatchdog "readelf -w abc 2>&1 | tee gcc-readelf.log" 10
        rlAssert0 "Checking if 'readelf' ends itself" $?
        # Test
        cb=$(grep Abbrev gcc-readelf.log | grep DW_TAG_common_block -c)
        rlRun "if [ ${cb} -eq 3 ]; then true; else false; fi" 0 "Expected amount of common blocks is 3; got ${cb}"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
