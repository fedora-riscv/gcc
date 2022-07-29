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

PACKAGES=(gcc libgcj strace gcc-java)

rlJournalStart
    rlPhaseStartSetup
        for p in "${PACKAGES[@]}"; do
            rlAssertRpm "$p"
        done; unset p
        rlRun "TmpDir=\`mktemp -d\`"
        rlRun "cp -v foo.java $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

# I weeded out the if (isRHEL 3) support.
for gj in "" "4"; do
    gcj_name="/usr/bin/gcj${gj}"
    gij_name="/usr/bin/gij${gj}"
    if [ -x ${gcj_name} ] && [ -x ${gij_name} ]; then
        gcj_basename=$(basename ${gcj_name})
        gij_basename=$(basename ${gij_name})

            rlPhaseStartTest "[${gij_basename}] Interpreting and compiling via java"
                rlRun "${gcj_name} -C foo.java" 0 "[${gcj_basename}] Creating bytecode"
                mv foo.class ~
                pushd /tmp

                echo "Dry run w/o strace"
                ${gij_basename} -cp ~/ foo

                echo "=== Dry run end ==="
                strace -f -v -s1024 ${gij_basename} -cp ~/ foo 2>&1 | tee out.${gij_basename}
                echo
                grep foolib out.${gij_basename}
                foolib_cnt="$(grep foolib out.${gij_basename} -c)"
                echo
                rlRun "if [ ${foolib_cnt} -ne 0 ]; then egrep '\"libfoolib.la|\"foolib.la' out.${gij_basename}; else echo \"Zero lines w/ foolib\"; true; fi" 1 "[${gij_basename}] Interpreting test case" # use 'true' (sic!)
                popd
                rm -f ~/foo.class
            rlPhaseEnd

    fi
done

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
