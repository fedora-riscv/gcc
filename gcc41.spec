ExclusiveArch: ppc
%define DATE 20070102
%define gcc_version 4.1.1
%define gcc_release 50.ada
%define _unpackaged_files_terminate_build 0
%define multilib_64_archs sparc64 ppc64 s390x x86_64
%define include_gappletviewer 1
%ifarch %{ix86} x86_64 ia64 ppc
%define build_ada 1
%else
%define build_ada 0
%endif
%define build_java 1
%ifarch s390x
%define multilib_32_arch s390
%endif
%ifarch sparc64
%define multilib_32_arch sparc
%endif
%ifarch ppc64
%define multilib_32_arch ppc
%endif
%ifarch x86_64
%define multilib_32_arch i386
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}
License: GPL
Group: Development/Languages
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: libgcc_post_upgrade.c
Source2: README.libgcjwebplugin.so
Source3: protoize.1
Source4: gcc-gnat-4.1.1-47.ppc.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
BuildRequires: binutils >= 2.17.50.0.2-8
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
BuildRequires: /usr/bin/fastjar
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.72
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparc ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
%ifnarch ppc
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
Requires: binutils >= 2.17.50.0.2-8
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
Obsoletes: gcc3
Obsoletes: egcs
%ifarch sparc
Obsoletes: gcc-sparc32
Obsoletes: gcc-c++-sparc32
%endif
%ifarch ppc
Obsoletes: gcc-ppc32
Obsoletes: gcc-c++-ppc32
%endif
Obsoletes: gcc-chill
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%ifarch sparc sparc64
Obsoletes: egcs64
%endif
Obsoletes: gcc34
Obsoletes: gcc35
Obsoletes: gcc4
Prereq: /sbin/install-info
AutoReq: true

Patch1: gcc41-ice-hack.patch
Patch2: gcc41-ppc64-m32-m64-multilib-only.patch
Patch3: gcc41-ia64-libunwind.patch
Patch4: gcc41-gnuc-rh-release.patch
Patch5: gcc41-java-nomulti.patch
Patch6: gcc41-ada-pr18302.patch
Patch7: gcc41-ada-tweaks.patch
Patch8: gcc41-java-slow_pthread_self.patch
Patch9: gcc41-ppc32-retaddr.patch
Patch10: gcc41-mni.patch
Patch11: gcc41-dsohandle.patch
Patch12: gcc41-rh184446.patch
Patch13: gcc41-pr20297-test.patch
Patch14: gcc41-objc-rh185398.patch
Patch15: gcc41-tests.patch
Patch16: gcc41-pr25874.patch
Patch17: gcc41-pr29241.patch
Patch18: gcc41-i386-tune-geode.patch
Patch19: gcc41-hash-style-gnu.patch
Patch20: gcc41-pr30001.patch
Patch21: gcc41-java-libdotdotlib.patch
Patch22: gcc41-pr28709.patch
Patch23: gcc41-pr28755.patch
Patch24: gcc41-pr27898.patch
Patch25: gcc41-pr27567.patch
Patch26: gcc41-pr29272.patch
Patch27: gcc41-pr29059.patch
Patch28: gcc41-strncat-chk.patch
Patch29: gcc41-pr29703.patch
Patch30: gcc41-pr29299.patch
Patch31: gcc41-libjava-anonverscript.patch
Patch32: gcc41-ppc64-libffi-unwind.patch
Patch33: gcc41-pr30113.patch
Patch34: gcc41-pr30110.patch
Patch35: gcc41-pr29166.patch
Patch36: gcc41-pr27266.patch
Patch37: gcc41-pr30143.patch
Patch38: gcc41-pr28261.patch
Patch39: gcc41-pr29054.patch
Patch40: gcc41-pr29535-test.patch
Patch41: gcc41-pr30045.patch
Patch42: gcc41-pr30286.patch
Patch43: gcc41-pr25993.patch
Patch44: gcc41-pr28217.patch
Patch45: gcc41-pr30189.patch
Patch46: gcc41-rh220627.patch
%define _gnu %{nil}
%ifarch sparc
%define gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%define gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparc ppc
%define gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.1.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.1 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Obsoletes: gcc3-c++
Obsoletes: gcc34-c++
Obsoletes: gcc35-c++
Obsoletes: gcc4-c++
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Obsoletes: libstdc++3
Obsoletes: libstdc++34
Autoreq: true

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++ = %{version}-%{release}, %{_prefix}/%{_lib}/libstdc++.so.6
Obsoletes: libstdc++3-devel
Obsoletes: libstdc++34-devel
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Obsoletes: gcc3-objc
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran 95 support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8
Prereq: /sbin/install-info
Obsoletes: gcc3-g77
Obsoletes: gcc-g77
Obsoletes: gcc4-gfortran
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran 95
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran 95 runtime
Group: System Environment/Libraries
Obsoletes: libf2c
Autoreq: true

%description -n libgfortran
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP 2.5 shared support library
Group: System Environment/Libraries

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers and static libraries for building
mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Obsoletes: gcc3-java
Obsoletes: gcc34-java
Obsoletes: gcc35-java
Obsoletes: gcc4-java
Prereq: /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Prereq: /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
BuildRequires: gtk2-devel >= 2.4.0
Requires: glib2 >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
Requires: libart_lgpl >= 2.1.0
BuildRequires: firefox-devel
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
Obsoletes: gcc-libgcj
Obsoletes: libgcj3
Obsoletes: libgcj34
Obsoletes: libgcj4
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj = %{version}-%{release}, %{_prefix}/%{_lib}/libgcj.so.7rh
Requires: zlib-devel, %{_prefix}/%{_lib}/libz.so
Requires: /bin/awk
Obsoletes: libgcj3-devel
Obsoletes: libgcj34-devel
Obsoletes: libgcj4-devel
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Obsoletes: libgcj4-src
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n cpp
Summary: The C Preprocessor.
Group: Development/Languages
Prereq: /sbin/install-info
%ifarch ia64
Obsoletes: gnupro
%endif
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}, libgnat = %{version}-%{release}
Obsoletes: gnat-devel, gcc3-gnat
Prereq: /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Obsoletes: gnat libgnat3
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch1 -p0 -b .ice-hack~
%patch2 -p0 -b .ppc64-m32-m64-multilib-only~
%patch3 -p0 -b .ia64-libunwind~
%patch4 -p0 -b .gnuc-rh-release~
%patch5 -p0 -b .java-nomulti~
%patch6 -p0 -b .ada-pr18302~
%patch7 -p0 -b .ada-tweaks~
%patch8 -p0 -b .java-slow_pthread_self~
%patch9 -p0 -b .ppc32-retaddr~
%patch10 -p0 -b .mni~
%patch11 -p0 -b .dsohandle~
%patch12 -p0 -b .rh184446~
%patch13 -p0 -E -b .pr20297-test~
%patch14 -p0 -b .objc-rh185398~
%patch15 -p0 -b .tests~
%patch16 -p0 -b .pr25874~
%patch17 -p0 -b .pr29241~
%patch18 -p0 -b .i386-tune-geode~
%patch19 -p0 -b .hash-style-gnu~
%patch20 -p0 -b .pr30001~
%patch21 -p0 -b .java-libdotdotlib~
%patch22 -p0 -b .pr28709~
%patch23 -p0 -b .pr28755~
%patch24 -p0 -b .pr27898~
%patch25 -p0 -b .pr27567~
%patch26 -p0 -b .pr29272~
%patch27 -p0 -b .pr29059~
%patch28 -p0 -b .strncat-chk~
%patch29 -p0 -b .pr29703~
%patch30 -p0 -b .pr29299~
%patch31 -p0 -b .libjava-anonverscript~
%patch32 -p0 -b .ppc64-libffi-unwind~
%patch33 -p0 -b .pr30113~
%patch34 -p0 -b .pr30110~
%patch35 -p0 -b .pr29166~
%patch36 -p0 -b .pr27266~
%patch37 -p0 -b .pr30143~
%patch38 -p0 -b .pr28261~
%patch39 -p0 -b .pr29054~
%patch40 -p0 -b .pr29535-test~
%patch41 -p0 -b .pr30045~
%patch42 -p0 -b .pr30286~
%patch43 -p0 -b .pr25993~
%patch44 -p0 -b .pr28217~
%patch45 -p0 -b .pr30189~
%patch46 -p0 -b .rh220627~

sed -i -e 's/4\.1\.2/4.1.1/' gcc/BASE-VER gcc/version.c
sed -i -e 's/" (Red Hat[^)]*)"/" (Red Hat %{version}-%{gcc_release})"/' gcc/version.c

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

%ifarch ppc
if [ -d libstdc++-v3/config/abi/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/sparc64-linux-gnu/32
fi
%endif
%ifarch ppc
tar xfz %SOURCE4
%endif

%build

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  mkdir locale
  localedef -f ISO-8859-1 -i de_DE locale/de_DE
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch sparc sparc64
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
%ifarch ppc
  CC=`pwd`/../usr/bin/gcc
  export PATH=`pwd`/../usr/bin:$PATH
  export LD_LIBRARY_PATH=`pwd`/../usr/lib
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-libgcj-multifile \
%if !%{build_ada}
	--enable-languages=c,c++,objc,obj-c++,java,fortran \
%else
	--enable-languages=c,c++,objc,obj-c++,java,fortran,ada \
%endif
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi --enable-plugin \
	--with-java-home=%{_prefix}/lib/jvm/java-1.4.2-gcj-1.4.2.0/jre \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-cpu=generic \
%endif
%ifarch s390 s390x
	--with-tune=z9-109 \
%endif
%ifnarch sparc ppc
	--host=%{gcc_target_platform}
%endif

#GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++" || :
cd gcc
mv testsuite{,.normal}
make %{?_smp_mflags} -k \
  `sed -n 's/check-ada//;s/^CHECK_TARGETS[[:blank:]]*=[[:blank:]]*//p' Makefile` \
  RUNTESTFLAGS="--target_board=unix/-fstack-protector ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++" || :
mv testsuite{,.ssp}
mv testsuite{.normal,}
cd ..
echo ====================TESTING=========================
( ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats\|ada'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
for i in `find . -name \*.log | grep -F testsuite.ssp/ | grep -v 'config.log\|acats\|ada'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ssp-`basename $i` || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}
cp -p %{SOURCE2} rpm.doc/README.libgcjwebplugin.so

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr $RPM_BUILD_ROOT

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html

cd obj-%{gcc_target_platform}

if [ ! -f /usr/lib/locale/de_DE/LC_CTYPE ]; then
  export LOCPATH=`pwd`/locale:/usr/lib/locale
fi

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=$RPM_BUILD_ROOT%{_prefix} mandir=$RPM_BUILD_ROOT%{_mandir} \
  infodir=$RPM_BUILD_ROOT%{_infodir} install
%if %{build_java}
make DESTDIR=$RPM_BUILD_ROOT -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 $RPM_BUILD_ROOT%{_infodir}/gnat*
%endif

FULLPATH=$RPM_BUILD_ROOT%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=$RPM_BUILD_ROOT%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

# fix some things
ln -sf gcc $RPM_BUILD_ROOT%{_prefix}/bin/cc
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/cpp $RPM_BUILD_ROOT/lib/cpp
ln -sf gfortran $RPM_BUILD_ROOT%{_prefix}/bin/f95
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
gzip -9 $RPM_BUILD_ROOT%{_infodir}/*.info*
ln -sf gcc $RPM_BUILD_ROOT%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > $RPM_BUILD_ROOT%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

%ifarch sparc sparc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target_platform}-gcc \
  $RPM_BUILD_ROOT%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparc ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find $RPM_BUILD_ROOT -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o libgcj-tools.a -o libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a | xargs rm -f

mv $RPM_BUILD_ROOT%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgcc_s.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 $RPM_BUILD_ROOT/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 $RPM_BUILD_ROOT/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparc ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
mv -f $RPM_BUILD_ROOT%{_prefix}/include/omp.h $FULLPATH/include/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 $RPM_BUILD_ROOT%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 $RPM_BUILD_ROOT%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
if [ "%{_lib}" != "lib" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/libgcj.pc \
    > $RPM_BUILD_ROOT%{_prefix}/%{_lib}/pkgconfig/libgcj.pc
fi
%endif

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.1 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgfortran.so.1.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../libgcj.so.7rh.* libgcj.so
ln -sf ../../../libgcj-tools.so.7rh.* libgcj-tools.so
ln -sf ../../../libgij.so.7rh.* libgij.so
%endif
%if %{build_ada}
cd adalib
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.1.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.1.so
cd ..
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.1 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.1.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.7rh.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.7rh.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.7rh.* libgij.so
%endif
%if %{build_ada}
cd adalib
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.1.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.1.so
cd ..
%endif
fi
%if %{build_java}
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libsupc++.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortranbegin.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.*a .
mv -f $RPM_BUILD_ROOT%{_prefix}/include/mf-runtime.h include/

%ifarch sparc ppc
ln -sf ../../../../../lib64/libobjc.so.1 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.* | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.1.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
ln -sf ../`echo ../../../../lib/libmudflap.so.0.* | sed s~/lib/~/lib64/~` 64/libmudflap.so
ln -sf ../`echo ../../../../lib/libmudflapth.so.0.* | sed s~/lib/~/lib64/~` 64/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.7rh.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.7rh.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.7rh.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libsupc++.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgfortran.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgfortranbegin.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libobjc.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libgomp.*a 64/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib64/libmudflap{,th}.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.1 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.1.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
ln -sf ../`echo ../../../../lib64/libmudflap.so.0.* | sed s~/../lib64/~/~` 32/libmudflap.so
ln -sf ../`echo ../../../../lib64/libmudflapth.so.0.* | sed s~/../lib64/~/~` 32/libmudflapth.so
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.7rh.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.7rh.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.7rh.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libsupc++.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgfortran.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgfortranbegin.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libobjc.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libgomp.*a 32/
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/libmudflap{,th}.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a \) -a -type f`
popd
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgfortran.so.1.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libobjc.so.1.*

%if %{build_ada}
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libgnat*so*
%endif

for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > $RPM_BUILD_ROOT%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/c?9

mkdir -p $RPM_BUILD_ROOT%{_prefix}/sbin
gcc -static -Os %{SOURCE1} -o $RPM_BUILD_ROOT%{_prefix}/sbin/libgcc_post_upgrade
strip $RPM_BUILD_ROOT%{_prefix}/sbin/libgcc_post_upgrade

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/{32,64}/libiberty.a
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libssp*

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/lib*.so*
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/lib*.a
%else
%ifarch sparc ppc
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64/lib*.so*
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64/lib*.a
%endif
%endif

%if %{build_java}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 $RPM_BUILD_ROOT%{_prefix}/share/java/gcj-endorsed \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version} \
	  $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man1/protoize.1
echo '.so man1/protoize.1' > $RPM_BUILD_ROOT%{_mandir}/man1/unprotoize.1
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man1/unprotoize.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcc.info.gz

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz
fi

%post -n cpp
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/cpp.info.gz

%preun -n cpp
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz
fi

%post gfortran
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz

%preun gfortran
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz
fi

%post java
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz

%preun java
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz
fi

%post gnat
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz

%preun gnat
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn_unw.info.gz
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p %{_prefix}/sbin/libgcc_post_upgrade

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgcj
/sbin/ldconfig
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz

%preun -n libgcj
if [ $1 = 0 ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp -p /sbin/ldconfig

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/protoize
%{_prefix}/bin/unprotoize
%ifarch sparc ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/protoize.1*
%{_mandir}/man1/unprotoize.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/SYSCALLS.c.X
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/README
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING*

%files -n cpp -f cpplib.lang
%defattr(-,root,root)
/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{_prefix}/sbin/libgcc_post_upgrade
%doc gcc/COPYING.LIB

%files c++
%defattr(-,root,root)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparc ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%ifarch sparc sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root)
%{_prefix}/%{_lib}/libstdc++.so.6*

%files -n libstdc++-devel
%defattr(-,root,root)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gj]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%endif
%ifnarch sparc sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%endif
%ifnarch sparc ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/docs/html/

%files objc
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root)
%{_prefix}/%{_lib}/libobjc.so.1*

%files gfortran
%defattr(-,root,root)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgfortran.so.1*

%if %{build_java}
%files java
%defattr(-,root,root)
%{_prefix}/bin/gcj
%{_prefix}/bin/gcjh
%{_prefix}/bin/gjnih
%{_prefix}/bin/jcf-dump
%{_prefix}/bin/jv-scan
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/gcjh.1*
%{_mandir}/man1/gjnih.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/jv-scan.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparc sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/fastjar
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gcj-dbtool
%if %{include_gappletviewer}
%{_prefix}/bin/gappletviewer
%endif
%{_prefix}/bin/gjarsigner
%{_prefix}/bin/gkeytool
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_infodir}/fastjar*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%if %{include_gappletviewer}
%{_prefix}/%{_lib}/gcj-%{version}/libgcjwebplugin.so
%endif
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^s]*
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%if %{include_gappletviewer}
%doc rpm.doc/README.libgcjwebplugin.so
%endif

%files -n libgcj-devel
%defattr(-,root,root)
%{_prefix}/bin/addr2name.awk
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparc sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/%{_lib}/pkgconfig/libgcj.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*
%endif

%files -n libgcj-src
%defattr(-,root,root)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip

%if %{build_ada}
%files gnat
%defattr(-,root,root)
%{_prefix}/bin/gnat*
%{_prefix}/bin/gpr*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so
%endif

%files -n libgomp
%defattr(-,root,root)
%{_prefix}/%{_lib}/libgomp.so.1*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap-devel
%defattr(-,root,root)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%ifarch sparc ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%changelog
* Wed Jan  3 2007 Jakub Jelinek <jakub@redhat.com> 4.1.1-50.ada
- Build with ADA on PowerPC

* Wed Jan  3 2007 Jakub Jelinek <jakub@redhat.com> 4.1.1-50
- backwards compatibility with old layout of struct _Unwind_Context
  (#220627)
- fix preprocessor defines in assembly preprocessed with -std=...
  (Steven Bosscher, PR c/25993)
- fix PCH creation with templates (Jason Merrill, PR c++/28217)
- fix dwarf2out ICE (Alexandre Oliva, #217529, PR debug/30189)

* Tue Jan  2 2007 Jakub Jelinek <jakub@redhat.com> 4.1.1-49
- update from gcc-4_1-branch (-r120062:120325)
  - PRs debug/26964, fortran/30200, libfortran/30145
- fix endless recursion in negate_expr/fold_unary (PR middle-end/30286)
- fix cpp problem on empty source files (Tom Tromey, PR preprocessor/30001)
- improve constructor disambiguation (Mark Mitchell, PR c++/28261,
  PR c++/29535)
- fix handling of non-NULL attribute on nested functions (Andrew Pinski,
  PR tree-opt/30045)
- fix ICE with friend templatized static member function (PR c++/29054)

* Wed Dec 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-48
- update from gcc-4_1-branch (-r119833:120062)
  - PRs libstdc++/11953, target/24036
- fix ia64 EH region boundaries where last br.call in the region
  is not at the end of a bundle (#219596, PR target/30230)
- fix DI resp. TImode __sync_*_compare_and_swap on i?86 resp. x86_64
  (Kazu Hirata, #220258, PR target/27266)
- fix asm vs. nested functions or OpenMP (#220250, PRs middle-end/30262,
  middle-end/30263)
- fix handling of complex shared OpenMP vars (Andrew Pinski,
  PR middle-end/30143)

* Thu Dec 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-47
- fix ia64 prologue generation (Andreas Schwab, #219594, PR target/29166)
- fix ppc64 divdi3 (PR target/30185)

* Wed Dec 13 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-46
- update from gcc-4_1-branch (-r119654:119833)
  - PRs c++/27316, c++/28740, c++/29732, fortran/29820, fortran/29821,
	fortran/29912, fortran/29916, fortran/30003, libstdc++/26497,
	libstdc++/28125, libstdc++/28265, target/30039
- fix loop unswitching (Zdenek Dvorak, #219138, PR rtl-optimization/30113)

* Fri Dec  8 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-45
- update from gcc-4_1-branch (-r119343:119654)
  - PRs c++/14329, c++/28284, c++/29632, c++/29728, c++/29729, c++/29730,
	c++/29733, c++/30022, libfortran/29810
- add protoize.1 and unprotoize.1 man pages (#188914)
- fix RTL sharing problem in combine (#218603, PR rtl-optimization/27761)
- additions to libgcj-src (Ben Konrath, PR libgcj/30110)

* Fri Dec  1 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-44
- fix OpenMP loops with 0 iterations (PR libgomp/29947)

* Thu Nov 30 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-43
- update from gcc-4_1-branch (-r119167:119343)
  - PRs c++/29022, fortran/29391, fortran/29489, fortran/29982,
	libgfortran/29936, target/29319, tree-opt/29964
- fix -fopenmp ICEs on omp constructs where the body never returns
  (PR middle-end/29965)

* Fri Nov 24 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-42
- update from gcc-4_1-branch (-r119021:119167)
  - fix s390{,x} __sync_* builtins
- fix ppc64 libffi unwind info

* Thu Nov 23 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-41
- fix ICE with -fopenmp -fexceptions on ia64 (#216988, PR c/29955)
- fix parsing of C++ if/switch/etc. conditions (PR c++/29886)

* Wed Nov 22 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-40
- disallow multiple vector_size attributes (PR c/29736)
- don't ICE on main returning int with vector_size attribute (PR c++/29735)
- hide symbols that shouldn't be exported from libgcj.so (GC_*, ffi_*,
  lt_* etc., #216120)

* Tue Nov 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-39
- update from gcc-4_1-branch (-r118891:119021)
  - PRs middle-end/26306, middle-end/29753, target/18553, target/29114,
	target/29449, tree-opt/29788, tree-optimization/28888
- fix some C++ vector conversions (PR c++/29734)
- fix C++ ICE with value dependent const brace enclosed initializer
  (PR c++/29570)

* Thu Nov 16 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-38
- update from gcc-4_1-branch (-r118805:118891)
  - PRs rtl-optimization/29797
- fix forwprop switch optimization (PR middle-end/29584)
- remove old *34* provides (#215839)

* Tue Nov 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-37
- fix up check_effective_target_fopenmp tcl test for the testsuite
  framework backport changes

* Tue Nov 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-36
- update from gcc-4_1-branch (-r118571:118805)
  - PRs c++/29106, c++/29518, fortran/24518, fortran/29216, fortran/29314,
	fortran/29371, fortran/29387, fortran/29392, fortran/29490,
	fortran/29565, fortran/29630, fortran/29679, fortran/29713,
	middle-end/21032, testsuite/28703, tree-opt/28545
- honor initial conditions and variable types in conversion to perfect
  nesting for -ftree-loop-linear optimizations (#209297,
  PR tree-optimization/29581)

* Sat Nov 11 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-35
- fix libgcj_bc.so dummy lib on i?86/x86_64/ia64/s390/s390x

* Sat Nov 11 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-34
- fix libgcj_bc.so symlink and dummy lib placement to avoid 64-bit gcc-java
  requiring 32-bit libc or vice versa
- fix ICE on Fortran !$omp continued line followed by !$ conditional
  line (PR fortran/29759)

* Wed Nov  8 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-33
- update from gcc-4_1-branch (-r118468:118571)
  - PRs fortran/24398, fortran/27701, fortran/29098, fortran/29115,
	fortran/29211, fortran/29232, fortran/29364, fortran/29373,
	fortran/29407, libfortran/29627, tree-optimization/29610
- fix java.net.SocketPermission (Gary Benson, #212739)
- fix java.util.regex.Matcher (Ito Kazumitsu, #183698, PR classpath/29703)
- fix # <linenum> <file> <flags> handling in libcpp when switching
  from system header to non-system header or main source
  (PR preprocessor/29612)
- fix gcc configury detection of ld COMDAT support
- move *.so symlinks from libgcj-devel to gcc-java (#214195)

* Sat Nov  4 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-32
- update from gcc-4_1-branch (-r118025:118468)
  - PRs bootstrap/28400, fortran/29067, libgfortran/29563, middle-end/29250,
	rtl-optimization/28970, rtl-optimization/29631, target/29377,
	tree-optimization/27891
  - fix infinite recursion in make_vector_type (#212848,
    PR tree-optimization/29637)
- merge gomp fixes from the trunk (-r118133:118134)
  - PR fortran/29629
- fix A < 0 ? <sign bit of A> : 0 optimization (#213821, PR middle-end/29695)
- fix ICE in gfc_get_derived_type (Paul Thomas, #212936, PR fortran/29641)

* Wed Oct 25 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-31
- update from gcc-4_1-branch (-r117629:118025)
  - PRs c++/20647, c++/25878, c++/26884, c++/27787, c++/28506, c++/28906,
	c++/29020, c++/29175, c++/29318, c++/29408, c++/29435, c/27184,
	c/29092, fortran/25091, fortran/25092, fortran/29284, fortran/29321,
	fortran/29322, fortran/29393, fortran/29403, gcov/profile/26570,
	inline-asm/29119, middle-end/20491, rtl-optimization/29323,
	target/25519, target/28825, target/28960, target/29300,
	testsuite/28829, tree-optimization/26969
  - fix libstdc++.so backwards compatibility with GCC 3.4.x (#210452)
- fix always_inline attribute at -O0 (Jan Hubicka, PR middle-end/29241)
- fix function local static vars with used attribute (Jan Hubicka,
  Richard Guenther, PR middle-end/29299)

* Wed Oct 11 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-30
- update from gcc-4_1-branch (-r117464:117629)
  - PRs c++/28302, c++/28349, c++/28450, c++/29002, libstdc++/29095,
	libstdc++/29354, libstdc++/29368, target/28490
- fix gnu.xml.transform.TransformerImpl (Tom Tromey, #208854,
  PR classpath/29362)

* Fri Oct  6 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-29
- update from gcc-4_1-branch (-r117266:117464)
  - PRs bootstrap/26764, bootstrap/27334, c++/29080, c++/29138, c++/29226,
	c/27489, c/27490, debug/28980, fortran/18791, libfortran/18791,
	middle-end/28862, objc/29195, other/25035, tree-opt/28952
  - fix s390{,x} address legitimization with TLS symbols (Angel Nunez
    Mencias)
- fix -fno-automatic with Fortran auto arrays with non-constant size
  (#203928, PR fortran/28415)
- fix char and short __sync_fetch_and_XXX (PR target/28924)
- fix emitting of vector constants with incomplete initializers (PR c/29091)
- fix ICE with multiple exit loop and -ftree-loop-linear
  (#208935, PR tree-optimization/29290)

* Sat Sep 30 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-28
- fix i386/x86_64 legitimize_pic_address with TLS symbols (PR target/29198)
- fix gimplification of post-increment with side-effects on the inner
  expression (PR c/29154)

* Thu Sep 28 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-27
- update from gcc-4_1-branch (-r117225:117266)
  - PR target/29230
- restrict single entry mem{{,p}cpy,move,set} optimization to vars
  and components thereof (PR middle-end/29272)
- fix java.util.Locale (Tom Tromey, #201712)

* Tue Sep 26 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-26
- update from gcc-4_1-branch (-r117162:117225)
  - PRs classpath/28661, libgcj/29178, libstdc++/29179, libstdc++/29224
  - fix unwind info generation, broken in gcc-4.1.1-21
    (Roger Sayle, PR debug/29132)

* Sat Sep 23 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-25
- update from gcc-4_1-branch (-r117069:117162)
  - PRs c++/28996, c++/29087, middle-end/26983
- fix -fprofile-use with anonymous namespaces (Jan Hubicka, PRs profile/20815,
  profile/26399)
- fix #pragma omp parallel and #pragma omp section that call nested
  functions (PRs middle-end/25261, middle-end/28790)

* Wed Sep 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-24
- update from gcc-4_1-branch (-r117000:117069)
  - PRs fortran/21918, fortran/28526, fortran/28817, fortran/29060,
	fortran/29101, java/28754, java/28892, java/29013,
	middle-end/27226, middle-end/4520, tree-optimization/28900
- fix java.utils.logging.Logger (Mark Wielaard, #207111)
- fix gnu.javax.net.ssl.provider.SSLSocket (Tom Tromey, #206904)
- add support for Fortran OpenMP conditional inclusion (PR fortran/29097)
- add some -D_FORTIFY_SOURCE compile time strncat buffer overflow checks

* Sun Sep 17 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-23
- update from gcc-4_1-branch (-r116958:117000)
  - PRs fortran/29051, target/28946
- fix single entry mem{{,p}cpy,move,set} optimization (Andrew Pinski,
  PR tree-opt/29059)

* Fri Sep 15 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-22
- update from gcc-4_1-branch (-r116778:116958)
  - PRs ada/21952, ada/29025, c++/26957, fortran/28890, fortran/28923,
	fortran/28959, libfortran/28890, libfortran/28923, libfortran/28947,
	middle-end/28493, other/23541, other/26507, rtl-optimization/28243,
	rtl-optimization/28634, rtl-optimization/28636, rtl-optimization/28726,
	target/13685, target/26504, target/27537, target/27681, target/28621,
	target/29006, testsuite/28950, testsuite/29007
- fix #pragma omp atomic (PR middle-end/28046)
- speed up dominance frontiers calculation (Jan Hubicka)
- add README.libgcjwebplugin.so to libgcj %%doc (Tom Fitzsimmons)
- fix gcc-gfortran %%doc (#206333)
- fix gcc-debuginfo (#205500)

* Fri Sep  8 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-21
- update from gcc-4_1-branch (-r116498:116778)
  - PRs c++/19809, c++/26102, c++/26195, c++/26571, c++/26670, c++/26671,
	c++/26696, c++/26917, c++/28860, c++/28878, c++/28886, fortran/20067,
	fortran/24866, fortran/25077, fortran/25102, fortran/28005,
	fortran/28873, fortran/28885, fortran/28908, libfortran/28005,
	middle-end/27724, middle-end/28814, other/22313,
	rtl-optimization/27616, rtl-optimization/28386, target/24367
- add primitive class object symbols to libgcj_bc.so (Tom Tromey,
  PR libgcj/28698)
- optimize single entry memcpy/mempcpy/memmove/memset already at the tree
  level (PR middle-end/27567)
- add dependencies to *-devel subpackages, so that e.g. ppc64
  libstdc++-devel requires 64-bit libstdc++, similarly for libgcj-devel
  and libgcj/zlib-devel

* Fri Aug 25 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-20
- update from gcc-4_1-branch (-r116389:116498)
  - PRs c++/28056, c++/28058, c++/28595, c++/28853, c/27558,
	c/27893, c/28299, c/28418, driver/27622, libfortran/28452,
	libfortran/28542, target/27075
- optimize A / (B << N) where A and B is positive and B is a power of two
  (Alan Modra, #195924, PR rtl-optimization/26026)
- fix attribute handling in C++ (Jason Merrill, #204277, #204035,
  PRs c++/28659, c++/28863)

* Fri Aug 25 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-19
- update from gcc-4_1-branch (-r116223:116389)
  - PRs c++/23372, c++/27714, c++/28346, c++/28385, fortran/18111,
	fortran/20886, fortran/25217, fortran/25828, fortran/28425,
	fortran/28496, fortran/28601, fortran/28630, fortran/28660,
	fortran/28735, fortran/28762, fortran/28771, fortran/28788,
	libstdc++/28765, target/27565
- another big Java merge from the trunk (Tom Fitzsimmons)
- fix ICE in add_reg_br_prob_note (PR middle-end/28683)

* Fri Aug 18 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-18
- update from gcc-4_1-branch (-r116176:116223)
  - PRs c++/28593, c++/28606, c++/28710, c/27697, middle-end/20256,
	middle-end/25211, middle-end/26435
- don't waste .rodata space when copying from const array with large
  entries (PR middle-end/28755)
- fix --combine with anonymous structures in unions (Alexandre Oliva,
  PR c/27898)
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Wed Aug 16 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-17
- update from gcc-4_1-branch (-r116082:116176)
  - PRs c++/27894, c++/28677, c/28649, middle-end/28075,
	rtl-optimization/23454
- merge gomp fixes from the trunk (-r116152:116154)
  - PRs middle-end/28713, middle-end/28724
- add -march=geode and -mtune=geode support (Vlad Makarov)
- use %gs rather than %fs register on x86_64 with
  -mcmodel=kernel -fstack-protector (Arjan van de Ven, #202842)
- don't create jar manifest in libgcj-tools-4.*.jar (#200887)
- externally_visible attribute fixes (Jan Hubicka, PRs c/25795, c++/27369)
- --combine fixes for aggregates with attributes (PRs c/28706, c/28712)
- further externally_visible attr fixes (PR c/28744)
- fix invalid token pasting error message (PR preprocessor/28709)
- obey OpenMP 2.5 chapter 4 env var requirements (whitespace rules
  and case insensitivity in the env vars; PR libgomp/28725)
- fix OPT_FLAGS on sparc

* Sat Aug 12 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-16
- fix multilib conflict in libgcj-tools-4.1.1.jar (#200887)

* Fri Aug 11 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-15
- update from gcc-4_1-branch (-r115877:116082)
  - PRs c++/27508, c++/28148, c++/28250, c++/28256, c++/28257, c++/28259,
	c++/28267, c++/28274, c++/28347, c++/28432, c++/28557, c++/28594,
	c++/28637, c++/28638, c++/28639, c++/28640, c++/28641, c/27721,
	c/28136, fortran/27981, fortran/28548, fortran/28590,
	middle-end/28651, rtl-optimization/27291, rtl-optimization/28221,
	target/27566, target/27827
- fix Fortran ICE with nested function (Paul Thomas, #200618,
  PR fortran/28600)

* Wed Aug  2 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-14
- update from gcc-4_1-branch (-r115644:115877)
  - PRs c++/27572, c++/27668, c++/27962, c++/28025, c++/28258, c++/28523,
	debug/25468, fortran/20892, fortran/27874, fortran/28129,
	fortran/28439, libgfortran/28335, libgfortran/28339,
	middle-end/28402, middle-end/28403, middle-end/28473,
	target/27287, target/28247, tree-optimization/26719,
	tree-optimization/27639, tree-optimization/27795,
	tree-optimization/28029, tree-optimization/28238
- BuildRequire firefox-devel instead of mozilla-devel

* Tue Jul 25 2006 Alexandre Oliva <aoliva@redhat.com> 4.1.1-13
- backport fix by Andrew Haley for build problems related with the
  bootstrap ClassLoader

* Mon Jul 24 2006 Alexandre Oliva <aoliva@redhat.com> 4.1.1-12
- backport fix by Mark Wielaard for NullPointerException in GCJ web plugin

* Fri Jul 21 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-11
- update from gcc-4_1-branch (-r115565:115644)
  - PRs target/27363, c++/27495, c++/28048, c++/28235, c++/28337, c++/28338,
	c++/28363, middle-end/28283
- turn back autoprov/autoreq on gcc-java, instead disable it on
  libgcj-devel

* Thu Jul 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-10
- Java backport of from GCC trunk (Tom Tromey, Bryce McKinlay)
  - include libgcjwebplugin.so, gappletviewer, gjarsigner, gkeytool
- C++ visibility changes (Jason Merrill, PRs c++/28407, c++/28409)

* Tue Jul 18 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-9
- update from gcc-4_1-branch (-r115330:115565)
  - PRs c++/28016, c++/28051, c++/28249, c++/28291, c++/28294, c++/28304,
	c++/28343, c/26993, c/28286, fortran/20844, fortran/20893,
	fortran/20903, fortran/25097, fortran/27980, fortran/28201,
	fortran/28353, fortran/28384, libstdc++/27878,
	tree-optimization/19505, tree-optimization/28162,
	tree-optimization/28187
- fix directory traversal issue in fastjar (Richard Guenther, CVE-2006-3619,
  PR fastjar/28359)
- fix ICE on complex assignment in nested fn (Richard Henderson,
  PR middle-end/27889)
- fix __builtin_constant_p in initializers (Mark Shinwell, #198849)
- fix tree verification - IDENTIFIER_NODE can be shared (Diego Novillo)
- fix duplicate_eh_regions
- handle > 99 tree dumps in the testsuite

* Sat Jul 15 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-8
- fix handling of C++ template static data members in anonymous namespace
  (PR c++/28370)
- fix Fortran OpenMP handling of !$omp parallel do with lastprivate on the
  iteration variable (PR fortran/28390)
- backported reassociation pass rewrite (Daniel Berlin, Jeff Law,
  Roger Sayle, Peter Bergner, PRs ada/24994, tree-optimization/26854)
- BuildReq sharutils for uuencode

* Tue Jul 11 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-7
- update from gcc-4_1-branch (-r115058:115330)
  - PRs c++/13983, c++/17519, c++/18681, c++/18698, c++/26577, c++/27019,
	c++/27424, c++/27768, c++/27820, c++/28114, fortran/23420,
	fortran/23862, fortran/24748, fortran/26801, fortran/27965,
	fortran/28081, fortran/28094, fortran/28167, fortran/28174,
	fortran/28213, fortran/28237, middle-end/27428, target/28084,
	target/28207, tree-optimization/28218
- use --hash-style=gnu by default
- C++ visibility fixes (Jason Merrill, PRs c++/17470, c++/19134,
  c++/21581, c++/21675, c++/25915, c++/26612, c++/26905, c++/26984,
  c++/27000, c++/28215, c++/28279)
- fix ppc insvdi_internal2/3 (David Edelsohn, Alan Modra, #197755,
  PR target/28170)
- avoid TFmode PRE_INC/PRE_DEC on ppc (David Edelsohn, PR target/28150)

* Thu Jun 29 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-6
- update from gcc-4_1-branch (-r114766:115058)
  - PRs c++/27821, c++/28109, c++/28110, c++/28112, fortran/16206,
	fortran/18769, fortran/19310, fortran/19904, fortran/20867,
	fortran/20874, fortran/20876, fortran/22038, fortran/25049,
	fortran/25050, fortran/25056, fortran/25073, fortran/27554,
	fortran/27715, fortran/27784, fortran/27895, fortran/27958,
	fortran/28118, fortran/28119, libfortran/27784, libfortran/27895,
	libgcj/28178, middle-end/28045, middle-end/28151, target/27082,
	target/27861, tree-optimization/27781
- fix a reload problem that lead sometimes to writes to read-only objects
  (Bernd Schmidt, #196736, PR middle-end/26991, PR rtl-optimization/25636)
- ppc -mcpu=power6 initial support (Pete Steinmetz, #195924)

* Tue Jun 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-5
- fix C++ #pragma omp atomic (Mark Mitchell)

* Mon Jun 19 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-4
- update from gcc-4_1-branch (-r114555:114766)
  - PRs bootstrap/22541, c++/21210, c++/26559, c++/27227, c++/27648,
	c++/27665, c++/27666, c++/27689, c++/27884, c++/27933, c++/27951,
	fortran/27786, java/28024, middle-end/27733, middle-end/27802,
	target/27858, tree-optimization/27830
- merge gomp changes from the trunk (-r114642:114643)
  - PR libgomp/28008
- fix -fmerge-all-constants
- fix #pragma omp critical handling if not --enable-linux-futex

* Tue Jun 13 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-3
- add BuildRequires for elfutils-devel on ia64
- fix a reload bug visible on s390x (Andreas Krebbel, #193912,
  PR middle-end/27959)

* Mon Jun 12 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-2
- update from gcc-4_1-branch (-r114107:114555)
  - PRs ada/27769, c++/20173, c++/26068, c++/26433, c++/26496, c++/27177,
	c++/27385, c++/27447, c++/27451, c++/27601, c++/27713, c++/27716,
	c++/27722, c++/27801, c++/27806, c++/27807, c++/27819, c/25161,
	c/26818, c/27020, c/27718, fortran/14067, fortran/16943,
	fortran/18003, fortran/19015, fortran/19777, fortran/20839,
	fortran/20877, fortran/23091, fortran/23151, fortran/24168,
	fortran/24558, fortran/25047, fortran/25058, fortran/25082,
	fortran/25090, fortran/25098, fortran/25147, fortran/25746,
	fortran/26551, fortran/27155, fortran/27320, fortran/27411,
	fortran/27449, fortran/27470, fortran/27524, fortran/27552,
	fortran/27584, fortran/27613, fortran/27655, fortran/27662,
	fortran/27709, fortran/27897, libgcj/26483, libgfortran/24459,
	libgfortran/27757, middle-end/27743, middle-end/27793,
	target/25758, target/26223, target/27790, target/27842,
	testsuite/27705, tree-optimization/26242, tree-optimization/26622
- merge gomp changes from the trunk (-r114518:114520 and -r114524:114525)
  - PRs preprocessor/27746, c/27747, c++/27748, fortran/27916
- don't generate decls with the same DECL_UID in C++ FE (PR middle-end/27793)

* Thu May 25 2006 Jakub Jelinek <jakub@redhat.com> 4.1.1-1
- update from gcc-4_1-branch (-r113848:114107)
  - GCC 4.1.1 release
  - PR fortran/27553
- fix i386/x86_64 -O0 -fpic link failure (#192816, PR target/27758)
- fix gcjh on 64-bit hosts (#192700)
- -fvar-tracking fixes needed for SystemTap (Alexandre Oliva, BZ#2438)

* Wed May 17 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-19
- update from gcc-4_1-branch (-r113785:113848)
  - PRs c++/26757, c++/27339, c++/27491, driver/26885, rtl-optimization/14261,
	target/26600, tree-optimization/27603
- merge gomp changes from the trunk (-r113513:113514, -r113821:113823 and
  -r113845:113846)
  - PRs middle-end/27415, middle-end/27573
- optimize handling of large CONSTRUCTORs (Bernd Schmidt,
  PR middle-end/27620)

* Mon May 15 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-18
- update from gcc-4_1-branch (-r113722:113785)
  - PRs c++/27315, c++/27581, c++/27582, rtl-optimization/22563
- merge gomp changes from the trunk (-r113786:113790)

* Sun May 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-17
- make -mtune=z9-109 the default on s390{,x} (#184630)

* Sat May 13 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-16
- update from gcc-4_1-branch (-r113637:113722)
  - PRs bootstrap/26872, c++/27547, fortran/20460, fortran/24549,
	middle-end/27384, middle-end/27488, target/26545, target/27158
- fix libgcj.pc location and content on x86_64, ppc64 and s390x (#185230)
- make __dso_handle const, so that it is added into .data.rel.ro section
  in shared libraries
- fix a typo in __builtin_object_size computation (Richard Guenther,
  PR tree-optimization/27532)
- fix ICE on -O0 -g if static local variables are in unreachable code blocks
  (Jan Hubicka, PR debug/26881)
- fix ICEs with conflicts across abnormal edges (Zdenek Dvorak,
  PRs tree-optimization/27283, tree-optimization/27548,
  tree-optimization/27549)
- warn about OpenMP section 2.9 region nesting violations
- fix OpenMP fortran array REDUCTION with -fbounds-check (PR fortran/27446)
- fix OpenMP {{FIRST,LAST}PRIVATE,REDUCTION} in orphaned construct on
  Fortran dummy argument (PR middle-end/27416)
- fix ICE on #pragma omp for unsigned iteration variable (PR c/27499)

* Tue May  9 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-15
- update from gcc-4_1-branch (-r113623:113637)
  - PR fortran/27378
- update from trunk (-r109500:109501, -r109670:109671, -r111341:111342,
		     -r111704:111705, -r112546:112547, -r113111:113112,
		     -r113339:113341, -r113511:113513)
- fix loop peeling (Zdenek Dvorak, #190039, PR rtl-optimization/27335)

* Mon May  8 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-14
- update from gcc-4_1-branch (-r113489:113623)
  - PRs c++/27422, c++/27427, fortran/24813, fortran/25099, fortran/25681,
	fortran/27269, fortran/27324, libfortran/26985, objc/27240,
	target/26481, target/26765, tree-optimization/25985,
	tree-optimization/27151
- fix zero size field handling in structalias (Richard Guenther,
  PR tree-optimization/27409)
- fix PR tree-optimization/27136 (Richard Guenther)
- fix classification of invalid struct types on x86_64 (Volker Reichelt,
  PR target/27421)

* Wed May  3 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-13
- update from gcc-4_1-branch (-r113416:113489)
  - PRs c/25309, target/27374, target/27387, tree-optimization/27364
- merge gomp changes from trunk (-r113267:113271, -r113411:113412,
  -r113452:113456, -r113482:113483, -r113493:113494)
  - PR fortran/27395
- additional gomp fixes (PRs c++/27359, middle-end/27388)
- package SYSCALLS.c.X for protoize (#190047)
- fix gcj -fprofile-arcs -ftest-coverage (Alexandre Oliva, #177450)
- reenable profiledbootstrap
- in 64-bit builds remove 32-bit /usr/lib/lib* libraries from the
  buildroots (and similarly on 32-bit builds remove 64-bit /usr/lib64/lib*)
  before AutoReq generation (#190541)

* Mon May  1 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-12
- update from gcc-4_1-branch (-r113242:113416)
  - PRs c++/26534, c++/26912, c++/27094, c++/27278, c++/27279, fortran/26017,
	libgfortran/20257, libgfortran/27304, libgfortran/27360,
	libstdc++/26513, middle-end/26565, middle-end/26869,
	rtl-optimization/26685, target/26826
- merge gomp changes from trunk (-r113255:113256, -r113420:113421)
  - PRs libgomp/25865, c/27358
- assorted gomp fixes (PRs middle-end/27325, middle-end/27310,
  middle-end/27328, middle-end/27337, c++/26943)
- fix builtin memset (Alan Modra, PR middle-end/27260, PR middle-end/27095)

* Tue Apr 25 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-11
- update from gcc-4_1-branch (-r113149:113242)
  - PRs c/25875, c/26774, fortran/18803, fortran/25597, fortran/25669,
	fortran/26787, fortran/26822, fortran/26834, fortran/27089,
	fortran/27113, fortran/27122, fortran/27124, target/21283,
	target/26961
- fix number of iterations computation (Zdenek Dvorak, #189376,
  PR tree-optimization/27285)
- fix handling of volatile in the inliner (Andrew Pinski, Richard Guenther,
  PR tree-optimization/27236)
- strip useless type conversions in the inliner (Andrew Pinski,
  Richard Guenther, PR tree-optimization/27218)

* Fri Apr 21 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-10
- update from gcc-4_1-branch (-r113110:113149)
  - PRs libgcj/21941, libgcj/27170, libgcj/27231, libgfortran/27138,
	libstdc++/26424, mudflap/26789
- improve dir/../-stripping code to support /usr/lib64 and /usr/lib in
  separate AFS mountpoints (Alexandre Oliva, #137200)
- fix fortran real(16) transpose and reshape on 32-bit architectures
  (PR fortran/26769)
- fix i?86/x86_64 vector extraction (Alexandre Oliva, #187450)
- fix testcase for ppc32 va_arg bug
- fix testsuite log uuencoding
- fix acats timeout framework

* Thu Apr 20 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-9
- update from gcc-4_1-branch (-r112951:113110)
  - PRs c++/10385, c++/26036, c++/26365, c++/26558, classpath/27163,
	fortran/26769, libgcj/27171, libgfortran/26766, libstdc++/27162,
	middle-end/27095, middle-end/27134, target/27182,
	tree-optimization/26643, tree-optimization/26821,
	tree-optimization/26854, tree-optimization/27087
- fix ppc32 va_arg bug (Alan Modra)
- assorted gomp fixes (PRs c++/25874, middle-end/25989, c/25996, c/26171,
  middle-end/26913)
- fix pretty printing C array types (#188944)
- fix ICE on unprototyped alloca (PR tree-optimization/26865)
- fix truncation optimization overflow handling (PR middle-end/26729)
- uuencode dejagnu testsuite log files in rpmbuild output

* Fri Apr 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-8
- update from gcc-4_1-branch (-r112825:112951)
  - PRs c++/26122, c++/26295, fortran/23634, fortran/25619, fortran/26257,
	libgcj/23829, libgcj/26522, libgfortran/26890, target/27006
- merge gomp changes from trunk (-r112934:112935)
  - PR libgomp/26651
- fix ICE in gomp handling of EH regions (PR middle-end/26823)

* Mon Apr 10 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-7
- update from gcc-4_1-branch (-r112727:112825)
  - PRs fortran/19101, fortran/25031, fortran/26779, fortran/26891,
	fortran/26976, target/26508, tree-optimization/26919
- fix libgfortran printing of REAL*16 for IEEE quad and IBM extended formats
  (PR libgfortran/24685)
- fix Fortran -fbounds-check (Roger Sayle, #188409, PR middle-end/22375)
- fix Java StackTraceElement.toString() (Mark Wielaard, #183212,
  PR classpath/27081)
- fix -fopenmp -static

* Thu Apr  6 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-6
- update from gcc-4_1-branch (-r112706:112727)
  - PRs classpath/24752, classpath/27028, libgcj/26625, libgcj/27024,
	tree-optimization/26996
- reenable PR c++/19238, c++/21764 fixes, only PR c++/21581 is not
  applied
- better fix for Java GC vs. pthread_create (Bryce McKinlay, #182263,
  PR libgcj/13212)
- fix objc_push_parm (#185398)
- fix ICE with -feliminate-dwarf2-dups and using namespace (#187787,
  PR debug/27057)

* Wed Apr  5 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-5
- update from gcc-4_1-branch (-r112431:112706)
  - PRs bootstrap/26936, bootstrap/27023, classpath/25924, fortran/19303,
	fortran/25358, fortran/26816, java/25414, java/26042, java/26858,
	libfortran/26735, libgcj/26990, libstdc++/26777, testsuite/25741,
	tree-optimization/18527, tree-optimization/26763,
	tree-optimization/26830
- merge gomp changes from trunk (-r112602:112603 and -r112618:112619)
- temporarily revert PR c++/21764, c++/19238, c++/21581 fixes (#187399)

* Tue Mar 28 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-4
- update from gcc-4_1-branch (-r111697:112431)
  - PRs ada/25885, c/26004, fortran/17298, fortran/20935, fortran/20938,
	fortran/23092, fortran/24519, fortran/24557, fortran/25045,
	fortran/25054, fortran/25075, fortran/25089, fortran/25378,
	fortran/25395, fortran/26041, fortran/26054, fortran/26064,
	fortran/26107, fortran/26277, fortran/26393, fortran/26716,
	fortran/26741, libfortran/21303, libfortran/24903, libgcj/24461,
	libgcj/25713, libgcj/26103, libgcj/26688, libgcj/26706,
	libgfortran/26499, libgfortran/26509, libgfortran/26554,
	libgfortran/26661, libgfortran/26880, libstdc++/26132,
	middle-end/18859, middle-end/19543, middle-end/26557,
	middle-end/26630, other/26489, target/25917, target/26347,
	target/26459, target/26532, target/26607, tree-optimization/26524,
	tree-optimization/26587, tree-optimization/26672
  - fix visibility and builtins interaction (Jason Merrill,
    PR middle-end/20297, #175442)
- merge gomp changes from trunk (-r112022:112023, -r112250:112251,
  -r112252:112253, -r112350:112351 and -r112282:112283)
  - PRs c++/26691, middle-end/26084, middle-end/26611, c++/26690,
	middle-end/25989
- support visibility attribute on namespaces (Jason Merrill, PR c++/21764,
  PR c++/19238)
- use hidden visibility for anonymous namespaces by default (Jason Merrill,
  PR c++/21581)

* Thu Mar  9 2006 Alexandre Oliva <aoliva@redhat.com> 4.1.0-3
- make ppc32 TLS PIC code sequences compatible with secure plt (#184446)
  (Richard Henderson and myself)

* Sat Mar  4 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-2
- update from gcc-4_1-branch (-r111570:111697)
  - PRs c++/26291, libgfortran/26136, libgfortran/26423, libgfortran/26464,
	libstdc++/26526, rtl-optimization/26345, target/19061, target/26453
- handle DW_CFA_val_{offset,offset_sf,expression} in the libgcc{,_s} unwinder

* Tue Feb 28 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-1
- update from gcc-4_1-branch (-r111466:111570)
  - GCC 4.1.0 release
  - PR other/26473

* Mon Feb 27 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.31
- add __floatuns[sdt]i[sdxt]f exports to libgcc_s.so.1 (Joseph S. Myers)
- fix unwinding through signal frames (#175951, PR other/26208, glibc BZ#300)

* Mon Feb 27 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.30
- update from gcc-4_1-branch (-r111278:111466)
  - GCC 4.1.0 RC2
  - PRs fortran/26201, libobjc/26309, rtl-optimization/25603, target/25603
  - fix nested vector shifts (#182047, PR middle-end/26379)
- merge gomp changes from trunk (-r111390:111391, -r111428:111429 and
  -r111440:111441)
  - PR middle-end/26412
- fortran MATMUL optimization (Richard Sandiford)
- fortran WHERE optimizations (Roger Sayle)
- x86_64 _mm_monitor fixes (H.J. Lu, PR target/24879)
- add MNI support on i?86/x86_64, -mmni option and <tmmintrin.h> header
  (H.J Lu)

* Sun Feb 19 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.29
- update from gcc-4_1-branch (-r111179:111278)
  - PRs ada/13408, c++/26266, target/22209, target/26189
  - fix ppc32 -fpic reload problem with extenddftf2 pattern
    (David Edelsohn, #181625, PR target/26350)
  - fix the PR middle-end/26334 patch

* Fri Feb 17 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.28
- update from gcc-4_1-branch (-r110978:111179)
  - PRs ada/20753, bootstrap/16787, bootstrap/26053, fortran/25806,
	libfortran/15234, libgfortran/25949, middle-end/25335,
	target/25259, target/26255
  - fix ICE with shift by -1 (#181586, PR middle-end/26300)
- merge gomp changes from trunk (-r110983:110984, -r111017:111018,
  -r111152:111153 and -r111204:111205)
  - PRs bootstrap/26161, fortran/26224, libgomp/25938, libgomp/25984
- don't define _REENTRANT in gthr*.h (#176278, PR libstdc++/11953)
- define _REENTRANT if -pthread and _POSIX_SOURCE if -posix on s390{,x}
  and ia64
- fix ICE with register variable and __asm statement (#181731,
  PR middle-end/26334)

* Tue Feb 14 2006 Alexandre Oliva <aoliva@redhat.com> 4.1.0-0.27
- merge fix by Zdenek Dvorak for regression introduced by patch for PR
  tree-optimization/26209

* Tue Feb 14 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.26
- update from gcc-4_1-branch (-r110903:110978)
  - PRs fortran/20861, fortran/20871, fortran/25059, fortran/25070,
	fortran/25083, fortran/25088, fortran/25103, fortran/26038,
	fortran/26074, inline-asm/16194, libfortran/24685,
	libfortran/25425, target/26141, tree-optimization/26258
- ABI change - revert to GCC 3.3 and earlier behaviour of
  zero sized bitfields in packed structs (Michael Matz, PR middle-end/22275)
- fix valarrays vs. non-POD (Paolo Carlini, Gabriel Dos Reis,
  PR libstdc++/25626)
- fix C++ duplicate declspec diagnostics (Volker Reichelt, PR c++/26151)
- fix dominance ICE (Zdenek Dvorak, PR tree-optimization/26209)
- add some new Intel {,e,x}mmintrin.h intrinsics (H.J. Lu)
- speedup bitset<>::_M_copy_to_string (Paolo Carlini)
- fix tree_expr_nonzero_p (Jeff Law)
- fix TRUTH_XOR_EXPR handling in VRP (Jeff Law)

* Mon Feb 13 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.25
- update from gcc-4_1-branch (-r110831:110903)
  - PRs c++/16405, c++/24996, fortran/14771, fortran/20858, fortran/25756,
	middle-end/22439
- merge gomp changes from trunk (-r110719:110720, -r110852:110853 and
  -r110907:110908)
  - PR libgomp/25936
- fix gimplification of const fn pointers to builting functions
  (PR middle-end/26092)
- make sure Fortran length artifical variables aren't SAVEd (Andrew Pinski,
  PR fortran/26246)

* Fri Feb 10 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.24
- update from gcc-4_1-branch (-r110632:110831)
  - PRs tree-opt/26180, c++/26070, c++/26071, fortran/25577, java/26192,
	libfortran/23815, libstdc++/26127, target/23359, target/26109,
	tree-opt/25251
- remove gcc-ppc32, gcc-c++-ppc32, gcc-sparc32 and gcc-c++-sparc32
  subpackages, they do more harm than good.  Particularly this time
  gcc*ppc32 and gcc*sparc32 defaulted to DFmode long double rather
  than TFmode long double

* Mon Feb  6 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.23
- update from gcc-4_1-branch (-r110582:110632)
  - PRs classpath/24618, classpath/25141, classpath/25727, fortran/25046,
	fortran/26039
- use LOGICAL*1 instead of LOGICAL*4 for Fortran where temporary masks
  (Roger Sayle)
- fix symbol versions in s390 libgcc_s.so.1
- sparc32 and alpha long double fixes
- BuildRequires libXt-devel
- BuildRequires and Requires glibc-devel >= 2.3.90-35 on arches
  that are switching long double

* Sat Feb  4 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.22
- fix ia64 debug info patch
- fix libjava pthread_create wrapper patch

* Sat Feb  4 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.21
- update from gcc-4_1-branch (-r110433:110582)
  - PRs c++/25342, c++/25979, fortran/20845, fortran/24266,
	fortran/24958, fortran/25072, libstdc++/21554, middle-end/24901,
	middle-end/25977, middle-end/26001, target/25864, target/25926,
	target/25960
  - put ia64 read-only sections that require runtime relocations
    even in -fno-pic code into .data.rel.ro etc. sections
    rather than .rodata to avoid DT_TEXTREL binaries
    (Richard Henderson, PR target/26090)
- merge gomp changes from trunk (-r110511:110512 and -r110549:110552)
- fix ia64 debug info coverage of epilogues (Alexandre Oliva, PR debug/24444)
- export pthread_create from libgcj.so.7 as a wrapper around
  libpthread.so.0's pthread_create that handles GC (Anthony Green, Tom Tromey)
- BC-ABI java lookup fix (Andrew Haley, #179070, #178156)
- on sparc64 emit .register %g7,#ignore instead of .register %g7,#scratch
  to avoid problems with TLS or -fstack-protector
- switch to IBM extended format long double by default on ppc and ppc64
- switch to IEEE 754 quad format long double by default on s390, s390x,
  sparc32 and alpha

* Wed Feb  1 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.20
- merge from gomp-20050808-branch (up to -r110392)
  - fix PR c++/25874 (Diego Novillo)

* Wed Feb  1 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.19
- s390{,x} long double patch fix for s390x ICEs on test-ldouble
  and tst-align2 (Andreas Krebbel)

* Tue Jan 31 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.18
- update from gcc-4_1-branch (-r110317:110433)
  - PRs c++/25855, c++/25999, fortran/17911, fortran/18578, fortran/18579,
	fortran/20857, fortran/20885, fortran/20895, fortran/25030,
	fortran/25835, fortran/25951, java/21428, libgfortran/25835,
	target/14798, target/25706, target/25718, target/25947,
	target/26018, testsuite/25318
- add -mtune=generic support for i?86 and x86_64 (Jan Hubicka, H.J. Lu,
  Evandro Menezes)
- use -mtune=generic by default if neither -march= nor -mtune= is specified
  on command line on i?86 or x86_64
- updated s390{,x} long double patch, fixing ICEs on s390x glibc build
  (Andreas Krebbel, Ulrich Weigand)

* Sat Jan 28 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.17
- update from gcc-4_1-branch (-r110062:110317)
  - PRs ada/20548, ada/21317, bootstrap/25859, c++/25552, c++/25856,
	c++/25858, c++/25895, c/25892, fortran/18540, fortran/20852,
	fortran/20881, fortran/23308, fortran/24276, fortran/25084,
	fortran/25085, fortran/25086, fortran/25124, fortran/25416,
	fortran/25538, fortran/25625, fortran/25710, fortran/25716,
	fortran/25901, fortran/25964, java/25816, other/24829,
	rtl-optimization/24626, rtl-optimization/25654, target/24831,
	testsuite/24962, testsuite/25590
- atomic builtin fixes (Richard Henderson)
- -mlong-double-128 support on ppc32 (David Edelsohn, Alan Modra)
- -mlong-double-128 support on s390 and s390x (Andreas Krebbel,
  Ulrich Weigand)

* Sat Jan 21 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.16
- update from gcc-4_1-branch (-r109815:110062)
  - PRs ada/24533, c++/16829, c++/22136, c++/25836, c++/25854, c/25805,
	classpath/20198, fortran/20869, fortran/20875, fortran/25024,
	fortran/25631, fortran/25697, fortran/25785, libgcj/25840,
	libgfortran/25631, libgfortran/25697, libstdc++/25823,
	libstdc++/25824, target/25731, testsuite/25171
  - fix X509Certificate.java (#174708, #177733)

* Tue Jan 17 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.15
- update from gcc-4_1-branch (-r109401:109815)
  - PRs c++/24824, c++/25386, c++/25663, c/25682, classpath/25803,
	fortran/12456, fortran/20868, fortran/20870, fortran/21256,
	fortran/21977, fortran/22146, fortran/24640, fortran/25029,
	fortran/25093, fortran/25101, fortran/25486, fortran/25598,
	fortran/25730, libgcj/21637, libgcj/23499, libgfortran/25598,
	libstdc++/23591, libstdc++/25472, rtl-optimization/24257,
	rtl-optimization/25367, rtl-optimization/25662, target/20754,
	target/25042, target/25168, testsuite/25728, testsuite/25777,
	tree-opt/24365, tree-optimization/23109, tree-optimization/23948,
	tree-optimization/24123, tree-optimization/25125
- update from gomp-20050608-branch (up to -r109816)
- fix ppc32 libffi (#177655)
- fix lookup_conversions_r (#177918)
- define __STDC__ as a normal macro rather than a preprocessor builtin
  unless it needs to change its value between system and non-system
  headers (PR preprocessor/25717)

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.14
- update from gcc-4_1-branch (-r109369:109401)
  - PR fortran/23675
  - fix Java shutdown hook (Tom Tromey, #165136)
- fix libjava/shlibpath.m4 (PR libgcj/24940)

* Thu Jan  5 2006 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.13
- update from gcc-4_1-branch (-r108957:109369)
  - PRs c++/23171, c++/23172, c++/24671, c++/24782, c++/25294, c++/25417,
	c++/25439, c++/25492, c++/25625, c++/25632, c++/25633, c++/25634,
	c++/25635, c++/25637, c++/25638, c/25183, c/25559, debug/25562,
	fortran/18990, fortran/19362, fortran/20244, fortran/20862,
	fortran/20864, fortran/20889, fortran/22607, fortran/23152,
	fortran/25018, fortran/25053, fortran/25055, fortran/25063,
	fortran/25064, fortran/25066, fortran/25067, fortran/25068,
	fortran/25069, fortran/25106, fortran/25391, fortran/25532,
	fortran/25586, fortran/25587, libgcj/9715, libgcj/19132,
	libgfortran/25139, libgfortran/25419, libgfortran/25510,
	libgfortran/25550, libgfortran/25594, middle-end/24827, objc/25328,
	rtl-optimization/21041, rtl-optimization/25130, target/24342,
	target/25554, target/25572, testsuite/25214, testsuite/25441,
	testsuite/25442, testsuite/25444, tree-opt/25513
  - create java Package for compiled classes which are linked in but
    loaded by the system class loader (Tom Tromey, #176956)
  - fix posix_memalign prototype in <mm_malloc.h> (#176461)
- update from gomp-20050608-branch (up to -r109349)
- buildrequire libXtst-devel (#176898)
- fix built in path to classmap.db on x86_64, s390x and ppc64 (#176562)
- fix debug info for preprocessed Fortran code (#175071, PR fortran/25324)

* Fri Dec 22 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.12
- make sure GCJFLAGS are propagated down to libjava's configure
- build crt{begin,end}*.o with -fno-asynchronous-unwind-tables
  if RPM_OPT_FLAGS include -fasynchronous-unwind-tables
- fix PR c++/25369 (Mark Mitchell)
- fix PR libgfortran/25307 (Jerry DeLisle)

* Thu Dec 22 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.11
- update from gcc-4_1-branch (-r108861:108957)
  - PRs debug/25518, fortran/24268, fortran/25423, libgfortran/25463,
	rtl-optimization/25196, tree-optimization/24793
- validate changes in forward copy propagation (PR target/25005)
- fix Java constants constructors on 64-bit big endian arches
  (Andrew Haley, PR java/25535)
- fix PR c++/25364 (Mark Mitchell)

* Wed Dec 21 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.10
- update from gcc-4_1-branch (-r108539:108861)
  - PRs ada/18659, ada/18819, c++/20552, c++/21228, c++/24278, c++/24915,
	fortran/18197, fortran/25458, libgfortran/25039, libgfortran/25264,
	libgfortran/25349, libobjc/14382, libstdc++/25421, middle-end/22313,
	middle-end/24306, rtl-optimization/23837, rtl-optimization/25224,
	rtl-optimization/25310, target/24969, testsuite/25215,
	tree-optimization/23838, tree-optimization/24378
- update from gomp-20050608-branch (up to -r108859)
  - fix _Pragma handling (Richard Henderson, PR preprocessor/25240)
- fix reload re-recognition of insns (Alan Modra, PR rtl-optimization/25432)
- don't peephole RTX_FRAME_RELATED_P insns (Andrew Haley,
  PR middle-end/25121)

* Thu Dec 15 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.9
- fix OpenMP lastprivate handling for global vars (Aldy Hernandez)
- fix gnu.xml.dom.DomNode's detach method (Caolan McNamara,
  PR classpath/25426)
- fix up the #175569 fix (Tom Tromey, #175833, PR java/25429)
- fix strength reduction miscompilation of libgnomecanvas
  (#175669, PR rtl-optimization/24899)
- create libgcj-*.jar with -@E options and feed a sorted list to
  it rather than relying on filesystem sorting

* Wed Dec 14 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.8
- update from gcc-4_1-branch (-r108414:108539)
  - PRs classpath/25389, fortran/23815, fortran/25078, target/25254
- fix Java ICE on initialized static final var used in case
  (Andrew Haley, #175569, PR java/25429)
- fix crash in _Unwind_IteratePhdrCallback (Andrew Haley)
- don't Require alsa-lib-devel, just BuildRequire it
  (#175627)
- use .gnu.linkonce.d.rel.ro.* sections for objects that
  are constant after relocation processing

* Mon Dec 12 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.7
- update from gcc-4_1-branch (-r108157:108414)
  - PRs c++/19317, c++/19397, c++/19762, c++/19764, c++/25010, c++/25300,
	c++/25337, debug/24908, fortran/25292, libfortran/25116,
	libgcj/25265, target/17828, target/19005, target/23424,
	target/25212, target/25258, target/25311, testsuite/20772,
	testsuite/24478, testsuite/25167, tree-optimization/25248
- update from gomp-20050608-branch (up to -r108424)
- add BuildReq for alsa-lib-devel and configure with --disable-dssi
- sort files in libgcj-*.jar and touch them to latest ChangeLog
  timestamp, so that libgcj-*.jar is identical across multilib arches
- don't use pushw instruction on i?86, as that leads to ICEs
  in def_cfa_1, because negative CFA offsets not multiple of 4
  aren't representable in the unwind and debug info (PR debug/25023,
  PR target/25293)
- fix ICEs with x86_64 -mlarge-data-threshold=N and STRING_CSTs
  (Jan Hubicka, PR target/24188)
- fix Java ICE with input_filename being unset (Alexandre Oliva, #174912)
- don't accept invalid int x,; in C++ (Petr Machata, PR c++/24907)
- fix Java ICE in do_resolve_class (Andrew Haley, PR java/25366,
  PR java/25368)
- make sure g*.dg/compat/struct-layout-1.exp generated tests
  don't use arrays with entries aligned more than their size (PR c++/25331)
- don't use -liberty in g++.dg/compat/struct-layout-1.exp tests

* Wed Dec  7 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.6
- allow #pragmas at C struct scope as well as ObjC class scope
  (PR c/25246)
- some gomp testcase fixes

* Wed Dec  7 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.5
- update from gcc-4_1-branch (-r107810:108157)
  - PRs bootstrap/25207, c++/24103, c++/24138, c++/24173, fortran/15809,
	fortran/21302, fortran/23912, java/25283, libfortran/24919,
	libgfortran/25149, middle-end/25176, other/13873, target/18580,
	target/24108, target/24475, target/24934, target/25199,
	testsuite/25247, tree-optimization/24963
- update from gomp-20050608-branch (up to -r108105)
- -Wstrict-aliasing C++ support (Richard Guenther, Dirk Mueller,
  Paolo Carlini, PRs c++/14024, libstdc++/24975)
- fix mark_used_regs regression (Andreas Krebbel, PR rtl-optimization/24823)
- fix reload ICE (Kaz Kojima, PR target/24982)
- fix PPC ICE on Linux kernel (Paolo Bonzini, PR target/24982)
- fix s390{,x} shifts with shift count ANDed with constant mask
  (Andreas Krebbel, PR target/25268)
- s390{,x} atomic builtins enhancements (Adrian Straetling)

* Thu Dec  1 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.4
- update from gcc-4_1-branch (-r107618:107810)
  - PRs c++/21123, c++/21166, fortran/24223, fortran/24705, java/18278,
	libgfortran/25109, middle-end/20109, middle-end/25120,
	middle-end/25158, rtl-opt/24930
- use %%{_tmppath} in BuildRoot (#174594)
- require libgomp in gcc subpackage
- fix Java .so symlinks

* Tue Nov 29 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.3
- fix IA-64 local-exec TLS handling
- fix IA-64 __sync_fetch_and_{sub,xor,...}

* Mon Nov 28 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.2
- update from gcc-4_1-branch (-r107462:107618)
  - PRs fortran/24917, libgcj/25016, libgfortran/24945, middle-end/21309,
	middle-end/25022, libfortran/24991
- update from gomp-20050608-branch (up to -r107619)
  - fix omp_get_wti{me,ck} on older kernels
- ppc32 EH fix
- fix #pragma omp atomic
- resurrected multi32 hack for ppc32 and sparc32

* Thu Nov 24 2005 Jakub Jelinek <jakub@redhat.com> 4.1.0-0.1
- initial 4.1 package, using newly created redhat/gcc-4_1-branch
