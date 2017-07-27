%global DATE 20170727
%global SVNREV 250613
%global gcc_version 6.4.1
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 1
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64
%global build_ada 1
%else
%global build_ada 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 aarch64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 aarch64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64
%global build_libmpx 1
%else
%global build_libmpx 0
%endif
%global build_isl 1
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
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
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-6-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global isl_version 0.14
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
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
BuildRequires: python2-devel, python3-devel
%if %{build_go}
BuildRequires: hostname, procps
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
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
Requires: isl = %{isl_version}
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

Patch0: gcc6-hack.patch
Patch1: gcc6-java-nomulti.patch
Patch2: gcc6-ppc32-retaddr.patch
Patch3: gcc6-rh330771.patch
Patch4: gcc6-i386-libgomp.patch
Patch5: gcc6-sparc-config-detection.patch
Patch6: gcc6-libgomp-omp_h-multilib.patch
Patch7: gcc6-libtool-no-rpath.patch
Patch8: gcc6-isl-dl.patch
Patch9: gcc6-libstdc++-docs.patch
Patch10: gcc6-no-add-needed.patch
Patch11: gcc6-libgo-p224.patch
Patch12: gcc6-aarch64-async-unw-tables.patch
Patch13: gcc6-libsanitize-aarch64-va42.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
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
The gcc package contains the GNU Compiler Collection version 6.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 6 shared support library
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
Summary: GCC OpenMP v4.5 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package gdb-plugin
Summary: GCC plugin for GDB
Group: Development/Debuggers
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Group: System Environment/Libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
Group: Development/Libraries
BuildRequires: python-sphinx
Requires: libgccjit = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

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

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n libmpx-static
Summary: The Memory Protection Extensions static libraries
Group: Development/Libraries
Requires: libmpx = %{version}-%{release}

%description -n libmpx-static
This package contains the Memory Protection Extensions static runtime libraries.

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
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
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
   PATH=%{_builddir}/gcc-%{version}-%{DATE}/dwz-wrapper/:$PATH %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_dwz_opts} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
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
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch8 -p0 -b .isl-dl~
%endif
%if %{build_libstdcxx_docs}
%patch9 -p0 -b .libstdc++-docs~
%endif
%patch10 -p0 -b .no-add-needed~
%patch11 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch12 -p0 -b .aarch64-async-unw-tables~
%patch13 -p0 -b .libsanitize-aarch64-va42~

%if 0%{?_enable_debug_packages}
mkdir dwz-wrapper
if [ -f /usr/bin/dwz ]; then
cat > dwz-wrapper/dwz <<\EOF
#!/bin/bash
dwz_opts=
dwzm_opts=
dwz_files=
dwzm_files=
while [ $# -gt 0 ]; do
  case "$1" in
  -l|-L)
    dwz_opts="$dwz_opts $1 $2"; shift;;
  -m|-M)
    dwzm_opts="$dwzm_opts $1 $2"; shift;;
  -*)
    dwz_opts="$dwz_opts $1";;
  *)
    if [[ "$1" =~ (lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm|go\.so)|bin/gofmt.gcc.debug|bin/go.gcc.debug|/cgo.debug) ]]; then
      dwz_files="$dwz_files $1"
    else
      dwzm_files="$dwzm_files $1"
    fi;;
  esac
  shift
done
if [ -f /usr/bin/dwz ]; then
  /usr/bin/dwz $dwz_opts $dwz_files
  /usr/bin/dwz $dwz_opts $dwzm_opts $dwzm_files
fi
EOF
chmod 755 dwz-wrapper/dwz
fi
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)'`; do
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
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  cp -a "${BUILDDIR}"/debugfiles-base.list "${BUILDDIR}"/debugfiles-remove.list
%if %{build_go}
  libgoso=`basename .%{_prefix}/%{_lib}/libgo.so.9.*`
  for f in %{_prefix}/bin/go.gcc \
	   %{_prefix}/bin/gofmt.gcc \
	   %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cgo \
	   %{_prefix}/%{_lib}/$libgoso ; do
    eu-unstrip .$f usr/lib/debug$f.debug -o .$f.new
    chmod --reference=.$f .$f.new
    mv -f .$f.new .$f
    rm -f usr/lib/debug$f.debug
    echo "/usr/lib/debug$f.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  done
  rm -f usr/lib/debug%{_prefix}/%{_lib}/libgo.so.9.debug
  echo "/usr/lib/debug%{_prefix}/%{_lib}/libgo.so.9.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  for f in `find usr/lib/debug/.build-id -type l`; do
    if ls -l "$f" | egrep -q -- '->.*(/bin/go.gcc|/bin/gofmt.gcc|/cgo|lib[0-9]*/libgo\.so)'; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-remove.list
      rm -f "$f"
    fi
  done
%endif
  grep -v -f "${BUILDDIR}"/debugfiles-remove.list \
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

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

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

CC=gcc
CXX=g++
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
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      ../libgcc/Makefile.in
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
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch ppc64le %{mips}
	--disable-multilib \
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
	--disable-libgcj \
%if 0%{?fedora} >= 21 && 0%{?fedora} <= 22
	--with-default-libstdcxx-abi=gcc4-compatible \
%endif
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{build_libmpx}
	--enable-libmpx \
%else
	--disable-libmpx \
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
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
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
	--with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Werror=format-security / -Wformat -Werror=format-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,objc,obj-c++,fortran${enablelada}${enablelgo},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="`echo $OPT_FLAGS | sed 's/-Werror=format-security//'`" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/-Werror=format-security//'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{version}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

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
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}

for i in {gcc,gcc/cp,gcc/java,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}/ChangeLog*; do
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

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc
mkdir -p %{buildroot}%{_fmoddir}

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt
%endif

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

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
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
%if %{build_libcilkrts}
mv %{buildroot}%{_prefix}/%{_lib}/libcilkrts.spec $FULLPATH/
%endif
%if %{build_libmpx}
mv %{buildroot}%{_prefix}/%{_lib}/libmpx.spec $FULLPATH/
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
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
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
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_version}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__python3} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python3} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done

rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.4 libobjc.so
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.9.* libgo.so
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
ln -sf ../../../libasan.so.3.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../libmpx.so.2.* libmpx.so
ln -sf ../../../libmpxwrappers.so.2.* libmpxwrappers.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.9.* libgo.so
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
ln -sf ../../../../%{_lib}/libasan.so.3.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../../%{_lib}/libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../../%{_lib}/libmpx.so.2.* libmpx.so
ln -sf ../../../../%{_lib}/libmpxwrappers.so.2.* libmpxwrappers.so
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
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
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
%if %{build_libmpx}
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpx.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.*a $FULLLPATH/
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
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libnetgo.*a $FULLLPATH/
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
ln -sf ../../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-6.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-6.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-6.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-6.so
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
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.9.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.9.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
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
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.3.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.3.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
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
%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpxwrappers.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
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
%if %{build_libmpx}
ln -sf lib32/libmpx.a libmpx.a
ln -sf ../lib64/libmpx.a 64/libmpx.a
ln -sf lib32/libmpxwrappers.a libmpxwrappers.a
ln -sf ../lib64/libmpxwrappers.a 64/libmpxwrappers.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
ln -sf lib32/libnetgo.a libnetgo.a
ln -sf ../lib64/libnetgo.a 64/libnetgo.a
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
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.9.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.9.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
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
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.3.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.3.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
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
%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpxwrappers.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
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
%if %{build_libmpx}
ln -sf ../lib32/libmpx.a 32/libmpx.a
ln -sf lib64/libmpx.a libmpx.a
ln -sf ../lib32/libmpxwrappers.a 32/libmpxwrappers.a
ln -sf lib64/libmpxwrappers.a libmpxwrappers.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
ln -sf ../lib32/libnetgo.a 32/libnetgo.a
ln -sf lib64/libnetgo.a libnetgo.a
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
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++fs.a 32/libstdc++fs.a
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
%if %{build_libmpx}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmpx.a 32/libmpx.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmpxwrappers.a 32/libmpxwrappers.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgolibbegin.a 32/libgolibbegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libnetgo.a 32/libnetgo.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a -o -name libcilkrts.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libmpx.a -o -name libmpxwrappers.a \
		-o -name libnetgo.a -o -name libobjc.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcilkrts.a \
		    -o -name libmpx.a -o -name libmpxwrappers.a -o -name libcc1.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
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
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.3.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0.*
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5.*
%endif
%if %{build_libmpx}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpx.so.2.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.so.2.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.9.*
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

%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
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

%post gdb-plugin -p /sbin/ldconfig

%postun gdb-plugin -p /sbin/ldconfig

%post -n libgccjit -p /sbin/ldconfig

%postun -n libgccjit -p /sbin/ldconfig

%post -n libgccjit-devel
if [ -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%preun -n libgccjit-devel
if [ $1 = 0 -a -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

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

%post -n libmpx -p /sbin/ldconfig

%postun -n libmpx -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig

%postun -n libgo -p /sbin/ldconfig

%files -f %{name}.lang
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
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
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{version}
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/openacc.h
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pkuintrin.h
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vecintrin.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cilk
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.spec
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.spec
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
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpxwrappers.so
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
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpxwrappers.so
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
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.so
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
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.so
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%endif
%endif
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%dir %{_prefix}/share/gcc-%{gcc_version}
%dir %{_prefix}/share/gcc-%{gcc_version}/python
%{_prefix}/share/gcc-%{gcc_version}/python/libstdcxx

%files -n libstdc++-devel
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
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++fs.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++fs.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++fs.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
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
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
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
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*

%files gfortran
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/finclude
%endif
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran
%{_prefix}/%{_lib}/libgfortran.so.3*

%files -n libgfortran-static
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
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
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
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
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
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
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
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
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
%{_prefix}/%{_lib}/libasan.so.3*

%files -n libasan-static
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
%{_prefix}/%{_lib}/libubsan.so.0*

%files -n libubsan-static
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
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
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
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
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
%{_prefix}/%{_lib}/libcilkrts.so.5*

%files -n libcilkrts-static
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

%if %{build_libmpx}
%files -n libmpx
%{_prefix}/%{_lib}/libmpx.so.2*
%{_prefix}/%{_lib}/libmpxwrappers.so.2*

%files -n libmpx-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmpxwrappers.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmpxwrappers.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.a
%endif
%doc rpm.doc/changelogs/libmpx/ChangeLog*
%endif

%if %{build_go}
%files go
%ghost %{_prefix}/bin/go
%{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%ghost %{_prefix}/bin/gofmt
%{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/go1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cgo
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libnetgo.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libnetgo.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libnetgo.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%{_prefix}/%{_lib}/libgo.so.9*
%doc rpm.doc/libgo/*

%files -n libgo-devel
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libnetgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libnetgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libnetgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif

%files -n libgo-static
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

%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/libcc1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%changelog
* Thu Jul 27 2017 Jakub Jelinek <jakub@redhat.com> 6.4.1-1
- update from the 6 branch
  - GCC 6.4 release
  - PRs ada/79903, ada/79945, ada/80117, ada/80921, bootstrap/71510,
	c++/60992, c++/61636, c++/70844, c++/72775, c++/77563, c++/78282,
	c++/79050, c++/79264, c++/79461, c++/79508, c++/79512, c++/79519,
	c++/79548, c++/79566, c++/79572, c++/79580, c++/79607, c++/79639,
	c++/79640, c++/79641, c++/79664, c++/79681, c++/79687, c++/79796,
	c++/79896, c++/79900, c++/79962, c++/79984, c++/80043, c++/80091,
	c++/80129, c++/80141, c++/80150, c++/80176, c++/80179, c++/80241,
	c++/80244, c++/80267, c++/80294, c++/80297, c++/80363, c++/80973,
	c++/80984, c++/81011, c++/81130, c++/81154, c/79756, c/79940, c/80097,
	c/81006, debug/79255, debug/80025, debug/80321, driver/31468,
	driver/56469, fortran/65542, fortran/70601, fortran/71838,
	fortran/78331, fortran/78474, fortran/79434, fortran/79676,
	fortran/79894, fortran/80361, fortran/80392, fortran/80752,
	fortran/80904, fortran/80918, gcov-profile/53915, gcov-profile/78783,
	gcov-profile/80081, gcov-profile/80224, gcov-profile/80413, go/64238,
	ipa/65972, ipa/77333, ipa/79761, ipa/79849, ipa/79850, ipa/80104,
	ipa/80205, ipa/80212, ipa/80663, libgcc/80037, libgomp/80394,
	libgomp/80822, libstdc++/62045, libstdc++/67440, libstdc++/69699,
	libstdc++/71444, libstdc++/78236, libstdc++/79141, libstdc++/79511,
	libstdc++/79789, libstdc++/79980, libstdc++/80034, libstdc++/80041,
	libstdc++/80137, libstdc++/80316, libstdc++/80448, libstdc++/80493,
	libstdc++/80504, libstdc++/81002, lto/50345, lto/66295, lto/69953,
	lto/78049, lto/79579, lto/79587, lto/79760, lto/81487,
	middle-end/71310, middle-end/78339, middle-end/79396,
	middle-end/79536, middle-end/79537, middle-end/79576,
	middle-end/79753, middle-end/79831, middle-end/79931,
	middle-end/79971, middle-end/80004, middle-end/80075,
	middle-end/80171, middle-end/80222, middle-end/80281,
	middle-end/80341, middle-end/80362, middle-end/80539,
	middle-end/80692, middle-end/80809, middle-end/80853,
	middle-end/80902, middle-end/80929, other/80589, other/80909,
	plugin/80094, rtl-optimization/60818, rtl-optimization/73650,
	rtl-optimization/75964, rtl-optimization/79574,
	rtl-optimization/79577, rtl-optimization/79901,
	rtl-optimization/80112, rtl-optimization/80385,
	rtl-optimization/80429, rtl-optimization/80474,
	rtl-optimization/80501, sanitizer/70878, sanitizer/71458,
	sanitizer/78532, sanitizer/78992, sanitizer/79558, sanitizer/79562,
	sanitizer/79944, sanitizer/80067, sanitizer/80166, sanitizer/80168,
	sanitizer/80348, sanitizer/80349, sanitizer/80350, target/45053,
	target/49244, target/61729, target/65705, target/66669, target/67353,
	target/68163, target/68491, target/68972, target/69804, target/71294,
	target/71778, target/76731, target/77728, target/77850, target/78002,
	target/78543, target/79027, target/79155, target/79261, target/79439,
	target/79453, target/79494, target/79514, target/79544, target/79545,
	target/79559, target/79568, target/79570, target/79729, target/79733,
	target/79749, target/79752, target/79769, target/79770, target/79807,
	target/79883, target/79892, target/79906, target/79932, target/79947,
	target/79951, target/80019, target/80082, target/80090, target/80101,
	target/80103, target/80123, target/80246, target/80286, target/80298,
	target/80315, target/80376, target/80382, target/80462, target/80510,
	target/80569, target/80618, target/80718, target/80799, target/80966,
	target/80968, target/81300, target/81305, target/81375, target/81407,
	target/81471, testsuite/80092, testsuite/80678,
	tree-optimization/43434, tree-optimization/69264,
	tree-optimization/69823, tree-optimization/78644,
	tree-optimization/79256, tree-optimization/79552,
	tree-optimization/79631, tree-optimization/79666,
	tree-optimization/79732, tree-optimization/79803,
	tree-optimization/79977, tree-optimization/80113,
	tree-optimization/80122, tree-optimization/80167,
	tree-optimization/80170, tree-optimization/80181,
	tree-optimization/80218, tree-optimization/80262,
	tree-optimization/80275, tree-optimization/80334,
	tree-optimization/80426, tree-optimization/80453,
	tree-optimization/80492, tree-optimization/81162,
	tree-optimization/81192, tree-optimization/81555,
	tree-optimization/81556
  - fix _rdseed*_step and _rdrand*_step expansion (CVE-2017-11671, #1475735,
    PR target/80180)

* Thu Feb 16 2017 Jakub Jelinek <jakub@redhat.com> 6.3.1-3
- update from the 6 branch
  - PRs c++/77284, c++/77545, c++/78897, c++/78908, c++/79176, c++/79296,
	c++/79377, c++/79429, c/79428, c/79431, c/79471, fortran/70696,
	fortran/70697, fortran/79305, ipa/71207, ipa/79043, libstdc++/59161,
	libstdc++/59170, libstdc++/69301, libstdc++/69321, libstdc++/72792,
	libstdc++/72793, libstdc++/78134, libstdc++/78273, libstdc++/78346,
	libstdc++/78702, libstdc++/78979, libstdc++/79114, libstdc++/79195,
	libstdc++/79254, lto/69188, lto/79061, middle-end/61225,
	middle-end/78742, middle-end/79399, rtl-optimization/79121,
	target/65484, target/71017, target/77439, target/77455, target/78478,
	target/78862, target/78945, target/79079, target/79197, target/79268,
	target/79495, testsuite/70583, translation/79397,
	tree-optimization/71824, tree-optimization/72488,
	tree-optimization/77318, tree-optimization/79034,
	tree-optimization/79267, tree-optimization/79338,
	tree-optimization/79409, tree-optimization/79411

* Wed Jan 18 2017 Jakub Jelinek <jakub@redhat.com> 6.3.1-2
- update from the 6 branch
  - PRs c++/71182, c++/77812, c++/78341, c++/78693, c++/78949, debug/78839,
	driver/78863, fortran/78239, fortran/78866, libstdc++/78389,
	libstdc++/78956, libstdc++/78991, lto/79042, middle-end/50199,
	pch/78970, rtl-optimization/78255, rtl-optimization/78617,
	sanitizer/65479, target/70668, target/78041, target/78253,
	target/78900, target/79044, translation/78745, translation/78922,
	tree-optimization/71055, tree-optimization/78024,
	tree-optimization/78428, tree-optimization/78886

* Wed Dec 21 2016 Jakub Jelinek <jakub@redhat.com> 6.3.1-1
- update from the 6 branch
  - GCC 6.3 release
  - PRs bootstrap/77995, bootstrap/78188, c++/57728, c++/67631, c++/68377,
	c++/71274, c++/71515, c++/71848, c++/71912, c++/71979, c++/72808,
	c++/77285, c++/77375, c++/77467, c++/77482, c++/77591, c++/77637,
	c++/77638, c++/77722, c++/77739, c++/77748, c++/77804, c++/77907,
	c++/78039, c++/78089, c++/78252, c++/78550, c++/78551, c++/78649,
	c++/78701, c++/78761, c/71115, c/77450, c/77767, debug/77773,
	driver/78206, fortran/41922, fortran/58001, fortran/58991,
	fortran/58992, fortran/60774, fortran/61318, fortran/61420,
	fortran/66227, fortran/67219, fortran/69514, fortran/69544,
	fortran/69741, fortran/69867, fortran/69962, fortran/70006,
	fortran/71067, fortran/71730, fortran/71799, fortran/71859,
	fortran/71862, fortran/71891, fortran/71895, fortran/71902,
	fortran/72832, fortran/77260, fortran/77351, fortran/77372,
	fortran/77380, fortran/77391, fortran/77406, fortran/77420,
	fortran/77429, fortran/77460, fortran/77506, fortran/77507,
	fortran/77612, fortran/77665, fortran/77666, fortran/77694,
	fortran/77763, fortran/77915, fortran/77942, fortran/77973,
	fortran/77978, fortran/78013, fortran/78021, fortran/78092,
	fortran/78108, fortran/78123, fortran/78178, fortran/78221,
	fortran/78279, fortran/78297, fortran/78298, fortran/78299,
	fortran/78443, fortran/78500, fortran/78593, inline-asm/70184,
	ipa/77905, ipa/78309, libgcc/77519, libgcc/78064, libgfortran/77707,
	libgfortran/78123, libstdc++/51960, libstdc++/68323, libstdc++/70101,
	libstdc++/70564, libstdc++/70975, libstdc++/71337, libstdc++/72820,
	libstdc++/77288, libstdc++/77322, libstdc++/77459, libstdc++/77645,
	libstdc++/77686, libstdc++/77727, libstdc++/77794, libstdc++/77795,
	libstdc++/77801, libstdc++/77864, libstdc++/77987, libstdc++/77990,
	libstdc++/77994, libstdc++/78052, libstdc++/78111, libstdc++/78326,
	libstdc++/78465, libstdc++/78490, lto/78129, lto/78472,
	middle-end/67335, middle-end/69183, middle-end/71762,
	middle-end/72747, middle-end/77436, middle-end/77544,
	middle-end/77558, middle-end/77605, middle-end/77624,
	middle-end/77679, middle-end/78025, middle-end/78128,
	middle-end/78185, middle-end/78305, middle-end/78333,
	middle-end/78416, middle-end/78419, middle-end/78429,
	middle-end/78540, rtl-optimization/71496, rtl-optimization/71709,
	rtl-optimization/77309, rtl-optimization/77919,
	rtl-optimization/78038, rtl-optimization/78378,
	rtl-optimization/78546, sanitizer/66343, sanitizer/78294,
	target/48863, target/57438, target/59874, target/67710, target/71767,
	target/72717, target/72827, target/77326, target/77349, target/77483,
	target/77587, target/77621, target/77670, target/77756, target/77759,
	target/77822, target/77834, target/77874, target/77904, target/77933,
	target/77957, target/77991, target/78037, target/78057, target/78101,
	target/78166, target/78227, target/78229, target/78262, target/78310,
	target/78426, target/78796, testsuite/77411, tree-optimization/71575,
	tree-optimization/77478, tree-optimization/77514,
	tree-optimization/77550, tree-optimization/77621,
	tree-optimization/77646, tree-optimization/77648,
	tree-optimization/77673, tree-optimization/77745,
	tree-optimization/77768, tree-optimization/77839,
	tree-optimization/77855, tree-optimization/77879,
	tree-optimization/77916, tree-optimization/77937,
	tree-optimization/77943, tree-optimization/78047,
	tree-optimization/78189, tree-optimization/78224,
	tree-optimization/78228, tree-optimization/78482,
	tree-optimization/78542, tree-optimization/78646,
	tree-optimization/78731
  - remove pcommitintrin.h header

* Fri Sep 16 2016 Jakub Jelinek <jakub@redhat.com> 6.2.1-2
- update from the 6 branch
  - PRs c++/77427, c++/77539, c++/77553, debug/57519, fortran/77500,
	fortran/77516, middle-end/77594, rtl-optimization/77452,
	sanitizer/68260, sanitizer/77396, target/69255

* Thu Sep  1 2016 Jakub Jelinek <jakub@redhat.com> 6.2.1-1
- update from the 6 branch
  - GCC 6.2 release
  - PRs bootstrap/77279, debug/77363, fortran/69281, fortran/71014,
	fortran/72744, fortran/77352, fortran/77358, fortran/77374,
	libstdc++/77334, libstdc++/77395, lto/70955, middle-end/70895,
	middle-end/71700, middle-end/77377, target/71338, target/71910,
	target/72863, target/72867, target/77270, target/77281, target/77403,
	tree-optimization/62171, tree-optimization/68542,
	tree-optimization/71077, tree-optimization/72851,
	tree-optimization/72866, tree-optimization/76490,
	tree-optimization/76783

* Wed Aug 17 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-6
- update from the 6 branch
  - PRs c++/71972, c++/72868, c++/73456, c/67410, c/71512, c/72816,
	debug/71906, driver/72765, fortran/71123, fortran/71936,
	fortran/72698, libgfortran/71123, libgfortran/73142, sanitizer/71042,
	target/72819, target/72843, target/72853, target/76342,
	testsuite/77034, tree-optimization/71083, tree-optimization/73434
- fix devirtualization ICE (#1367212, PR middle-end/77259)
- build python3 bytecode manually to avoid python3-devel bugs (#1204355,
  #1366516)

* Wed Aug 10 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-5
- update from the 6 branch
  - PRs c++/52746, c++/55922, c++/63151, c++/68724, c++/69223, c++/70709,
	c++/70778, c++/71350, c++/71576, c++/71630, c++/71728, c++/71738,
	c++/71748, c++/71833, c++/71913, c++/72415, c++/72457, c++/72800,
	c/7652, fortran/70040, fortran/70524, fortran/70842, fortran/71795,
	fortran/71807, fortran/71883, ipa/68273, ipa/71981, libstdc++/70940,
	libstdc++/71964, rtl-optimization/71976, sanitizer/71953,
	target/70677, target/71151, target/71216, target/71869, target/72103,
	target/72767, target/72802, target/72805, tree-optimization/71881,
	tree-optimization/72824
- add python3 bytecode for libstdc++ gdb extensions (#1204355)

* Thu Jul 21 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-4
- update from the 6 branch
  - PRs c++/54430, c++/67565, c++/67579, c++/70781, c++/70822, c++/70824,
	c++/70869, c++/71054, c++/71092, c++/71117, c++/71214, c++/71495,
	c++/71511, c++/71513, c++/71604, c++/71711, c++/71718, c++/71739,
	c++/71814, c++/71822, c++/71828, c++/71835, c++/71843, c++/71871,
	c++/71896, c++/71909, c++/71941, c/71685, debug/71855, driver/71651,
	fortran/70673, fortran/71623, fortran/71687, fortran/71688,
	fortran/71704, fortran/71705, fortran/71717, fortran/71764,
	fortran/71783, ipa/71624, libstdc++/71313, libstdc++/71320,
	libstdc++/71856, middle-end/64516, middle-end/71423, middle-end/71606,
	middle-end/71626, middle-end/71693, middle-end/71758,
	middle-end/71874, rtl-optimization/71634, rtl-optimization/71916,
	target/30417, target/50739, target/71493, target/71656, target/71670,
	target/71698, target/71720, target/71733, target/71763, target/71805,
	target/71806, tree-optimization/71264, tree-optimization/71452,
	tree-optimization/71518, tree-optimization/71521,
	tree-optimization/71522, tree-optimization/71647,
	tree-optimization/71823

* Tue Jun 21 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-3
- update from the 6 branch
  - PRs ada/71317, ada/71358, bootstrap/71071, c++/60095, c++/69515,
	c++/69872, c++/70466, c++/70498, c++/70572, c++/70584, c++/70735,
	c++/70847, c++/70972, c++/71100, c++/71105, c++/71147, c++/71166,
	c++/71173, c++/71184, c++/71210, c++/71227, c++/71257, c++/71306,
	c++/71330, c++/71349, c++/71372, c++/71393, c++/71442, c++/71448,
	c++/71516, c++/71528, c/68657, c/71171, c/71381, debug/71057,
	fortran/56226, fortran/60751, fortran/66461, fortran/69603,
	fortran/69659, fortran/70855, fortran/70856, fortran/71047,
	fortran/71156, fortran/71204, hsa/70857, ipa/70646, ipa/70760,
	libffi/65567, libgcc/70720, libgfortran/68115, libstdc++/69703,
	libstdc++/70609, libstdc++/70762, libstdc++/71004, libstdc++/71005,
	libstdc++/71036, libstdc++/71037, libstdc++/71038, libstdc++/71049,
	libstdc++/71545, middle-end/70877, middle-end/70931, middle-end/70941,
	middle-end/71002, middle-end/71279, middle-end/71371,
	middle-end/71373, middle-end/71387, middle-end/71494,
	middle-end/71529, middle-end/71581, sanitizer/71160, sanitizer/71498,
	target/60751, target/67310, target/70809, target/70830, target/70860,
	target/70915, target/70947, target/70957, target/70963, target/71056,
	target/71103, target/71145, target/71161, target/71186, target/71201,
	target/71379, target/71389, target/71554, tree-optimization/69067,
	tree-optimization/69068, tree-optimization/70876,
	tree-optimization/70884, tree-optimization/71006,
	tree-optimization/71031, tree-optimization/71259,
	tree-optimization/71405, tree-optimization/71505,
	tree-optimization/71588
- fix AVX512F floating point vector comparison handling (PR target/71559)

* Tue May 10 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-2
- update from the 6 branch
  - PRs ada/70759, ada/70786, ada/70900, ada/70969, c++/70540, debug/70935,
	java/70839, middle-end/70626, sanitizer/70342, sanitizer/70875,
	target/60290, target/70858, tree-optimization/70916,
	tree-optimization/70956
- don't own %{_prefix}/libexec/getconf directory, as glibc owns it (#1333616)

* Wed Apr 27 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-1
- update from the trunk and 6 branch
  - GCC 6.1 release
  - PRs bootstrap/70704, c++/66543, c++/68206, c++/68530, c++/68722,
	c++/69066, c++/69517, c++/69687, c++/70019, c++/70029, c++/70492,
	c++/70494, c++/70501, c++/70505, c++/70522, c++/70528, c++/70543,
	c++/70571, c++/70588, c++/70590, c++/70594, c++/70610, c++/70615,
	c++/70622, c++/70627, c++/70634, c++/70635, c++/70639, c++/70641,
	c++/70648, c++/70675, c++/70685, c++/70690, c/70436, c/70651, c/70671,
	debug/70628, fortran/58000, fortran/67039, fortran/68566,
	fortran/70592, ipa/70348, ipa/70785, libgfortran/70684, lto/70289,
	middle-end/70533, middle-end/70534, middle-end/70535,
	middle-end/70593, middle-end/70633, middle-end/70643,
	middle-end/70680, middle-end/70747, preprocessor/61817,
	preprocessor/69391, preprocessor/69650, rtl-optimization/64886,
	rtl-optimization/66669, rtl-optimization/68749,
	rtl-optimization/70398, rtl-optimization/70574,
	rtl-optimization/70596, rtl-optimization/70681, sanitizer/70541,
	sanitizer/70573, sanitizer/70624, sanitizer/70712, target/64971,
	target/70117, target/70133, target/70566, target/70630, target/70640,
	target/70662, target/70669, target/70674, target/70711, target/70728,
	target/70750, testsuite/64039, testsuite/68242, testsuite/70553,
	testsuite/70581, tree-optimization/68644, tree-optimization/68756,
	tree-optimization/68953, tree-optimization/70130,
	tree-optimization/70373, tree-optimization/70586,
	tree-optimization/70602, tree-optimization/70614,
	tree-optimization/70623, tree-optimization/70724,
	tree-optimization/70725, tree-optimization/70726,
	tree-optimization/70780

* Wed Apr  6 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.20
- update from the trunk
  - PRs bootstrap/70173, c++/67376, c++/67394, c++/68475, c++/70170,
	c++/70172, c++/70228, c++/70336, c++/70393, c++/70449, c++/70452,
	c++/70481, c++/70488, c++/70512, c/70297, c/70307, fortran/65795,
	fortran/67538, hsa/70391, hsa/70399, hsa/70402, ipa/66223, ipa/68881,
	libstdc++/70437, libstdc++/70503, libstdc++/70554, middle-end/70307,
	middle-end/70457, middle-end/70499, middle-end/70550,
	rtl-optimization/70461, rtl-optimization/70467,
	rtl-optimization/70484, rtl-optimization/70542, target/67172,
	target/67391, target/69890, target/70292, target/70416, target/70439,
	target/70442, target/70453, target/70496, target/70510, target/70525,
	testsuite/70364, tree-optimization/70509, tree-optimization/70526
- include unstripped *.a libraries in gcc-debuginfo package

* Wed Apr  6 2016 Michal Toman <mtoman@fedoraproject.org>
- add support for MIPS

* Thu Mar 31 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.19
- update from the trunk
  - PRs c++/62212, c++/64266, c++/69315, c++/69884, c++/70323, c++/70332,
	c++/70344, c++/70347, c++/70353, c++/70376, c++/70386, c++/70422,
	c++/70430, fortran/70397, ipa/12392, ipa/70283, ipa/70366,
	libgfortran/70235, libgomp/69414, libstdc++/69945, lto/69650,
	middle-end/69845, middle-end/70355, middle-end/70370,
	middle-end/70424, middle-end/70450, rtl-optimization/68695,
	rtl-optimization/70429, rtl-optimization/70460, target/63890,
	target/69917, target/70052, target/70120, target/70290, target/70319,
	target/70381, target/70406, target/70421, testsuite/64177,
	testsuite/70356, tree-optimization/59124, tree-optimization/69042,
	tree-optimization/70372, tree-optimization/70396,
	tree-optimization/70405
- fix s390x ICE (PR target/70404)

* Wed Mar 23 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.18
- update from the trunk
  - PRs bootstrap/69513, c++/53792, c++/58281, c++/70095, c++/70096,
	c++/70106, c++/70139, c++/70141, c++/70144, c++/70147, c++/70194,
	c++/70204, c++/70205, c++/70209, c++/70218, c++/70259, c++/70267,
	c++/70272, c++/70273, c++/70285, c++/70295, c/69407, c/69993, c/70093,
	c/70264, c/70280, c/70281, debug/70271, driver/70132, driver/70192,
	fortran/45076, fortran/69043, fortran/69520, fortran/69524,
	fortran/70031, hsa/70234, hsa/70337, ipa/70161, ipa/70269, ipa/70306,
	libfortran/69799, libgcc/70363, lto/70187, lto/70258,
	middle-end/68215, middle-end/70199, middle-end/70219,
	middle-end/70239, middle-end/70240, middle-end/70251,
	middle-end/70326, middle-end/70333, rtl-optimization/63384,
	rtl-optimization/69032, rtl-optimization/69102,
	rtl-optimization/69307, rtl-optimization/70222,
	rtl-optimization/70224, rtl-optimization/70263,
	rtl-optimization/70278, target/38239, target/64411, target/66660,
	target/69614, target/70048, target/70083, target/70098, target/70123,
	target/70131, target/70162, target/70188, target/70232, target/70245,
	target/70261, target/70293, target/70296, target/70300, target/70302,
	target/70321, target/70325, target/70327, target/70329,
	tree-optimization/56365, tree-optimization/64058,
	tree-optimization/68714, tree-optimization/68715,
	tree-optimization/68809, tree-optimization/70045,
	tree-optimization/70190, tree-optimization/70252,
	tree-optimization/70288, tree-optimization/70310,
	tree-optimization/70317, tree-optimization/70354

* Fri Mar 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 6.0.0-0.17
- enable gnat on ppc64le

* Fri Mar 11 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.16
- update from the trunk
  - PRs c++/62096, c++/70001, c++/70105, c++/70135, c++/70153, c/68473,
	c/70085, c/70143, lto/69589, middle-end/69916, rtl-opt/70061,
	rtl-optimization/19705, rtl-optimization/47992,
	rtl-optimization/69195, rtl-optimization/70174, target/62281,
	target/70002, target/70044, target/70049, target/70064, target/70086,
	target/70110, target/70113, target/70160, target/70168,
	testsuite/68915, testsuite/70009, testsuite/70109,
	tree-optimization/70013, tree-optimization/70115,
	tree-optimization/70116, tree-optimization/70127,
	tree-optimization/70128, tree-optimization/70138,
	tree-optimization/70152, tree-optimization/70169,
	tree-optimization/70177

* Sat Mar  5 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.15
- update from the trunk
  - PRs c++/51406, c++/66786, c++/67164, c++/69203, c++/70035, c++/70054,
	c++/70067, c++/70084, c/67854, c/68187, c/69798, c/69824, c/69973,
	ipa/69990, libffi/70024, libgomp/69555, middle-end/67278,
	middle-end/70050, rtl-opt/67145, rtl-optimization/57676,
	rtl-optimization/69052, rtl-optimization/69904,
	rtl-optimization/69941, rtl-optimization/69942, target/67278,
	target/70004, target/70014, target/70021, target/70028, target/70059,
	target/70062, testsuite/69766, tree-optimization/55936,
	tree-optimization/68659, tree-optimization/70043

* Wed Mar  2 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.14
- update from the trunk
  - PRs ada/70017, c++/51489, c++/69795, c++/69961, c++/69995, c++/70036,
	c/69796, c/69974, fortran/47674, fortran/56007, fortran/60126,
	fortran/68147, fortran/69910, middle-end/70022, middle-end/70025,
	preprocessor/69985, rtl-optimization/70007, target/69706,
	target/70011, target/70027, target/70033, tree-optimization/68621,
	tree-optimization/69720, tree-optimization/69956,
	tree-optimization/69980, tree-optimization/69983,
	tree-optimization/69987, tree-optimization/69989,
	tree-optimization/69994, tree-optimization/69999,
	tree-optimization/70005

* Sat Feb 27 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.13
- update from the trunk
  - PRs c++/15766, c++/67364, c++/68049, c++/69323, c++/69736, c++/69743,
	c++/69826, c++/69865, c++/69889, c++/69902, c++/69912, c++/69922,
	c++/69958, c/28901, c/51147, c/69759, c/69819, c/69900, c/69911,
	c/69918, debug/61033, debug/69705, driver/68463, driver/69805,
	fortran/52531, fortran/57365, fortran/61156, fortran/69423, hsa/69568,
	ipa/37448, ipa/69630, libgfortran/69456, libstdc++/69881,
	libstdc++/69893, libstdc++/69939, middle-end/68963, middle-end/69760,
	middle-end/69780, middle-end/69909, middle-end/69915,
	middle-end/69919, middle-end/69920, objc/69844, preprocessor/69558,
	rtl-optimization/69886, rtl-optimization/69891,
	rtl-optimization/69896, target/54089, target/61397, target/69613,
	target/69709, target/69806, target/69810, target/69875, target/69885,
	target/69888, target/69894, target/69895, target/69946, target/69969,
	tree-optimization/15826, tree-optimization/48795,
	tree-optimization/69551, tree-optimization/69666,
	tree-optimization/69740, tree-optimization/69882,
	tree-optimization/69907
- make sure DW_TAG_dwarf_procedure referenced from DW_OP_GNU_implicit_pointer
  is not pruned as "unused" (PR debug/69947)

* Fri Feb 19 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.12
- update from the trunk
  - PRs bootstrap/69816, c++/65985, c++/67767, c++/68585, c++/68679,
	c++/68890, c++/69753, c++/69797, c++/69842, c++/69850, c++/69851,
	c/64748, c/69835, driver/69265, driver/69453, driver/69779,
	fortran/60526, fortran/68746, fortran/69742, libgfortran/69651,
	libgfortran/69668, libstdc++/69794, lto/67709, lto/69655,
	middle-end/69553, middle-end/69801, middle-end/69838,
	middle-end/69854, other/69554, rtl-optimization/69609,
	rtl-optimization/69648, rtl-optimization/69752,
	rtl-optimization/69764, rtl-optimization/69771, sanitizer/69863,
	target/48344, target/62254, target/64345, target/67260, target/67636,
	target/68973, target/69161, target/69532, target/69610, target/69671,
	target/69729, target/69820, testsuite/68580, testsuite/68886,
	testsuite/69573, testsuite/69586, tree-optimization/69586,
	tree-optimization/69714, tree-optimization/69776,
	tree-optimization/69783, tree-optimization/69802,
	tree-optimization/69820
- enable Ada on s390x

* Fri Feb 12 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.11
- update from the trunk
  - PRs c++/10200, c++/59627, c++/67835, c++/68726, c++/68926, c++/69098,
	c++/69139, c++/69283, c++/69631, c++/69657, c++/69662, c++/69688,
	c/69522, c/69643, c/69768, fortran/50555, fortran/66089,
	fortran/69296, go/68562, ipa/69239, libstdc++/48891, lto/69707,
	middle-end/66726, other/69722, plugins/69758, preprocessor/69664,
	rtl-optimization/68730, rtl-optimization/69291,
	rtl-optimization/69737, target/60410, target/65313, target/65867,
	target/68273, target/68404, target/68532, target/69148, target/69634,
	target/69713, tree-opt/69282, tree-optimization/65917,
	tree-optimization/68021, tree-optimization/68541,
	tree-optimization/69209, tree-optimization/69599,
	tree-optimization/69652, tree-optimization/69715,
	tree-optimization/69719, tree-optimization/69726
- temporarily revert PR c++/10200 fix
- fix -fpartial-inlining with clobber or debug stmts in return_bb
  (PR ipa/68672)

* Fri Feb  5 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.10
- update from the trunk
  - PRs bootstrap/69611, bootstrap/69677, c++/68948, c++/69056, c++/69251,
	c++/69253, c++/69277, c++/69290, c++/69349, c/69627, c/69669,
	fortran/67451, fortran/69368, fortran/69418, libstdc++/69626,
	middle-end/68542, rtl-opt/67609, rtl-optimization/64682,
	rtl-optimization/69567, rtl-optimization/69577, sanitizer/69276,
	target/65932, target/67032, target/67714, target/68124, target/68662,
	target/69118, target/69369, target/69454, target/69461, target/69548,
	target/69619, target/69625, target/69644, target/69667, target/69677,
	testsuite/65940, tree-optimization/69580, tree-optimization/69595,
	tree-optimization/69606
  - Go 1.6rc1
- fix various C++ ICEs in assign_temp (PR ipa/69241, PR c++/69649)
- fix character constant error recovery (PR c++/69628)
- fix invalid diagnostics on C++ array initializers (PR c++/69658)
- fix RA subreg handling (PR rtl-optimization/69691)
- fix up 435.gromacs performance regression (PR rtl-optimization/69274)

* Mon Feb  1 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.9
- update from the trunk
  - PRs middle-end/69556, tree-optimization/67921, tree-optimization/69574
- fix compile time and memory hog in combiner (PR rtl-optimization/69592)

* Mon Feb  1 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.8
- update from the trunk
  - PRs c++/68490, c++/68763, c++/69009, debug/68244, fortran/66707,
	fortran/67564, fortran/69566, libstdc++/69581, rtl-opt/69535,
	rtl-optimization/69570, target/65546, target/68741, testsuite/69584,
	tree-optimization/69579

* Fri Jan 29 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.7
- update from the trunk
  - PRs c++/69462, c++/69509, c++/69516, debug/69518, libstdc++/69506,
	middle-end/69537, other/69006, pch/68176, target/17381, target/65604,
	target/66137, target/68400, target/69299, target/69459, target/69530,
	target/69551, tree-optimization/69378, tree-optimization/69547
- buildrequire procps for go testing
- fix __uint128_t division (PR tree-optimization/69546)
- restore old behavior of _Pragma GCC diagnostics in macros
  (PR preprocessor/69543, PR c/69558)

* Thu Jan 28 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.6
- update from the trunk
  - PRs ada/69488, c++/24208, c++/67407, c++/69317, c++/69379, c++/69496,
	c/68062, cilkplus/69267, debug/66869, fortran/62536, fortran/69422,
	fortran/69484, libstdc++/69295, libstdc++/69450, lto/69254,
	middle-end/69542, pch/68758, preprocessor/69126, rtl-opt/69447,
	target/63679, target/68380, target/68986, target/69245, target/69305,
	target/69512, tree-optimization/68398, tree-optimization/69166,
	tree-optimization/69196, tree-optimization/69355,
	tree-optimization/69466
- temporarily revert _Pragma location fix (PR preprocessor/69126)
- fix up -Wunused-function for C++ (PR debug/66869)

* Wed Jan 27 2016 Jakub Jelinek <jakub@redhat.com> 6.0.0-0.5
- new package
