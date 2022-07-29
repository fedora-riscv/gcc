#!/bin/bash

#   Copyright (c) 2010 Red Hat, Inc. All rights reserved.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of
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

# Include rhts environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="gcc"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        kernel_uname="$(uname -a | awk '{ print $3 }')"
        kernel_arch="$(uname -a | awk '{ print $12 }')"
        echo kernel_arch: $kernel_arch
        kernel_version="$(echo ${kernel_uname} | sed 's/-/ /' | awk '{ print $1 }')"
        echo kernel_version: $kernel_version
        kernel_release="$(echo ${kernel_uname} | sed 's/-/ /' | awk '{ print $2 }' | sed 's/\./ /g' | awk '{ print $1,".",$2 }' | sed 's/ //g')"
        echo kernel_release_1: $kernel_release
        if $(echo ${kernel_release} | grep -iq PAE); then
            kernel_release="$(echo ${kernel_release} | sed 's/PAE//g' | sed 's/pae//g')"
            PAE="PAE-"
        fi
        echo kernel_release_2: $kernel_release
        if rlIsRHEL 6; then
                arch="${kernel_arch}-"
        fi
        kernel_debug="http://download.devel.redhat.com/brewroot/packages/kernel/${kernel_version}/${kernel_release}/${kernel_arch}/kernel-${PAE}debuginfo-${kernel_version}-${kernel_release}.${kernel_arch}.rpm"
        kernel_debug_common="http://download.devel.redhat.com/brewroot/packages/kernel/${kernel_version}/${kernel_release}/${kernel_arch}/kernel-debuginfo-common-${arch}${kernel_version}-${kernel_release}.${kernel_arch}.rpm"
        echo ">>> $kernel_debug $kernel_debug_common"
        debuginfo-install -y kernel
        rpmquery kernel-debuginfo || rpm -ivh ${kernel_debug} ${kernel_debug_common}
    rlPhaseEnd

    rlPhaseStartTest opt-O$opt
        rlRun "stap -vvvv -p2 -e 'probe kernel.function(\"sig_ignored\") {println($$parms)}' 2>&1 | grep 'variable location problem'" 1 "gcc produced good enough debuginfo w/o 'variable location problem'"
    rlPhaseEnd

    rlPhaseStartCleanup
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
