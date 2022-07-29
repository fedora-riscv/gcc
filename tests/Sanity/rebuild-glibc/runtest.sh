#!/bin/bash

# Copyright (c) 2009, 2012 Red Hat, Inc. All rights reserved.
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
# Rewrite: Marek Polacek <polacek@redhat.com>

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

cpu_good_for_make_check () {
    # glibc can create several alternative CPU-specific bits that are selected
    # in runtime. However the "make check" phase tries to test all of them and
    # fails when testing a more "advanced" binary than the SUT's CPU. In such
    # case we'd want to skip "make check" to prevent "rpmbuild" from a certain
    # failure.
    if rlIsRHEL '>=8' && [[ $(arch) = ppc64le ]] && grep -q 'POWER[2-8]' /proc/cpuinfo; then
        rlLogInfo 'RHEL8+ on <POWER9, make check will be skipped'
        return 1
    fi
    return 0
}

GCC=${GCC:-gcc}

rlJournalStart
  rlPhaseStartSetup

    cpu_good_for_make_check && CHECK_PARAM='' || CHECK_PARAM='--nocheck'

    rlRun "rpmquery -a | grep -e yum-utils -e dnf-utils" 0 "YUM or DNF utils are installed"

    rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
    rlRun "pushd $TmpDir"

    rlLogInfo "Running kernel: `uname -r`"
    rlLogInfo "Installed kernel(s): `rpm -q kernel`"
    rlLogInfo "Installed headers: `rpm -q kernel-headers`"

    rlFetchSrcForInstalled glibc || yumdownloader --source glibc
    srpm=$(find glibc*.src.rpm | tail -n1)
    rlRun "rpm -Uvh $srpm"
    spec_dir=$(rpm --eval=%_specdir)
    yum-builddep -y $spec_dir/glibc.spec

  rlPhaseEnd

  rlPhaseStartTest
    if [ "$(uname -i)" == "ppc64" ]; then 
        if rlIsRHEL 7 || rlIsRHEL 6; then
            target='--target=ppc64'
        else
            target='--target=ppc'
        fi
    fi
    rlRun "CC=$GCC rpmbuild -bb $target $CHECK_PARAM --clean $spec_dir/glibc.spec &> BUILD_LOG"
    test $? -eq 0 || tail -n 20 BUILD_LOG
  rlPhaseEnd

  rlPhaseStartCleanup
    rlBundleLogs "Build-log" BUILD_LOG
    rlRun "popd"
    rlRun "rm -r $TmpDir"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
