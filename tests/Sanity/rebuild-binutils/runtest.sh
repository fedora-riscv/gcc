#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Sanity/rebuild-binutils
#   Description: Rebuild binutils.
#   Author: Marek Polacek <polacek@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
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

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

# The test is expected to fail in devtoolset-* on RHEL-6 because of
# the "Unresolvable `R_X86_64_NONE` relocation" family of bugs, e.g.
#   https://bugzilla.redhat.com/show_bug.cgi?id=1545386
# They have been fixed for both the base and devtoolset binutils
# on RHEL-7 but on RHEL-6, it was just the base binutils.

GCC=${GCC:-gcc}

# Set the variabile UNDER_DTS on non-empty string, when run under devtoolset.
if $( echo `which gcc` | grep -qE '/opt/rh/' ); then
  UNDER_DTS="true"
  # Set the actual version of DTS
  DTS=`which gcc | awk 'BEGIN { FS="/" } { print $4 }'`
fi

rlJournalStart
  rlPhaseStartSetup
    rlLog "Using GCC: `rpmquery -f $(which $GCC)`"
    rlRun "rpmquery -a | grep -e yum-utils -e dnf-utils" 0 "YUM or DNF utils are installed"
    rlRun "TmpDir=\$(mktemp -d)"
    rlRun "pushd $TmpDir"

    if [ -z ${UNDER_DTS} ]; then
        rlFetchSrcForInstalled binutils || yumdownloader --source binutils
        srpm=$(find binutils*.src.rpm | tail -n1)
    else
        rlFetchSrcForInstalled $DTS-binutils || yumdownloader --source $DTS-binutils
        srpm=$(find $DTS-binutils*.src.rpm | tail -n1)
    fi
    rlRun "rpm -Uvh $srpm"
    spec_dir=$(rpm --eval=%_specdir)
    yum-builddep -y $spec_dir/binutils.spec
  rlPhaseEnd

  rlPhaseStartTest
    if [ "$(uname -i)" == "ppc64" ]; then 
      if rlIsRHEL 6; then
        target='--target=ppc64'
      else
        target='--target=ppc'
      fi
    fi
    if [ "$(uname -i)" == "i386" ]; then
      target='--target=i686'
    fi

    rlRun "setsebool allow_execmod 1"
    rlRun "CC=$GCC rpmbuild -bb $target --clean $spec_dir/binutils.spec &> BUILD_LOG" || ( echo "========== BUILD_LOG tail ==========" ; tail -n 20 BUILD_LOG )
    rlRun "setsebool allow_execmod 0"
  rlPhaseEnd

  rlPhaseStartCleanup
    rlBundleLogs "Build-log" BUILD_LOG
    rlRun "popd"
    rlRun "rm -r $TmpDir"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
