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

PACKAGES=(gcc libgcj-src)

rlJournalStart
    rlPhaseStartSetup
        for p in "${PACKAGES[@]}"; do
            rlAssertRpm "$p"
        done; unset p
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

srclist="/usr/share/java/src-*"
for src in ${srclist}; do

    rlPhaseStartTest "Try to unzip src file"
        rm -rf tmp/; mkdir tmp/
        rlRun "cp -fv ${src} tmp/" 0 "[${src}]: Copy the zip file to tmp/"
        cd tmp/
        rlRun "unzip ${src}" 0 "[${src}] Verify that is possible to unzip ${src}"
        cd ..
    rlPhaseEnd

done

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
