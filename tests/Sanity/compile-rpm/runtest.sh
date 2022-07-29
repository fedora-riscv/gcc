#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/gcc/Sanity/compile-rpm
#   Description: Compile a Red Hat RPM package.
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

GCC=${GCC:-gcc}

# Set the variabile UNDER_DTS on non-empty string, when run under devtoolset.
if $( echo `which gcc` | grep -qE '/opt/rh/' ); then
  UNDER_DTS="true"
  # Set the actual version of DTS
  DTS=`which gcc | awk 'BEGIN { FS="/" } { print $4 }'`
fi

rlJournalStart
  rlPhaseStartSetup
    # Work around troubles with buildroot packages being out-of-sync
    if rlIsRHEL; then
      rlMountRedhat
      for i in libipt source-highlight libbabeltrace; do
        rpm -q $i &>/dev/null || rlRun "yum -y install $i" 0-255
        rpm -q ${i}-devel &>/dev/null || rlRun "yum -y install ${i}-devel" 0-255
        d=/mnt/redhat/brewroot/packages/$i
        if rpm -q $i &>/dev/null && ! rpm -q ${i}-devel &>/dev/null; then
          if [[ -e /mnt/redhat/brewroot/packages/$i ]]; then
            d=/mnt/redhat/brewroot/packages/$i
          else
            d=/mnt/redhat/brewroot/packages/${i#lib}
          fi
          rlRun "yum -y install $d/$(rpm -q --qf='%{VERSION}/%{RELEASE}/%{ARCH}' $i)/${i}-devel-$(rpm -q --qf='%{VERSION}-%{RELEASE}.%{ARCH}' $i).rpm"
        fi
      done
    fi

    rlRun "TmpDir=\$(mktemp -d)"
    rlRun "pushd $TmpDir"

    if [ -z ${UNDER_DTS} ]; then
      rlFetchSrcForInstalled gdb || yumdownloader --source gdb
    else
      rlFetchSrcForInstalled $DTS-gdb || yumdownloader --source $DTS-gdb
    fi

    if [ -z  ${UNDER_DTS} ]; then
      srpm=$(rpmquery gdb --queryformat=%{NAME}-%{VERSION}-%{RELEASE})".src.rpm"
    else
      srpm=$(rpmquery $DTS-gdb --queryformat=%{NAME}-%{VERSION}-%{RELEASE})".src.rpm"
    fi
    rlRun "rpm -Uvh $srpm"
    spec_dir=$(rpm --eval=%_specdir)
    build_dir=$(rpm --eval=%_builddir)

    if [ -z  ${UNDER_DTS} ]; then
      pkg_dir=$(rpmquery gdb} --queryformat=%{NAME}-%{VERSION})
    else
      pkg_dir=$(rpmquery $DTS-gdb} --queryformat=%{NAME}-%{VERSION})
    fi

    yum-builddep -y $spec_dir/gdb.spec
  rlPhaseEnd

  rlPhaseStartTest
    rlRun "CC=$GCC rpmbuild -bb $spec_dir/gdb.spec &> BUILD_LOG"
    test $? -eq 0 || tail -n 20 BUILD_LOG
  rlPhaseEnd

  rlPhaseStartCleanup
    rlBundleLogs "Build-log" BUILD_LOG
    rlRun "popd"
    rlRun "rm -r $TmpDir"
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
