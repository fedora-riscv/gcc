#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Sanity/libitm-smoke
#   Description: Just runs prebuilt binaries
#   Author: Michael Petlan <mpetlan@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2016 Red Hat, Inc.
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

# Relevant for any system with libitm binary compatible with the attached
# binaries.
# Suggested TCMS relevancy:
#   distro = rhel-6 && arch = s390x: False

PACKAGE="gcc"
REALLY_WANT_TO_RUN="true"

rlJournalStart
	rlPhaseStartSetup
		rlAssertRpm $PACKAGE
		if [ "$BASEOS_CI" = "true" ]; then
			# in CI, we need to be able to skip this testcase
			# in case libitm is not a part of gcc-libraries
			rlCheckRpm "libitm" || REALLY_WANT_TO_RUN="false"
		else
			rlCheckRpm "libitm" || rlRun "yum install -y libitm" 0 "Installing missing libitm"
			rlAssertRpm "libitm"
		fi
		TARBALL="bins_`arch`.tar.gz"
		if [ ! -f $TARBALL ]; then
			rlDie "We do not have binaries for your arch (`arch`)"
		fi
		rlRun "zcat $TARBALL | tar x"
		rlRun "pushd bins"
	rlPhaseEnd

	if [ "$REALLY_WANT_TO_RUN" = "true" ]; then
		rlPhaseStartTest
			for i in T_*; do
				rlRun "./$i"
			done
		rlPhaseEnd
	else
		rlPhaseStartTest
			rlPass "SKIPPING THIS TEST -- libitm is probably not shipped within current gcc-libraries"
		rlPhaseEnd
	fi

	rlPhaseStartCleanup
		rlRun "popd"
		rlRun "rm -rf bins" 0 "Removing the stuff we created"
	rlPhaseEnd
rlJournalPrintText
rlJournalEnd
