%global DATE 20141101
%global SVNREV 216995
%global gcc_version 4.9.2
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 1
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc ppc64 ppc64p7 alpha %{arm} aarch64
%global build_ada 1
%else
%global build_ada 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 %{arm}
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 %{arm}
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%global build_cloog 1
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_9-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global isl_version 0.12.2
Source1: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
%global cloog_version 0.18.1
Source2: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
BuildRequires: binutils >= 2.24
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
%if %{build_go}
BuildRequires: hostname
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
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
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
Requires: binutils >= 2.24
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true
Provides: bundled(libiberty)

Patch0: gcc49-hack.patch
Patch1: gcc49-java-nomulti.patch
Patch2: gcc49-ppc32-retaddr.patch
Patch3: gcc49-rh330771.patch
Patch4: gcc49-i386-libgomp.patch
Patch5: gcc49-sparc-config-detection.patch
Patch6: gcc49-libgomp-omp_h-multilib.patch
Patch7: gcc49-libtool-no-rpath.patch
Patch8: gcc49-cloog-dl.patch
Patch9: gcc49-cloog-dl2.patch
Patch10: gcc49-pr38757.patch
Patch11: gcc49-libstdc++-docs.patch
Patch12: gcc49-no-add-needed.patch
Patch14: gcc49-pr56493.patch
Patch15: gcc49-color-auto.patch
Patch16: gcc49-libgo-p224.patch
Patch17: gcc49-aarch64-async-unw-tables.patch
Patch18: gcc49-aarch64-unwind-opt.patch
Patch19: gcc49-pr63659.patch

Patch1100: cloog-%{cloog_version}-ppc64le-config.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.9.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.9 shared support library
Group: System Environment/Libraries
Autoreq: false
%if !%{build_ada}
Obsoletes: libgnat < %{version}-%{release}
%endif
Obsoletes: libmudflap
Obsoletes: libmudflap-devel
Obsoletes: libmudflap-static
Obsoletes: libgcj < %{version}-%{release}
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
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
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Group: Development/Libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Group: Development/Libraries
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Group: Development/Libraries
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Group: Development/Libraries
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Group: Development/Libraries
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Group: Development/Libraries
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.

%package -n libcilkrts
Summary: The Cilk+ runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n libcilkrts-static
Summary: The Cilk+ static runtime library
Group: Development/Libraries
Requires: libcilkrts = %{version}-%{release}

%description -n libcilkrts-static
This package contains the Cilk+ static runtime library.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: filesystem >= 3
Provides: /lib/cpp
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
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
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries
Group: Development/Languages
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Group: Development/Languages
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo = %{version}-%{release}
Autoreq: true

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Group: Development/Libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%global __debug_package 1
%global __debug_install_post \
   %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
    %{_builddir}/gcc-%{version}-%{DATE}/split-debuginfo.sh\
%{nil}

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: gcc-base-debuginfo = %{version}-%{release}

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files debuginfo -f debugfiles.list
%defattr(-,root,root)

%package base-debuginfo
Summary: Debug information for libraries from package %{name}
Group: Development/Debug
AutoReqProv: 0

%description base-debuginfo
This package provides debug information for libgcc_s, libgomp and
libstdc++ libraries from package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files base-debuginfo -f debugfiles-base.list
%defattr(-,root,root)
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch8 -p0 -b .cloog-dl~
%patch9 -p0 -b .cloog-dl2~
%endif
%patch10 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch11 -p0 -b .libstdc++-docs~
%endif
%patch12 -p0 -b .no-add-needed~
%patch14 -p0 -b .pr56493~
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
%patch15 -p0 -b .color-auto~
%endif
%patch16 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch17 -p0 -b .aarch64-async-unw-tables~
%patch18 -p0 -b .aarch64-unwind-opt~
%patch19 -p0 -b .pr63659~

%if 0%{?_enable_debug_packages}
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)'`; do
    echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
    if [ -f "$f" -a ! -L "$f" ]; then
      cp -a "$f" "${BUILDDIR}"/test.debug
      /usr/lib/rpm/debugedit -b "${RPM_BUILD_DIR}" -d /usr/src/debug \
			     -l "${BUILDDIR}"/debugsources-base.list \
			     "${BUILDDIR}"/test.debug
      rm -f "${BUILDDIR}"/test.debug
    fi
  done
  for f in `find usr/lib/debug/.build-id -type l`; do
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  grep -v -f "${BUILDDIR}"/debugfiles-base.list \
    "${BUILDDIR}"/debugfiles.list > "${BUILDDIR}"/debugfiles.list.new
  mv -f "${BUILDDIR}"/debugfiles.list.new "${BUILDDIR}"/debugfiles.list
  for f in `LC_ALL=C sort -z -u "${BUILDDIR}"/debugsources-base.list \
	    | grep -E -v -z '(<internal>|<built-in>)$' \
	    | xargs --no-run-if-empty -n 1 -0 echo \
	    | sed 's,^,usr/src/debug/,'`; do
    if [ -f "$f" ]; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
      echo "%%exclude /$f" >> "${BUILDDIR}"/debugfiles.list
    fi
  done
  mv -f "${BUILDDIR}"/debugfiles-base.list{,.old}
  echo "%%dir /usr/lib/debug" > "${BUILDDIR}"/debugfiles-base.list
  awk 'BEGIN{FS="/"}(NF>4&&$NF){d="%%dir /"$2"/"$3"/"$4;for(i=5;i<NF;i++){d=d"/"$i;if(!v[d]){v[d]=1;print d}}}' \
    "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  cat "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  rm -f "${BUILDDIR}"/debugfiles-base.list.old
fi
EOF
chmod 755 split-debuginfo.sh
%endif

%patch1100 -p0 -b .cloog-ppc64le-config~

sed -i -e 's/4\.9\.3/4.9.2/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
# Default to -gdwarf-4 -fno-debug-types-section rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(4)/' gcc/common.opt
sed -i '/flag_debug_types_section/s/Init(1)/Init(0)/' gcc/common.opt
sed -i '/dwarf_record_gcc_switches/s/Init(0)/Init(1)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\14./' gcc/doc/invoke.texi
%else
# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi
sed -i 's/#define[[:blank:]]*EMIT_ENTRY_VALUE[[:blank:]].*$/#define EMIT_ENTRY_VALUE 0/' gcc/{var-tracking,dwarf2out}.c
sed -i 's/#define[[:blank:]]*EMIT_TYPED_DWARF_STACK[[:blank:]].*$/#define EMIT_TYPED_DWARF_STACK 0/' gcc/dwarf2out.c
sed -i 's/#define[[:blank:]]*EMIT_DEBUG_MACRO[[:blank:]].*$/#define EMIT_DEBUG_MACRO 0/' gcc/dwarf2out.c
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_cloog}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
../../isl-%{isl_version}/configure --disable-shared \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ..

mkdir cloog-build cloog-install
cd cloog-build
cat >> ../../cloog-%{cloog_version}/source/isl/constraints.c << \EOF
#include <isl/flow.h>
static void __attribute__((used)) *s1 = (void *) isl_union_map_compute_flow;
static void __attribute__((used)) *s2 = (void *) isl_map_dump;
EOF
sed -i 's|libcloog|libgcc49privatecloog|g' \
  ../../cloog-%{cloog_version}/{,test/}Makefile.{am,in}
isl_prefix=`cd ../isl-install; pwd` \
../../cloog-%{cloog_version}/configure --with-isl=system \
  --with-isl-prefix=`cd ../isl-install; pwd` \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
   --prefix=`cd ..; pwd`/cloog-install
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make %{?_smp_mflags} install
cd ../cloog-install/lib
rm libgcc49privatecloog-isl.so{,.4}
mv libgcc49privatecloog-isl.so.4.0.0 libcloog-isl.so.4
ln -sf libcloog-isl.so.4 libcloog-isl.so
ln -sf libcloog-isl.so.4 libcloog.so
cd ../..
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64 ppc64le ppc64p7
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
enablelgo=
enablelada=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
CC="$CC" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Werror=format-security / -Wformat -Werror=format-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--disable-multilib \
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu \
	--enable-languages=c,c++,objc,obj-c++,fortran${enablelada}${enablelgo},lto \
	--enable-plugin --enable-initfini-array \
	--disable-libgcj \
%if %{build_cloog}
	--with-isl=`pwd`/isl-install --with-cloog=`pwd`/cloog-install \
%else
	--without-isl --without-cloog \
%endif
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
	--with-arch=z196 --with-tune=zEC12 --enable-decimal-float \
%else
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%endif
%ifarch armv7hl
	--with-cpu=cortex-a8 --with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

%ifarch %{arm} sparc sparcv9 sparc64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libgomp,libatomic,libsanitizer,libcilkrts}

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libgomp,libatomic,libsanitizer,libcilkrts}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 $FULLPATH/
%endif

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
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

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64 ppc64p7
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%ifarch %{arm}
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_version}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.4 libobjc.so
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.5.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.1.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../libcilkrts.so.5.* libcilkrts.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.5.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.1.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../../%{_lib}/libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_libcilkrts}
mv -f %{buildroot}%{_prefix}/%{_lib}/libcilkrts.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.9.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.9.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.9.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.9.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.9.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.9.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.9.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.9.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.5.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.5.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.1.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 64/libcilkrts.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf lib32/libcilkrts.a libcilkrts.a
ln -sf ../lib64/libcilkrts.a 64/libcilkrts.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.4 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.5.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.5.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.1.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 32/libcilkrts.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../lib32/libcilkrts.a 32/libcilkrts.a
ln -sf lib64/libcilkrts.a libcilkrts.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libsupc++.a 32/libsupc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libasan.a 32/libasan.a
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libubsan.a 32/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libcilkrts.a 32/libcilkrts.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgobegin.a 32/libgobegin.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcilkrts.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.1.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0.*
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.5.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
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
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
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
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/gappletviewer || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-%{version} || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
cd obj-%{gcc_target_platform}

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan -p /sbin/ldconfig

%postun -n libasan -p /sbin/ldconfig

%post -n libubsan -p /sbin/ldconfig

%postun -n libubsan -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig

%postun -n libtsan -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig

%postun -n liblsan -p /sbin/ldconfig

%post -n libcilkrts -p /sbin/ldconfig

%postun -n libcilkrts -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig

%postun -n libgo -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cilk
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsanitizer.spec
%endif
%if %{build_cloog}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcloog-isl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcilkrts.so
%endif
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
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcilkrts.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.so
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.so
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%endif
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
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
%ifarch sparcv9 ppc
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
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%dir %{_prefix}/share/gcc-%{gcc_version}/python
%{_prefix}/share/gcc-%{gcc_version}/python/libstdcxx

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
%defattr(-,root,root,-)
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
%ifarch sparcv9 ppc
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
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.4*

%files gfortran
%defattr(-,root,root,-)
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%files -n libgfortran-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libasan.so.1*

%files -n libasan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libubsan.so.0*

%files -n libubsan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libcilkrts}
%files -n libcilkrts
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libcilkrts.so.5*

%files -n libcilkrts-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libcilkrts.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libcilkrts.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.a
%endif
%doc rpm.doc/changelogs/libcilkrts/ChangeLog* libcilkrts/README
%endif

%if %{build_go}
%files go
%defattr(-,root,root,-)
%{_prefix}/bin/gccgo
%{_mandir}/man1/gccgo.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/go1
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgobegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgobegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgo.so.5*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_version}
%{_prefix}/%{_lib}/go/%{gcc_version}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_version}
%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgobegin.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgobegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif

%files -n libgo-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%endif
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%changelog
* Sat Nov  1 2014 Jakub Jelinek <jakub@redhat.com> 4.9.2-1
- update from the 4.9 branch
  - GCC 4.9.2 release
  - PRs sanitizer/63638, sanitizer/63697, tree-optimization/63530
- handle REG_EQ* notes in REE (PR rtl-optimization/63659)
- include asan/lsan sanitizer/ includes

* Fri Oct 24 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-13
- update from the 4.9 branch
  - PRs bootstrap/63632, libfortran/63589, libstdc++/63500,
	lto/63603, tree-optimization/63563
- backport -f{,no-}sanitize-recover=<list> support from the trunk
- backport var-tracking fix (#1151226, PR debug/63623)

* Fri Oct 17 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-12
- update from the 4.9 branch
  - PRs ada/63225, c++/63306, c++/63405, c++/63415, c++/63437, c++/63455,
	c/63495, debug/63342, fortran/59488, ipa/61144, ipa/62121,
	libgfortran/63460, libgomp/61200, libstdc++/57440, libstdc++/59603,
	libstdc++/63199, libstdc++/63449, libstdc++/63456, lto/62026,
	regression/61510, rtl-optimization/57003, rtl-optimization/63448,
	sanitizer/61100, sanitizer/61530, sanitizer/61547, sanitizer/61897,
	sanitizer/62089, sanitizer/62140, target/52941, target/63428,
	tree-optimization/61969, tree-optimization/62031,
	tree-optimization/63302, tree-optimization/63375,
	tree-optimization/63379, tree-optimization/63380
  - initial -fsanitize=kernel-address support

* Tue Sep 30 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-11
- update from the 4.9 branch
  - PRs c++/61465, c++/62219, c++/63249, inline-asm/63282, middle-end/63247,
	plugins/63410, sanitizer/61272, target/49423, target/61407,
	target/62218, target/63335, tree-optimization/63341
- avoid fnsplit if there are forced labels accessed in between the partitions
  (#1106758, PR tree-optimization/63186)

* Mon Sep 22 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-10
- update from the 4.9 branch
  - PRs c++/62017, c++/63241, c++/63248, debug/63284, debug/63328, ipa/61654,
	target/61853, testsuite/63292
- fix scheduler -fcompare-debug issue (#1140872, PR debug/63285)

* Fri Sep 12 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-9
- update from the 4.9 branch
  - PRs c++/58624, c++/61214, c++/61659, c++/62129, c++/62224, c++/62659,
	c++/63139, c/61271, c/62294, fortran/62106, fortran/62142,
	fortran/62214, fortran/62215, fortran/62270, ipa/60449, ipa/61986,
	ipa/62015, libgfortran/62188, libstdc++/62264, libstdc++/63219,
	middle-end/61776, other/62008, other/62248, rtl-optimization/61672,
	rtl-optimization/62004, rtl-optimization/62030,
	rtl-optimization/62079, rtl-optimization/62146, target/61641,
	target/61996, target/62011, target/62038, target/62040, target/62111,
	target/62195, target/62261, target/62262, target/62312, target/63209,
	target/63223, target/63228, testsuite/56194, tree-optimization/60196,
	tree-optimization/62075, tree-optimization/62091,
	tree-optimization/62175, tree-optimization/63189
- fix s390{,x} return address handling in epilogues (#1131899,
  PR target/62662)

* Fri Aug 15 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-8
- update from the 4.9 branch
  - PRs fortran/62076, fortran/62107, lto/62032, middle-end/62092,
	target/61713
- allow elements/components of allocatables in !$omp atomic
  (PR fortran/62131)
- require/build require >= 2.24 binutils

* Thu Aug 14 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-7
- fix up scheduler deps handling fix (PR target/62025)
- vectorization fix (PR tree-optimization/62073)

* Wed Aug 13 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-6
- update from the 4.9 branch
  - PRs c++/58714, c++/60872, c++/61959, c++/61994, fortran/61999,
	libstdc++/61667, other/61962, tree-optimization/60707
  - fix scheduler deps handling of inc with clobbers vs. mem user (#1126463,
    PR target/62025)
- optimize slightly aarch64 unwind info
- backport arm vcvtf2i fix from trunk (PR target/62098)
- backport fold_ctor_reference big-endian fix (PR middle-end/62103)

* Thu Aug  7 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-5
- update from the 4.9 branch
  - PRs debug/61923, libstdc++/58962, libstdc++/61374, libstdc++/61390,
	libstdc++/61946, middle-end/61455, other/61963, target/60102,
	tree-optimization/61320, tree-optimization/61375

* Fri Aug  1 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-3
- update from the 4.9 branch
  - PRs fortran/61780, libobjc/61920, libstdc++/60037, target/47230,
	target/61656, target/61662, target/61794, target/61844,
	target/61855, tree-optimization/61964
  - fix libgfortran overflows on allocation (CVE-2014-5044)
- backport -fsanitize=alignment support from the trunk

* Thu Jul 24 2014 Dan Horák <dan[at]danny.cz> 4.9.1-2.1
- fix a LRA inheritance bug (#1117799)

* Thu Jul 17 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-2
- update from the 4.9 branch
  - PRs c-family/61741, rtl-optimization/61801, target/61737,
	tree-optimization/61779

* Wed Jul 16 2014 Jakub Jelinek <jakub@redhat.com> 4.9.1-1
- update from the 4.9 branch
  - GCC 4.9.1 release
  - PRs c++/58155, c++/58636, c++/61661, fortran/41936, fortran/58883,
	fortran/61459, libgfortran/61640, middle-end/53590,
	middle-end/61654, target/59843, target/61062, target/61544,
	tree-optimization/61680, tree-optimization/61681,
	tree-optimization/61684, tree-optimization/61725
- enable libitm on aarch64
- emit .note.GNU-stack on aarch64 (#1119885)
- small -fsanitize=bounds fix from the trunk

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> 4.9.0-15
- fix license handling

* Wed Jul  2 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-14
- update from the 4.9 branch
  - OpenMP 4.0 Fortran support
  - PRs c++/51253, c++/58704, c++/58753, c++/58781, c++/58930, c++/59867,
	c++/60249, c++/61242, c++/61382, c++/61433, c++/61488, c++/61500,
	c++/61537, c++/61539, c++/61566, c++/61614, c++/61647, fortran/60127,
	fortran/60928, libgfortran/61499, middle-end/57541, target/61503,
	target/61542, target/61586, target/61633, tree-optimization/57233,
	tree-optimization/61299, tree-optimization/61306
- fix combiner on s390 (#1102324, PR rtl-optimization/61673)
- some -fsanitize=undefined fixes from the trunk

* Wed Jun 25 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-13
- update from the 4.9 branch
  - PRs bootstrap/61583, c++/61556, ipa/61211, ipa/61540, libstdc++/61532,
	target/61570
- backport -fsanitize=bounds support from the trunk

* Thu Jun 19 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-12
- update from the 4.9 branch
  - PRs c++/59296, c++/60605, c++/61507, debug/57519

* Wed Jun 18 2014 Kyle McMartin <kyle@redhat.com> 4.9.0-11
- avoid applying patch 16 twice

* Wed Jun 18 2014 Richard Henderson <rth@redhat.com>
- import fix for PR target/61545 from the 4.9 branch

* Tue Jun 17 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-10
- update from the 4.9 branch
  - PRs fortran/45187, ipa/61186, libstdc++/60326, libstdc++/61269,
	rtl-optimization/61094, rtl-optimization/61446, target/61415,
	target/61423, target/61483

* Thu Jun 12 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-9
- update from the 4.9 branch
  - PRs c++/61343, fortran/61406, fortran/61418, ipa/61393,
	libfortran/61173, middle-end/61456, middle-end/61486,
	target/61300, target/61431, target/61443, tree-optimization/61452
  - fix up jump threading (#1094975, PR tree-optimization/61289)
- include vxworks-dummy.h in arm gcc-plugin-devel (PR plugins/45078)

* Thu Jun  5 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-8
- enable ada on arm

* Wed Jun  4 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-7
- update from the 4.9 branch
  - PRs c++/61020, c++/61134, c/58942, c/61053, ipa/61160, libstdc++/60734,
	libstdc++/61227, rtl-optimization/60866, rtl-optimization/60901,
	target/61239, tree-optimization/61383

* Thu May 29 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-6
- update from the 4.9 branch
  - PRs bootstrap/60984, c++/60189, c/60189, c/61191, fortran/60834,
	libfortran/61310, libgcc/61152, libstdc++/61143, libstdc++/61329,
	lto/60820, lto/61012, middle-end/58094, middle-end/61010,
	middle-end/61045, middle-end/61252, rtl-optimization/61215,
	rtl-optimization/61325, target/61044, target/61202, target/61208,
	target/61231, target/61249, target/61271, tree-optimization/60979
- backport -fsanitize=float-cast-overflow support from trunk

* Sun May 18 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-5
- update from the 4.9 branch
  - PRs debug/61013, ipa/60854, ipa/60897, ipa/61085, libfortran/61187,
	libgcc/61097, libstdc++/60966, lto/60981, rtl-optimization/60969,
	target/60969, target/61193, tree-optimization/61158

* Wed May 14 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-4
- update from the 4.9 branch
  - PRs c++/60019, c++/60999, c++/61083, c++/61151, driver/61106, ipa/60973,
	libfortran/61049, libstdc++/60594, libstdc++/61023, libstdc++/61086,
	libstdc++/61117, target/59952, target/60991, target/61055,
	target/61060, target/61092, tree-optimization/57864,
	tree-optimization/60902, tree-optimization/61009
- obsolete gcc-java and libjava*, remove all traces of build_java from the
  spec file (#1096474, #1095513)
- backport -fsanitize=float-divide-by-zero support from trunk

* Tue May  6 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-3
- update from the 4.9 branch
  - PRs driver/61065, ipa/60965
- disable gcc-java and libjava, broken by recent eclipse-ecj changes

* Mon May  5 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-2
- update from the 4.9 branch
  - PRs c++/60951, c++/60980, c++/60992, fortran/60495, ipa/60911, ipa/60912,
	libstdc++/59476, libstdc++/60497, libstdc++/60710, libstdc++/61036,
	lto/60720, middle-end/60891, middle-end/60895, target/60909,
	target/60941, target/61026, tree-optimization/60903,
	tree-optimization/60930, tree-optimization/60960,
	tree-optimization/60971
- backport -fno-sanitize-recover and -fsanitize-undefined-trap-on-error
  support from the trunk (PR sanitizer/60275)

* Tue Apr 29 2014 Richard Henderson <rth@redhat.com>
- enable ada, go and libatomic on aarch64

* Tue Apr 22 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-1
- update from the 4.9 branch
  - GCC 4.9.0 release
  - PRs c/59073, c/60819, fortran/58085, fortran/60717, libfortran/60810,
	middle-end/55022, middle-end/60281, middle-end/60467,
	middle-end/60469, middle-end/60849, other/43620, other/60644,
	target/60839, target/60847, target/60868, tree-optimization/59817,
	tree-optimization/60453, tree-optimization/60823,
	tree-optimization/60836, tree-optimization/60841,
	tree-optimization/60844

* Fri Apr 11 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.10
- update from the trunk and 4.9 branch
  - GCC 4.9.0-rc1
  - PRs ada/54040, ada/59346, c++/52844, ipa/60761, lto/60567,
	middle-end/60556, middle-end/60797, other/59055, testsuite/60773
  - fix CSE with non-volatile inline asm with multiple results or
    single result and clobbers (#1086332, PR rtl-optimization/60663)
- enable ppc64le in the spec file

* Wed Apr  9 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.9
- update from the trunk
  - PRs ada/60703, bootstrap/60620, bootstrap/60719, bootstrap/60743,
	c++/21113, c++/44613, c++/44859, c++/58207, c++/59115, c++/60374,
	c++/60573, c++/60626, c++/60642, c++/60708, c++/60713, c++/60731,
	debug/55794, debug/60655, fortran/60191, ipa/59626, ipa/60640,
	ipa/60659, ipa/60746, libstdc++/60270, middle-end/60706,
	middle-end/60729, middle-end/60750, rtl-optimization/60155,
	rtl-optimization/60604, rtl-optimization/60700,
	rtl-optimization/60776, sanitizer/60745, target/43751, target/54083,
	target/54407, target/60034, target/60363, target/60504, target/60602,
	target/60609, target/60650, target/60657, target/60697, target/60704,
	target/60735, target/60763, testsuite/60671, testsuite/60672,
	tree-optimization/60505, tree-optimization/60656,
	tree-optimization/60733, tree-optimization/60740,
	tree-optimization/60766, tree-optimization/60785

* Fri Mar 28 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.8
- update from the trunk
  - PRs c++/52369, c++/60331, c++/60375, c++/60566, c++/60574, c++/60627,
	c++/60628, c++/60689, c/35449, c/37428, c/39525, c/50347,
	fortran/34928, fortran/58880, fortran/60522, fortran/60677, ipa/60315,
	ipa/60600, libstdc++/60612, libstdc++/60658, middle-end/60635,
	middle-end/60682, other/59545, rtl-optimization/60452,
	rtl-optimization/60501, rtl-optimization/60650, sanitizer/56781,
	sanitizer/60636, target/60580, target/60672, target/60675,
	target/60693, testsuite/58013
- inliner speed fixes (PR ipa/60243)
- fortran wrong-code fix (PR fortran/60576)
- fix IPA-SRA with mismatched types between caller and callee
  (PR middle-end/60647)
- fix expansion of switch with constant index not optimized during gimple
  passes (PR target/60648)

* Mon Mar 24 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.7
- update from the trunk
  - PRs c++/60384, debug/60603, fortran/60599, ipa/59176, ipa/60419,
	libstdc++/60587, libstdc++/60623, rtl-optimization/60601,
	sanitizer/60613, target/60598, target/60610, tree-optimization/60577

* Thu Mar 20 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.6
- update from the trunk
  - PRs ada/39172, c++/51474, c++/54250, c++/59571, c++/60305, c++/60332,
	c++/60390, c++/60391, c++/60572, c/55383, fortran/55207,
	fortran/60283, fortran/60543, fortran/60549, libfortran/48600,
	libfortran/58324, libstdc++/60564, lto/59543, lto/60571,
	middle-end/60534, middle-end/60553, middle-end/60597, other/60589,
	rtl-optimization/56356, sanitizer/60535, sanitizer/60557,
	sanitizer/60569, target/60039, target/60516, target/60562,
	target/60563, target/60568, testsuite/58851, testsuite/60590,
	tree-optimization/60559

* Sat Mar 15 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.5
- update from the trunk
  - PRs ada/51483, ada/60411, bootstrap/58572, c++/53492, c++/58609,
	c++/60033, c++/60254, c++/60367, c++/60383, c++/60389, c++/60393,
	c++/60532, c/60197, debug/60438, fortran/51976, fortran/60392,
	fortran/60447, ipa/58721, ipa/60457, libfortran/38199,
	libfortran/60128, libgcc/59339, libgcc/60472, libgfortran/60128,
	libstdc++/59392, libstdc++/60499, lto/60424, lto/60427, lto/60461,
	middle-end/36282, middle-end/60418, middle-end/60445,
	middle-end/60474, middle-end/60482, middle-end/60484,
	middle-end/60518, rtl-optimization/57189, rtl-optimization/57320,
	rtl-optimization/60508, target/58271, target/58595, target/59396,
	target/60264, target/60486, target/60525, tree-optimization/59025,
	tree-optimization/59779, tree-optimization/60429,
	tree-optimization/60454, tree-optimization/60485,
	tree-optimization/60502

* Thu Mar  6 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.4
- update from the trunk
  - PRs c++/60361, c++/60409, debug/60381, testsuite/59308

* Wed Mar  5 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.3
- update from the trunk
  - PRs bootstrap/48230, bootstrap/50927, bootstrap/52466, bootstrap/60343,
	c++/11586, c++/14710, c++/50025, c++/54359, c++/54440, c++/55877,
	c++/57132, c++/58170, c++/58606, c++/58610, c++/58678, c++/58835,
	c++/58845, c++/58873, c++/59231, c++/59347, c++/60046, c++/60051,
	c++/60052, c++/60053, c++/60064, c++/60065, c++/60108, c++/60146,
	c++/60167, c++/60182, c++/60185, c++/60186, c++/60187, c++/60190,
	c++/60215, c++/60216, c++/60219, c++/60222, c++/60224, c++/60225,
	c++/60227, c++/60241, c++/60248, c++/60250, c++/60251, c++/60252,
	c++/60253, c++/60267, c++/60272, c++/60311, c++/60312, c++/60314,
	c++/60328, c++/60345, c++/60347, c++/60353, c++/60376, c++/60377,
	c++/60379, c++/60415, c++/60417, c/37743, c/60195, debug/56563,
	debug/57232, debug/59992, debug/60152, driver/60233, fortran/49397,
	fortran/55907, fortran/59599, fortran/60231, fortran/60232,
	fortran/60234, fortran/60236, fortran/60286, fortran/60302,
	fortran/60341, fortran/60359, ipa/55260, ipa/58555, ipa/60150,
	ipa/60243, ipa/60266, ipa/60306, ipa/60327, libfortran/58015,
	libfortran/59313, libfortran/60148, libgcc/60166, libgcj/55637,
	libjava/60261, libstdc++/58338, libstdc++/60308, lto/53808, lto/60179,
	lto/60295, lto/60319, lto/60404, lto/60405, middle-end/58477,
	middle-end/59223, middle-end/60147, middle-end/60175,
	middle-end/60221, middle-end/60291, objc++/60398, objc/56870,
	pch/60010, plugins/59335, preprocessor/58844, preprocessor/60400,
	rtl-optimization/49847, rtl-optimization/52714,
	rtl-optimization/58960, rtl-optimization/59535,
	rtl-optimization/60131, rtl-optimization/60268,
	rtl-optimization/60292, rtl-optimization/60317, sanitizer/60142,
	target/46898, target/55426, target/57896, target/57935, target/57936,
	target/58675, target/59222, target/59794, target/59799, target/60071,
	target/60169, target/60193, target/60203, target/60204, target/60205,
	target/60207, target/60280, target/60298, testsuite/60173,
	tree-optimization/56490, tree-optimization/58028,
	tree-optimization/60174, tree-optimization/60183,
	tree-optimization/60276, tree-optimization/60382
- configure with --enable-gnu-indirect-function on architectures
  and distros that support it and don't support it by default
  yet (#1067245)
- remove libgo P.224 elliptic curve (#1066539)

* Thu Feb 13 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.2
- update from the trunk
  - PRs bootstrap/59878, c++/60047, c/60101, debug/59776, fortran/52370,
	libffi/60073, lto/59468, lto/60060, middle-end/59737,
	middle-end/60092, rtl-optimization/60116, target/43546, target/49008,
	target/59927, target/60137, target/60151, testsuite/58630
- upgrade to newer cloog and isl

* Tue Feb 11 2014 Jakub Jelinek <jakub@redhat.com> 4.9.0-0.1
- new package
