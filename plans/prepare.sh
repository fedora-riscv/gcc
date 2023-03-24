#!/bin/bash

#
# Setup task for Fedora CI system.  Install the x86_64 GCC build under test
# along with its respective i686 (compat arch) bits needed for the testing.
# KOJI_TASK_ID per https://github.com/fedora-ci/dist-git-pipeline/pull/50 .
#

set -x

true "V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V-V"

echo "KOJI_TASK_ID=$KOJI_TASK_ID"

. /etc/os-release

if [ "$ID" == "fedora" ] && [ "$(arch)" == "x86_64" ]; then

    if [ -z "${KOJI_TASK_ID}" ]; then
        echo "Missing koji task ID, skipping ..."
        exit 0
    fi

    tmpd=`mktemp -d`
    pushd $tmpd
        koji download-task $KOJI_TASK_ID --noprogress --arch=src
        ls
        VR=$(rpm -qp gcc* --queryformat='%{version}-%{release}')
    popd
    rm -rf $tmpd

    tmpd=`mktemp -d`
    pushd $tmpd
        koji download-task $KOJI_TASK_ID --noprogress --arch=x86_64 --arch=noarch
        rm -f *debuginfo*
        ls
        dnf -y install *.rpm
    popd
    rm -rf $tmpd

    tmpd=`mktemp -d`
    pushd $tmpd
        koji download-task $KOJI_TASK_ID --noprogress --arch=i686
        rm -f *debuginfo*
        ls
        yum -y install libgcc-$VR* libgfortran-$VR* libgomp-$VR* libitm-$VR* \
                       libstdc++-devel-$VR* libstdc++-$VR* libstdc++-static-$VR*
    popd
    rm -rf $tmpd
else
    echo "Not Fedora x86_64, skipping..."
fi

true "^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^"
