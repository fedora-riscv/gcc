%global DATE 20231113
%global gitrev 4292c70489195b52615f16679dc6df18cd1c8432
%global gcc_version 13.2.1
%global gcc_major 13
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 5
%global nvptx_tools_gitrev aa3404ad5a496cda5d79a50bedb1344fd63e8763
%global newlib_cygwin_gitrev 9e09d6ed83cce4777a5950412647ccc603040409
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build
%undefine _auto_set_build_flags
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
# Until annobin is fixed (#1519165).
%undefine _annotated_build
%endif
# Strip will fail on nvptx-none *.a archives and the brp-* scripts will
# fail randomly depending on what is stripped last.
%if 0%{?__brp_strip_static_archive:1}
%global __brp_strip_static_archive %{__brp_strip_static_archive} || :
%endif
%if 0%{?__brp_strip_lto:1}
%global __brp_strip_lto %{__brp_strip_lto} || :
%endif
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%else
%global multilib_64_archs sparc64 ppc64 ppc64p7 x86_64
%endif
%if 0%{?rhel} > 7
%global build_ada 0
%global build_objc 0
%global build_go 0
%global build_d 0
%global build_m2 0
%else
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64 riscv64
%global build_ada 1
%else
%global build_ada 0
%endif
%global build_objc 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 %{arm} aarch64 %{mips} s390 s390x riscv64
%global build_d 1
%else
%global build_d 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_m2 1
%else
%global build_m2 0
%endif
%endif
%ifarch %{ix86} x86_64 ia64 ppc64le
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 aarch64
%global build_libhwasan 1
%else
%global build_libhwasan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64 s390x
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64 s390x
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%if 0%{?rhel} > 8
%global build_isl 0
%else
%global build_isl 1
%endif
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch x86_64 ppc64le
%global build_offload_nvptx 1
%else
%global build_offload_nvptx 0
%endif
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%ifarch s390x
%global multilib_32_arch s390
%endif
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
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 10
%global build_annobin_plugin 1
%else
%global build_annobin_plugin 0
%endif
Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
# The source for this package was pulled from upstream's vcs.
# %%{gitrev} is some commit from the
# https://gcc.gnu.org/git/?p=gcc.git;h=refs/vendors/redhat/heads/gcc-%%{gcc_major}-branch
# branch.  Use the following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
Source0: gcc-%{version}-%{DATE}.tar.xz
# The source for nvptx-tools package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://github.com/MentorEmbedded/nvptx-tools.git nvptx-tools-dir.tmp
# git --git-dir=nvptx-tools-dir.tmp/.git fetch --depth 1 origin %%{nvptx_tools_gitrev}
# git --git-dir=nvptx-tools-dir.tmp/.git archive --prefix=nvptx-tools-%%{nvptx_tools_gitrev}/ %%{nvptx_tools_gitrev} | xz -9e > nvptx-tools-%%{nvptx_tools_gitrev}.tar.xz
# rm -rf nvptx-tools-dir.tmp
Source1: nvptx-tools-%{nvptx_tools_gitrev}.tar.xz
# The source for nvptx-newlib package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone git://sourceware.org/git/newlib-cygwin.git newlib-cygwin-dir.tmp
# git --git-dir=newlib-cygwin-dir.tmp/.git archive --prefix=newlib-cygwin-%%{newlib_cygwin_gitrev}/ %%{newlib_cygwin_gitrev} ":(exclude)newlib/libc/sys/linux/include/rpc/*.[hx]" | xz -9e > newlib-cygwin-%%{newlib_cygwin_gitrev}.tar.xz
# rm -rf newlib-cygwin-dir.tmp
Source2: newlib-cygwin-%{newlib_cygwin_gitrev}.tar.xz
%global isl_version 0.24
Source3: https://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
URL: http://gcc.gnu.org
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %%gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
# Need binutils which support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
BuildRequires: binutils >= 2.31
%else
BuildRequires: binutils >= 2.24
%endif
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1
BuildRequires: python3-devel, /usr/bin/python
BuildRequires: gcc, gcc-c++, make
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
BuildRequires: libzstd-devel
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
%if %{build_d}
# D requires D to build
BuildRequires: gcc-gdc >= 11.0.0, libgphobos-static >= 11.0.0
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
# Need binutils that support %%gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
# Need binutils that support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
Requires: binutils >= 2.31
%else
Requires: binutils >= 2.24
%endif
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
# lto-wrapper invokes make
Requires: make
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
AutoReq: true
Provides: bundled(libiberty)
Provides: bundled(libbacktrace)
Provides: bundled(libffi)
Provides: gcc(major) = %{gcc_major}

Patch0: gcc13-hack.patch
Patch2: gcc13-sparc-config-detection.patch
Patch3: gcc13-libgomp-omp_h-multilib.patch
Patch4: gcc13-libtool-no-rpath.patch
Patch5: gcc13-isl-dl.patch
Patch6: gcc13-isl-dl2.patch
Patch7: gcc13-libstdc++-docs.patch
Patch8: gcc13-no-add-needed.patch
Patch9: gcc13-Wno-format-security.patch
Patch10: gcc13-rh1574936.patch
Patch11: gcc13-d-shared-libphobos.patch
Patch12: gcc13-pr110792.patch

Patch50: isl-rh2155127.patch

Patch100: gcc13-fortran-fdec-duplicates.patch

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

%if %{build_go}
# Avoid stripping these libraries and binaries.
%global __os_install_post \
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.22.* \
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%__os_install_post \
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.22.* \
chmod 755 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 755 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%{nil}
%endif

%description
The gcc package contains the GNU Compiler Collection version 13.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 13 shared support library
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
%ifarch %{ix86} x86_64
Obsoletes: libcilkrts
Obsoletes: libcilkrts-static
Obsoletes: libmpx
Obsoletes: libmpx-static
%endif

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Provides: gcc-g++ = %{version}-%{release}
Provides: g++ = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Autoreq: true
Requires: glibc >= 2.10.90-7
BuildRequires: tzdata >= 2017c
%if 0%{?fedora} > 38 || 0%{?rhel} > 9
Recommends: tzdata >= 2017c
%else
Requires: tzdata >= 2017c
%endif

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
Provides: gcc-fortran = %{version}-%{release}
Provides: gfortran = %{version}-%{release}
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Autoreq: true
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.

%package gdc
Summary: D support
Requires: gcc = %{version}-%{release}
Requires: libgphobos = %{version}-%{release}
Provides: gcc-d = %{version}-%{release}
Provides: gdc = %{version}-%{release}
Autoreq: true

%description gdc
The gcc-gdc package provides support for compiling D
programs with the GNU Compiler Collection.

%package -n libgphobos
Summary: D runtime
Autoreq: true

%description -n libgphobos
This package contains D shared library which is needed to run
D dynamically linked programs.

%package -n libgphobos-static
Summary: Static D libraries
Requires: libgphobos = %{version}-%{release}
Requires: gcc-gdc = %{version}-%{release}

%description -n libgphobos-static
This package contains static D libraries.

%package gm2
Summary: Modula-2 support
Requires: gcc = %{version}-%{release}
Requires: libgm2 = %{version}-%{release}
Provides: gcc-m2 = %{version}-%{release}
Provides: gm2 = %{version}-%{release}
Autoreq: true

%description gm2
The gcc-gm2 package provides support for compiling Modula-2
programs with the GNU Compiler Collection.

%package -n libgm2
Summary: Modula-2 runtime
Autoreq: true

%description -n libgm2
This package contains Modula-2 shared libraries which are needed to run
Modula-2 dynamically linked programs.

%package -n libgm2-static
Summary: Static Modula-2 libraries
Requires: libgm2 = %{version}-%{release}
Requires: gcc-gm2 = %{version}-%{release}

%description -n libgm2-static
This package contains static Modula-2 libraries.

%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package -n libgomp-offload-nvptx
Summary: GCC OpenMP v4.5 plugin for offloading to NVPTX
Requires: libgomp = %{version}-%{release}

%description -n libgomp-offload-nvptx
This package contains libgomp plugin for offloading to NVidia
PTX.  The plugin needs libcuda.so.1 shared library that has to be
installed separately.

%package gdb-plugin
Summary: GCC plugin for GDB
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: python3-sphinx
%else
BuildRequires: python-sphinx
%endif
Requires: libgccjit = %{version}-%{release}

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

%package -n libquadmath
Summary: GCC __float128 shared support library

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libhwasan
Summary: The Hardware-assisted Address Sanitizer runtime library

%description -n libhwasan
This package contains the Hardware-assisted Address Sanitizer library
which is used for -fsanitize=hwaddress instrumented programs.

%package -n libhwasan-static
Summary: The Hardware-assisted Address Sanitizer static library
Requires: libhwasan = %{version}-%{release}

%description -n libhwasan-static
This package contains Hardware-assisted Address Sanitizer static runtime
library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.

%package -n cpp
Summary: The C Preprocessor
Requires: filesystem >= 3
Provides: /lib/cpp
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
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Autoreq: true

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.

%package go
Summary: Go support
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides: gccgo = %{version}-%{release}
Autoreq: true

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Requires: libgo = %{version}-%{release}
Autoreq: true

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package offload-nvptx
Summary: Offloading compiler to NVPTX
Requires: gcc = %{version}-%{release}
Requires: libgomp-offload-nvptx = %{version}-%{release}

%description offload-nvptx
The gcc-offload-nvptx package provides offloading support for
NVidia PTX.  OpenMP and OpenACC programs linked with -fopenmp will
by default add PTX code into the binaries, which can be offloaded
to NVidia PTX capable devices if available.

%package plugin-annobin
Summary: The annobin plugin for gcc, built by the installed version of gcc
Requires: gcc = %{version}-%{release}
%if %{build_annobin_plugin}
BuildRequires: annobin-plugin-gcc >= 10.62, rpm-devel, binutils-devel, xz
%endif

%description plugin-annobin
This package adds a version of the annobin plugin for gcc.  This version
of the plugin is explicitly built by the same version of gcc that is installed
so that there cannot be any synchronization problems.

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3
%patch -P0 -p0 -b .hack~
%patch -P2 -p0 -b .sparc-config-detection~
%patch -P3 -p0 -b .libgomp-omp_h-multilib~
%patch -P4 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch -P5 -p0 -b .isl-dl~
%patch -P6 -p0 -b .isl-dl2~
%endif
%if %{build_libstdcxx_docs}
%patch -P7 -p0 -b .libstdc++-docs~
%endif
%patch -P8 -p0 -b .no-add-needed~
%patch -P9 -p0 -b .Wno-format-security~
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
%patch -P10 -p0 -b .rh1574936~
%endif
%patch -P11 -p0 -b .d-shared-libphobos~
%patch -P12 -p0 -b .pr110792~

%patch -P50 -p0 -b .rh2155127~
touch -r isl-0.24/m4/ax_prog_cxx_for_build.m4 isl-0.24/m4/ax_prog_cc_for_build.m4

%if 0%{?rhel} >= 9
%patch -P100 -p1 -b .fortran-fdec-duplicates~
%endif

%ifarch %{arm}
rm -f gcc/testsuite/go.test/test/fixedbugs/issue19182.go
%endif
rm -f libphobos/testsuite/libphobos.gc/forkgc2.d
#rm -rf libphobos/testsuite/libphobos.gc

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt
sed -i -e 's/context->report_bug = false;/context->report_bug = true;/' gcc/diagnostic.cc

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

CC=gcc
CXX=g++
OPT_FLAGS="%{optflags}"
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=[123]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[123]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/\(-Wp,\)\?-U_FORTIFY_SOURCE//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-flto=auto//g;s/-flto//g;s/-ffat-lto-objects//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fno-omit-frame-pointer//g;s/-mbackchain//g;s/-mno-omit-leaf-frame-pointer//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
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
      libgcc/Makefile.in
    ;;
esac

%if %{build_offload_nvptx}
mkdir obji
IROOT=`pwd`/obji
cd nvptx-tools-%{nvptx_tools_gitrev}
rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC="$CC" CXX="$CXX" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
../configure --prefix=%{_prefix}
make %{?_smp_mflags}
make install prefix=${IROOT}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
rm -rf obj-offload-nvptx-none
mkdir obj-offload-nvptx-none

cd obj-offload-nvptx-none
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --disable-bootstrap --disable-sjlj-exceptions \
	--enable-newlib-io-long-long --with-build-time-tools=${IROOT}%{_prefix}/nvptx-none/bin \
	--target nvptx-none --enable-as-accelerator-for=%{gcc_target_platform} \
	--enable-languages=c,c++,fortran,lto \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-checking=release --with-system-zlib \
	--with-gcc-major-version-only --without-isl
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_isl}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
sed -i 's|libisl\([^-]\)|libgcc13privateisl\1|g' \
  ../../isl-%{isl_version}/Makefile.{am,in}
../../isl-%{isl_version}/configure \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags} CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC"
make install
cd ../isl-install/lib
rm libgcc13privateisl.so{,.23}
mv libgcc13privateisl.so.23.1.0 libisl.so.23
ln -sf libisl.so.23 libisl.so
cd ../..
%endif

enablelgo=
enablelada=
enablelobjc=
enableld=
%if %{build_objc}
enablelobjc=,objc,obj-c++
%endif
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_d}
enableld=,d
%endif
%if %{build_m2}
enablelm2=,m2
%endif
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch ppc64le %{mips} s390x
%ifarch s390x
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
	--enable-multilib \
%else
	--disable-multilib \
%endif
%else
	--disable-multilib \
%endif
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
	--enable-libstdcxx-backtrace --with-libstdcxx-zoneinfo=%{_datadir}/zoneinfo \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
%if %{build_isl}
	--with-isl=`pwd`/isl-install \
%else
	--without-isl \
%endif
%if %{build_offload_nvptx}
	--enable-offload-targets=nvptx-none \
	--without-cuda-driver --enable-offload-defaulted \
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
%ifarch ppc64le
	--with-long-double-format=ieee \
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
%if 0%{?rhel} >= 9
	--with-cpu-32=power9 --with-tune-32=power9 --with-cpu-64=power9 --with-tune-64=power9 \
%else
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--enable-cet \
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
%if 0%{?rhel} > 8
	--with-arch_64=x86-64-v2 \
%endif
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
%if 0%{?rhel} > 7
%if 0%{?rhel} > 8
%if 0%{?rhel} >= 9
	--with-arch=z14 --with-tune=z15 \
%else
	--with-arch=z13 --with-tune=arch13 \
%endif
%else
	--with-arch=z13 --with-tune=z14 \
%endif
%else
	--with-arch=z196 --with-tune=zEC12 \
%endif
%else
%if 0%{?fedora} >= 38
	--with-arch=z13 --with-tune=z14 \
%else
%if 0%{?fedora} >= 26
	--with-arch=zEC12 --with-tune=z13 \
%else
	--with-arch=z9-109 --with-tune=z10 \
%endif
%endif
%endif
	--enable-decimal-float \
%endif
%ifarch armv7hl
	--with-tune=generic-armv7-a --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifarch riscv64
	--with-arch=rv64gc --with-abi=lp64d --with-multilib-list=lp64d \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
%ifnarch %{arm}
	--with-build-config=bootstrap-lto --enable-link-serialization=1 \
%endif
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,fortran${enablelobjc}${enablelada}${enablelgo}${enableld}${enablelm2},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" LDFLAGS_FOR_TARGET=-Wl,-z,relro,-z,now bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" LDFLAGS_FOR_TARGET=-Wl,-z,relro,-z,now profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

%if %{build_isl}
cp -a isl-install/lib/libisl.so.23 gcc/
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
mkdir -p rpm.doc/{gfortran,objc,gdc,libphobos,gm2,libgm2}
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%if %{build_objc}
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%endif
%if %{build_d}
(cd gcc/d; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gdc/$i.gdc
done)
(cd libphobos; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libphobos/$i.libphobos
done
cp -a src/LICENSE*.txt libdruntime/LICENSE.txt ../rpm.doc/libphobos/)
%endif
%if %{build_m2}
(cd gcc/m2; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gm2/$i.gm2
done)
(cd libgm2; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libgm2/$i.libgm2
done)
%endif
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

%if %{build_annobin_plugin}
mkdir annobin-plugin
cd annobin-plugin
tar xf %{_usrsrc}/annobin/latest-annobin.tar.xz
cd annobin*
touch aclocal.m4 configure Makefile.in */configure */config.h.in */Makefile.in
ANNOBIN_FLAGS=../../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags
ANNOBIN_CFLAGS1="%build_cflags -I %{_builddir}/gcc-%{version}-%{DATE}/gcc"
ANNOBIN_CFLAGS1="$ANNOBIN_CFLAGS1 -I %{_builddir}/gcc-%{version}-%{DATE}/obj-%{gcc_target_platform}/gcc"
ANNOBIN_CFLAGS2="-I %{_builddir}/gcc-%{version}-%{DATE}/include -I %{_builddir}/gcc-%{version}-%{DATE}/libcpp/include"
ANNOBIN_LDFLAGS="%build_ldflags -L%{_builddir}/gcc-%{version}-%{DATE}/obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs"
CC="`$ANNOBIN_FLAGS --build-cc`" CXX="`$ANNOBIN_FLAGS --build-cxx`" \
  CFLAGS="$ANNOBIN_CFLAGS1 $ANNOBIN_CFLAGS2 $ANNOBIN_LDFLAGS" \
  CXXFLAGS="$ANNOBIN_CFLAGS1 `$ANNOBIN_FLAGS --build-includes` $ANNOBIN_CFLAGS2 $ANNOBIN_LDFLAGS" \
  ./configure --with-gcc-plugin-dir=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin \
	      --without-annocheck --without-tests --without-docs --disable-rpath --without-debuginfod
make
cd ../..
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# RISC-V ABI wants to install everything in /lib64/lp64d or /usr/lib64/lp64d.
# Make these be symlinks to /lib64 or /usr/lib64 respectively. See:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/DRHT5YTPK4WWVGL3GIN5BF2IKX2ODHZ3/
%ifarch riscv64
for d in %{buildroot}%{_libdir} %{buildroot}/%{_lib} \
	  %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib} \
	  %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/%{_lib}; do
  mkdir -p $d
  (cd $d && ln -sf . lp64d)
done
%endif

%if %{build_offload_nvptx}
cd nvptx-tools-%{nvptx_tools_gitrev}
cd obj-%{gcc_target_platform}
make install prefix=%{buildroot}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
cd obj-offload-nvptx-none
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/mgomp/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/mgomp/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
find %{buildroot}%{_prefix}/lib/gcc/nvptx-none %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none \
     %{buildroot}%{_prefix}/nvptx-none/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

%if %{build_isl}
cp -a isl-install/lib/libisl.so.23 $FULLPATH/
%endif

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
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
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

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
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
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

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
%if %{build_d}
mv %{buildroot}%{_prefix}/%{_lib}/libgphobos.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 ppc64le %{arm} aarch64 riscv64
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%else
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%endif
%ifarch sparcv9 ppc
%ifarch ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m64 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%else
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%endif
%ifarch %{multilib_64_archs}
%ifarch x86_64 ppc64 ppc64p7
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m32 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%else
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
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
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
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
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.5.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.22.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../libgdruntime.so.4.* libgdruntime.so
ln -sf ../../../libgphobos.so.4.* libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../libm2$i.so.18.* libm2$i.so
done
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.8.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.1.* libubsan.so
%endif
else
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.5.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.22.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../../%{_lib}/libgdruntime.so.4.* libgdruntime.so
ln -sf ../../../../%{_lib}/libgphobos.so.4.* libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../../%{_lib}/libm2$i.so.18.* libm2$i.so
done
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.8.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.1.* libubsan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.2.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
%endif
%if %{build_libhwasan}
rm -f libhwasan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libhwasan.so.0.* | sed 's,^.*libh,libh,'`' )' > libhwasan.so
mv ../../../../%{_lib}/libhwasan_preinit.o libhwasan_preinit.o
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
mv ../../../../%{_lib}/liblsan_preinit.o liblsan_preinit.o
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++exp.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++_libbacktrace.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_d}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgdruntime.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgphobos.*a $FULLLPATH/
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  mv -f %{buildroot}%{_prefix}/%{_lib}/libm2$i.*a $FULLLPATH/
  rm -f m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so m2/m2$i/
  ln -sf ../../libm2$i.a m2/m2$i/
done
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
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
%endif
%if %{build_libhwasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libhwasan.*a $FULLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
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
ln -sf ../../../../../libgnarl-*.so libgnarl-12.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-12.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-12.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-12.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-12.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-12.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-12.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-12.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
%if %{build_objc}
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
%endif
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.5.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.22.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.22.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgdruntime.so.4.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgdruntime.so.4.* | sed 's,^.*libg,libg,'`' )' > 64/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgphobos.so.4.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgphobos.so.4.* | sed 's,^.*libg,libg,'`' )' > 64/libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  rm -f libm2$i.so
  echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libm2$i.so.18.* | sed 's,^.*libm,libm,'`' )' > libm2$i.so
  echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libm2$i.so.18.* | sed 's,^.*libm,libm,'`' )' > 64/libm2$i.so
  rm -f 64/m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so 64/m2/m2$i/
  ln -sf ../../libm2$i.a 64/m2/m2$i/
done
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
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libstdc++exp.a libstdc++exp.a
ln -sf ../lib64/libstdc++exp.a 64/libstdc++exp.a
ln -sf lib32/libstdc++_libbacktrace.a libstdc++_libbacktrace.a
ln -sf ../lib64/libstdc++_libbacktrace.a 64/libstdc++_libbacktrace.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_d}
ln -sf lib32/libgdruntime.a libgdruntime.a
ln -sf ../lib64/libgdruntime.a 64/libgdruntime.a
ln -sf lib32/libgphobos.a libgphobos.a
ln -sf ../lib64/libgphobos.a 64/libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf lib32/libm2$i.a libm2$i.a
  ln -sf ../lib64/libm2$i.a 64/libm2$i.a
done
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
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
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
%if %{build_objc}
ln -sf ../../../../libobjc.so.4 32/libobjc.so
%endif
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.5.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.22.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.22.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgdruntime.so.4.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgdruntime.so.4.* | sed 's,^.*libg,libg,'`' )' > 32/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgphobos.so.4.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgphobos.so.4.* | sed 's,^.*libg,libg,'`' )' > 32/libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  rm -f libm2$i.so
  echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libm2$i.so.18.* | sed 's,^.*libm,libm,'`' )' > libm2$i.so
  echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libm2$i.so.18.* | sed 's,^.*libm,libm,'`' )' > 32/libm2$i.so
  rm -f 32/m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so 32/m2/m2$i/
  ln -sf ../../libm2$i.a 32/m2/m2$i/
done
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
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libstdc++exp.a 32/libstdc++exp.a
ln -sf lib64/libstdc++exp.a libstdc++exp.a
ln -sf ../lib32/libstdc++_libbacktrace.a 32/libstdc++_libbacktrace.a
ln -sf lib64/libstdc++_libbacktrace.a libstdc++_libbacktrace.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_d}
ln -sf ../lib32/libgdruntime.a 32/libgdruntime.a
ln -sf lib64/libgdruntime.a libgdruntime.a
ln -sf ../lib32/libgphobos.a 32/libgphobos.a
ln -sf lib64/libgphobos.a libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../lib32/libm2$i.a 32/libm2$i.a
  ln -sf lib64/libm2$i.a libm2$i.a
done
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
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++exp.a 32/libstdc++exp.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++_libbacktrace.a 32/libstdc++_libbacktrace.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libsupc++.a 32/libsupc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_d}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgdruntime.a 32/libgdruntime.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgphobos.a 32/libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libm2$i.a 32/libm2$i.a
done
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libasan.a 32/libasan.a
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgolibbegin.a 32/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adalib 32/adalib
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libobjc.a -o -name libgdruntime.a -o -name libgphobos.a \
		-o -name libm2\*.a -o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libstdc++exp.a \
		-o -name libstdc++_libbacktrace.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libgdruntime.a -o -name libgphobos.a -o -name libm2\*.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcc1.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.5.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_d}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgdruntime.so.4.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgphobos.so.4.*
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  chmod 755 %{buildroot}%{_prefix}/%{_lib}/libm2$i.so.18.*
done
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.8.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.2.*
%endif
%if %{build_libhwasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libhwasan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
# Avoid stripping these libraries and binaries.
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.22.*
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

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
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gdc || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gm2 || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

# Add symlink to lto plugin in the binutils plugin directory.
%{__mkdir_p} %{buildroot}%{_libdir}/bfd-plugins/
ln -s ../../libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so \
  %{buildroot}%{_libdir}/bfd-plugins/

%if %{build_annobin_plugin}
mkdir -p $FULLPATH/plugin
rm -f $FULLPATH/plugin/gcc-annobin*
cp -a %{_builddir}/gcc-%{version}-%{DATE}/annobin-plugin/annobin*/gcc-plugin/.libs/annobin.so.0.0.0 \
  $FULLPATH/plugin/gcc-annobin.so.0.0.0
ln -sf gcc-annobin.so.0.0.0 $FULLPATH/plugin/gcc-annobin.so.0
ln -sf gcc-annobin.so.0.0.0 $FULLPATH/plugin/gcc-annobin.so
%endif

%check
cd obj-%{gcc_target_platform}

# run the tests.
LC_ALL=C make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
%if !%{build_annobin_plugin}
if [ -f %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so ]; then
  # Test whether current annobin plugin won't fail miserably with the newly built gcc.
  echo -e '#include <stdio.h>\nint main () { printf ("Hello, world!\\n"); return 0; }' > annobin-test.c
  echo -e '#include <iostream>\nint main () { std::cout << "Hello, world!" << std::endl; return 0; }' > annobin-test.C
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{c,.c} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  2> ANNOBINOUT1 || echo Annobin test 1 FAIL > ANNOBINOUT2;
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` \
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{C,.C} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/:%{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  -B %{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  2> ANNOBINOUT3 || echo Annobin test 2 FAIL > ANNOBINOUT4;
  [ -f ./annobin-testc ] || echo Annobin test 1 MISSING > ANNOBINOUT5;
  [ -f ./annobin-testc ] && \
  ( ./annobin-testc > ANNOBINRES1 2>&1 || echo Annobin test 1 RUNFAIL > ANNOBINOUT6 );
  [ -f ./annobin-testC ] || echo Annobin test 2 MISSING > ANNOBINOUT7;
  [ -f ./annobin-testC ] && \
  ( ./annobin-testC > ANNOBINRES2 2>&1 || echo Annobin test 2 RUNFAIL > ANNOBINOUT8 );
  cat ANNOBINOUT[1-8] > ANNOBINOUT
  touch ANNOBINRES1 ANNOBINRES2
  [ -s ANNOBINOUT ] && echo Annobin testing FAILed > ANNOBINRES
  cat ANNOBINOUT ANNOBINRES[12] >> ANNOBINRES
  rm -f ANNOBINOUT* ANNOBINRES[12] annobin-test{c,C}
fi
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
%if !%{build_annobin_plugin}
[ -f ANNOBINRES ] && cat ANNOBINRES
%endif
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | xz -9e \
  | uuencode testlogs-%{_target_platform}.tar.xz || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

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

%ldconfig_scriptlets -n libstdc++

%ldconfig_scriptlets -n libobjc

%ldconfig_scriptlets -n libgfortran

%ldconfig_scriptlets -n libgphobos

%ldconfig_scriptlets -n libgm2

%ldconfig_scriptlets -n libgnat

%ldconfig_scriptlets -n libgomp

%ldconfig_scriptlets gdb-plugin

%ldconfig_scriptlets -n libgccjit

%ldconfig_scriptlets -n libquadmath

%ldconfig_scriptlets -n libitm

%ldconfig_scriptlets -n libatomic

%ldconfig_scriptlets -n libasan

%ldconfig_scriptlets -n libubsan

%ldconfig_scriptlets -n libtsan

%ldconfig_scriptlets -n liblsan

%ldconfig_scriptlets -n libgo

%files -f %{name}.lang
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/gcov-dump
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%{_prefix}/bin/lto-dump
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
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-tool.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man1/lto-dump.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_libdir}/bfd-plugins/liblto_plugin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/acc_prof.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gfniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cet.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnnivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vaesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vpclmulqdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pconfigintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wbnoinvdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movdirintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/waitpkgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cldemoteintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/enqcmdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/serializeintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tsxldtrkintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxtileintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxint8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxbf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86gprintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/uintrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/hresetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/keylockerintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fp16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fp16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniint8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxneconvertintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cmpccxaddintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxfp16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/raointintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxcomplexintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amo.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86gprintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rs6000-vecdefines.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_sve.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vecintrin.h
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%if %{build_isl}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libisl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%endif
%if %{build_libhwasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan_preinit.o
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
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1

%files -n libgcc
/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
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
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/g++-mapper-server
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++_libbacktrace.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++_libbacktrace.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++_libbacktrace.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
# Package symlink to keep compatibility
%ifarch riscv64
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/lp64d
%endif
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%dir %{_prefix}/share/gcc-%{gcc_major}
%dir %{_prefix}/share/gcc-%{gcc_major}/python
%{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%files -n libstdc++-devel
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++_libbacktrace.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++_libbacktrace.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++_libbacktrace.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*
%endif

%files gfortran
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/finclude
%endif
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran
%{_prefix}/%{_lib}/libgfortran.so.5*

%files -n libgfortran-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif

%if %{build_d}
%files gdc
%{_prefix}/bin/gdc
%{_mandir}/man1/gdc.1*
%{_infodir}/gdc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/d
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/d21
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.spec
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.so
%endif
%doc rpm.doc/gdc/*

%files -n libgphobos
%{_prefix}/%{_lib}/libgdruntime.so.4*
%{_prefix}/%{_lib}/libgphobos.so.4*
%doc rpm.doc/libphobos/*

%files -n libgphobos-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgphobos.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgphobos.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%endif

%if %{build_m2}
%files gm2
%{_prefix}/bin/gm2
%{_mandir}/man1/gm2.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/m2
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1gm2
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/m2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libm2*.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libm2*.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/m2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libm2*.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libm2*.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/m2rte.so
%doc rpm.doc/gm2/*

%files -n libgm2
%{_prefix}/%{_lib}/libm2*.so.18*
%doc rpm.doc/libgm2/*

%files -n libgm2-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libm2*.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libm2*.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.a
%endif
%endif

%if %{build_ada}
%files gnat
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/ada_target_properties
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/ada_target_properties
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/ada_target_properties
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
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
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm.h
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%{_prefix}/%{_lib}/libasan.so.8*

%files -n libasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%{_prefix}/%{_lib}/libubsan.so.1*

%files -n libubsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%{_prefix}/%{_lib}/libtsan.so.2*

%files -n libtsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libhwasan}
%files -n libhwasan
%{_prefix}/%{_lib}/libhwasan.so.0*

%files -n libhwasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan.a
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
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_go}
%files go
%ghost %{_prefix}/bin/go
%attr(755,root,root) %{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%ghost %{_prefix}/bin/gofmt
%attr(755,root,root) %{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgolibbegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgolibbegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%attr(755,root,root) %{_prefix}/%{_lib}/libgo.so.22*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgolibbegin.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgolibbegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif

%files -n libgo-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
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
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%if %{build_offload_nvptx}
%files offload-nvptx
%{_prefix}/bin/nvptx-none-*
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-gcc
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-lto-dump
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%{_prefix}/lib/gcc/nvptx-none
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%dir %{_prefix}/nvptx-none
%{_prefix}/nvptx-none/bin
%{_prefix}/nvptx-none/include

%files -n libgomp-offload-nvptx
%{_prefix}/%{_lib}/libgomp-plugin-nvptx.so.*
%endif

%if %{build_annobin_plugin}
%files plugin-annobin
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so.0
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so.0.0.0
%endif

%changelog
* Mon Nov 13 2023 Jakub Jelinek <jakub@redhat.com> 13.2.1-5
- update from releases/gcc-13 branch
  - PRs c++/89038, c/111884, d/110712, d/112270, fortran/67740, fortran/97245,
	fortran/111837, fortran/112316, libbacktrace/111315,
	libbacktrace/112263, libstdc++/110944, libstdc++/111172,
	libstdc++/111936, libstdc++/112089, libstdc++/112314,
	middle-end/111253, middle-end/111818, modula2/111756, modula2/112110,
	target/101177, target/110170, target/111001, target/111366,
	target/111367, target/111380, target/111935, target/112443,
	tree-optimization/111397, tree-optimization/111445,
	tree-optimization/111489, tree-optimization/111583,
	tree-optimization/111614, tree-optimization/111622,
	tree-optimization/111694, tree-optimization/111764,
	tree-optimization/111820, tree-optimization/111833,
	tree-optimization/111917
  - fix aarch64 RA ICE (#2241139, PR target/111528)
- fix ia32 doubleword rotates (#2238781, PR target/110792)

* Wed Oct 11 2023 Jakub Jelinek <jakub@redhat.com> 13.2.1-4
- update from releases/gcc-13 branch
  - PRs ada/110488, ada/111434, c++/99631, c++/111471, c++/111485, c++/111493,
	c++/111512, fortran/68155, fortran/92586, fortran/111674,
	libstdc++/108046, libstdc++/111050, libstdc++/111102,
	libstdc++/111511, middle-end/111699, modula2/111510, target/111121,
	target/111411, tree-optimization/110315, tree-optimization/110386,
	tree-optimization/111331, tree-optimization/111519

* Mon Sep 18 2023 Jakub Jelinek <jakub@redhat.com> 13.2.1-3
- update from releases/gcc-13 branch
  - PRs c++/111357, modula2/111330, target/96762, target/111306,
	target/111335, target/111340, target/111412

* Fri Sep  8 2023 Jakub Jelinek <jakub@redhat.com> 13.2.1-2
- update from releases/gcc-13 branch
  - PRs c++/92407, c++/106310, c++/106652, c++/109678, c++/109751, c++/110197,
	c++/110566, c++/110927, debug/111080, fortran/99326, fortran/102109,
	fortran/102112, fortran/102190, fortran/102532, fortran/108961,
	fortran/109684, fortran/109948, fortran/110825, libgcc/110956,
	libstdc++/110593, libstdc++/110708, libstdc++/110719,
	libstdc++/110807, libstdc++/110860, libstdc++/110862,
	libstdc++/110917, libstdc++/110968, libstdc++/110970,
	libstdc++/110974, libstdc++/110990, middle-end/111017, modula2/108119,
	modula2/108344, modula2/109779, modula2/109810, modula2/109830,
	modula2/109879, modula2/109908, modula2/109952, modula2/110003,
	modula2/110019, modula2/110125, modula2/110126, modula2/110161,
	modula2/110174, modula2/110189, modula2/110284, modula2/110631,
	modula2/110779, modula2/110865, target/89835, target/109713,
	target/109725, target/110220, target/110484, target/110741,
	target/111010, target/111127, tree-optimization/110280,
	tree-optimization/110702, tree-optimization/110914,
	tree-optimization/111015, tree-optimization/111019,
	tree-optimization/111039, tree-optimization/111070,
	tree-optimization/111109

* Mon Jul 31 2023 Patsy Griffin <patsy@redhat.com>
- allow for the optional removal of tzdata
  - see https://fedoraproject.org/wiki/Changes/AllowRemovalOfTzdata

* Fri Jul 28 2023 Jakub Jelinek <jakub@redhat.com> 13.2.1-1
- update from releases/gcc-13 branch
  - GCC 13.2 release
  - PRs c++/109247, c++/110102, c++/110122, c++/110463, c++/110468,
	c++/110524, c++/110535, c++/110595, c++/110809, d/103944, d/106977,
	d/108842, d/108962, d/110113, d/110359, d/110471, d/110514, d/110516,
	debug/110295, fortran/86277, fortran/95947, fortran/100297,
	fortran/110288, fortran/110585, fortran/110658, ipa/109983,
	ipa/110276, libgcc/109712, libgcc/110179, libstdc++/95048,
	libstdc++/100285, libstdc++/104299, libstdc++/109741,
	libstdc++/109921, libstdc++/110149, libstdc++/110239,
	libstdc++/110432, libstdc++/110542, libstdc++/110574,
	middle-end/98619, middle-end/103979, middle-end/110055,
	middle-end/110420, modula2/108121, modula2/109586, modula2/109675,
	modula2/109729, modula2/110246, rtl-optimization/110237,
	target/101469, target/105325, target/106966, target/108743,
	target/109932, target/110011, target/110100, target/110132,
	target/110136, target/110206, target/110264, target/110309,
	target/110406, target/110560, target/110624, testsuite/66005,
	testsuite/83904, testsuite/110230, tree-optimization/109143,
	tree-optimization/110228, tree-optimization/110298,
	tree-optimization/110381, tree-optimization/110392,
	tree-optimization/110515, tree-optimization/110556,
	tree-optimization/110557, tree-optimization/110669,
	tree-optimization/110731, tree-optimization/110755,
	tree-optimization/110766, tree-optimization/110799,
	tree-optimization/110829

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.1.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Jakub Jelinek <jakub@redhat.com> 13.1.1-4
- update from releases/gcc-13 branch
  - PRs bootstrap/110085, c++/109871, fortran/100607, libgcc/109670,
	libgcc/109685, libstdc++/108178, libstdc++/109261, libstdc++/109758,
	libstdc++/109822, libstdc++/109949, libstdc++/110139,
	middle-end/110200, target/82931, target/92729, target/104327,
	target/105753, target/106907, target/109547, target/109650,
	target/109800, target/109939, target/109954, target/110036,
	target/110044, target/110088, target/110108, target/110227,
	tree-optimization/109505, tree-optimization/110165,
	tree-optimization/110166

* Fri May 19 2023 Jakub Jelinek <jakub@redhat.com> 13.1.1-3
- update from releases/gcc-13 branch
  - PRs c++/80488, c++/83258, c++/97700, c++/103807, c++/109651, c++/109745,
	c++/109761, c++/109774, c++/109868, c++/109884, fortran/109641,
	fortran/109846, libstdc++/109816, libstdc++/109883, target/104338,
	target/109697

* Thu May 11 2023 Jakub Jelinek <jakub@redhat.com> 13.1.1-2
- update from releases/gcc-13 branch
  - PRs c++/91618, c++/96604, c++/109506, c++/109640, c++/109642, c++/109666,
	c++/109671, c++/109756, c/107682, c/109409, c/109412, debug/109676,
	fortran/109622, libffi/109447, libgomp/108098, libstdc++/40380,
	libstdc++/109694, libstdc++/109703, rtl-optimization/109585,
	target/108758, target/109069, target/109535, target/109661,
	target/109762, tree-optimization/109573, tree-optimization/109609,
	tree-optimization/109724, tree-optimization/109778

* Wed Apr 26 2023 Jakub Jelinek <jakub@redhat.com> 13.1.1-1
- update from releases/gcc-13 branch
  - GCC 13.1 release
  - PRs c/107041, target/109566

* Fri Apr 21 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.16
- update from trunk and releases/gcc-13 branch
  - GCC 13.1-rc3
  - PRs tree-optimization/109564
- fix ICE on fneg/fadd optimization (PR tree-optimization/109583)
- include amxcomplexintrin.h header on x86 (#2188608)

* Wed Apr 19 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.15
- update from trunk and releases/gcc-13 branch
  - GCC 13.1-rc2
  - PRs c++/109556, target/106602

* Tue Apr 18 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.14
- update from trunk and releases/gcc-13 branch
  - PRs analyzer/108722, bootstrap/109510, c++/109277, c++/109357, c++/109420,
	c++/109514, c++/109531, driver/108241, fortran/61615, fortran/85686,
	fortran/87477, fortran/88247, fortran/91941, fortran/92779,
	fortran/93339, fortran/93813, fortran/98408, fortran/99982,
	fortran/100948, fortran/102106, fortran/104272, fortran/104312,
	fortran/104349, fortran/105205, fortran/106918, fortran/109492,
	fortran/109511, ipa/107769, ipa/108959, ipa/109318, libstdc++/108291,
	libstdc++/108827, libstdc++/108969, libstdc++/109482,
	libstdc++/109525, modula2/109423, modula2/109488, modula2/109496,
	modula2/109497, target/54816, target/70243, target/99708,
	target/104989, target/108812, target/108892, target/108947,
	target/109040, target/109104, target/109374, target/109402,
	target/109458, target/109479, target/109508, testsuite/108809,
	testsuite/108815, tree-optimization/108139, tree-optimization/109392,
	tree-optimization/109410, tree-optimization/109417,
	tree-optimization/109427, tree-optimization/109434,
	tree-optimization/109462, tree-optimization/109469,
	tree-optimization/109473, tree-optimization/109491,
	tree-optimization/109502, tree-optimization/109524,
	tree-optimization/109539

* Tue Apr  4 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.13
- update from trunk
  - PRs c++/53164, c++/105848, c++/107484, c++/109160, c++/109300, ipa/109303,
	modula2/109388, other/109306, sanitizer/109107, target/102146,
	target/108699, target/108807, target/109375, target/109376,
	target/109384, tree-optimization/109304, tree-optimization/109386

* Sat Apr  1 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.12
- update from trunk
  - PRs analyzer/107396, bootstrap/101834, c++/101118, c++/105221, c++/105452,
	c++/107897, c++/108887, c++/109278, c++/109319, libstdc++/109242,
	libstdc++/109339, libstdc++/109340, modula2/109315, modula2/109336,
	target/85048, target/109254, target/109328, tree-optimization/91645,
	tree-optimization/109342, tree-optimization/109362

* Wed Mar 29 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.11
- update from trunk
  - PRs analyzer/109098, bootstrap/84402, bootstrap/109310, c++/105481,
	c++/106969, c++/107163, c++/109309, c++/109320, c++/109321, c/107002,
	fortran/104321, fortran/104949, fortran/109314, gcov-profile/109297,
	ipa/105685, ipa/106124, libgcc/108891, libstdc++/103387,
	libstdc++/109288, libstdc++/109299, lto/109263, middle-end/106190,
	other/109163, other/109293, rtl-optimization/109187,
	rtl-optimization/109237, target/106282, target/109072, target/109082,
	target/109140, target/109167, target/109276, target/109296,
	target/109312, tree-optimization/54498, tree-optimization/106912,
	tree-optimization/107087, tree-optimization/108129,
	tree-optimization/108357, tree-optimization/109154,
	tree-optimization/109230, tree-optimization/109238,
	tree-optimization/109265, tree-optimization/109274,
	tree-optimization/109301, tree-optimization/109327,
	tree-optimization/109331

* Fri Mar 24 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.10
- update from trunk
  - PRs analyzer/109239, c++/105996, c++/108390, c++/108795, c++/109177,
	c++/109241, c/84900, fortran/104572, middle-end/109258,
	modula2/107630, modula2/109248, modula2/109264, target/103628,
	target/109137, target/109228, target/109244, testsuite/105959,
	tree-optimization/99739, tree-optimization/107569,
	tree-optimization/109176, tree-optimization/109262

* Tue Mar 21 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.9
- update from trunk
  - PRs analyzer/109094, c++/106890, c++/109159, c++/109164, fortran/85877,
	fortran/87127, fortran/99036, fortran/109186, fortran/109206,
	fortran/109209, fortran/109216, libstdc++/109182, target/109067,
	target/109178, testsuite/108898, tree-optimization/109170,
	tree-optimization/109192, tree-optimization/109215,
	tree-optimization/109219

* Sat Mar 18 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.8
- update from trunk
  - PRs analyzer/105906, analyzer/108045, analyzer/109097, c++/58538,
	c++/69410, c++/95036, c++/96830, c++/98056, c++/100288, c++/101869,
	c++/103871, c++/104107, c++/105406, c++/105809, c++/107128,
	c++/107280, c++/107310, c++/108179, c++/108242, c++/108468,
	c++/108975, c++/109096, c++/109172, c/109151, d/109108, d/109144,
	fortran/37336, fortran/58331, fortran/64290, fortran/67444,
	fortran/67471, fortran/69298, fortran/70863, fortran/71798,
	fortran/80524, fortran/82996, fortran/84472, fortran/88735,
	fortran/91316, fortran/93691, fortran/96122, fortran/103854,
	fortran/106576, fortran/106945, ipa/107925, libstdc++/62196,
	libstdc++/109111, libstdc++/109165, middle-end/106133,
	middle-end/108685, middle-end/109031, modula2/109032, modula2/109089,
	modula2/109102, modula2/109103, modula2/109125, other/109086,
	preprocessor/67046, rtl-optimization/107762, rtl-optimization/109179,
	target/105554, target/108583, target/109092, target/109109,
	target/109117, testsuite/109118, testsuite/109129, testsuite/109145,
	tree-optimization/106896, tree-optimization/109005,
	tree-optimization/109046, tree-optimization/109115,
	tree-optimization/109123, tree-optimization/109139,
	tree-optimization/109141, web/88860

* Fri Mar 10 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.7
- update from trunk
  - PRs ada/108858, ada/108983, analyzer/102671, analyzer/105755,
	analyzer/108251, analyzer/108400, analyzer/108475, analyzer/109059,
	analyzer/109060, c++/102529, c++/105841, c++/106651, c++/107532,
	c++/107558, c++/107939, c++/108099, c++/108542, c++/108566,
	c++/108773, c++/108972, c++/109030, c++/109039, c++/109042, c/108079,
	driver/108865, fortran/104332, fortran/106856, libgcc/108727,
	libgomp/90596, libgomp/109062, libstdc++/107572, libstdc++/108362,
	libstdc++/108882, libstdc++/109024, libstdc++/109064,
	middle-end/108995, other/108464, plugins/108634, sanitizer/81649,
	sanitizer/108060, sanitizer/109050, target/107299, target/107703,
	target/107998, target/108185, target/108429, target/108654,
	target/109000, testsuite/70150, testsuite/108729, testsuite/108730,
	testsuite/108810, testsuite/108813, tree-optimization/108980,
	tree-optimization/109008, tree-optimization/109025

* Sat Mar  4 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.6
- update from trunk
  - PRs ada/108909, analyzer/107565, analyzer/108830, analyzer/108935,
	analyzer/108968, analyzer/109016, c++/100127, c++/105224, c++/105839,
	c++/106259, c++/107574, c++/107938, c++/108218, c++/108219,
	c++/108550, c++/108606, c++/108702, c++/108848, c++/108934,
	c++/108998, c/107465, c/107846, c/108880, c/108986, d/108167,
	d/108763, d/108877, d/108945, d/108946, debug/108716, debug/108772,
	debug/108967, fortran/96024, fortran/96025, fortran/108621,
	fortran/108923, fortran/108924, fortran/108937, jit/107999,
	libquadmath/87204, libquadmath/94756, libstdc++/52590,
	libstdc++/95989, libstdc++/104852, libstdc++/108846, libstdc++/108856,
	libstdc++/108952, middle-end/97956, middle-end/106258,
	middle-end/107411, middle-end/108545, middle-end/108546,
	middle-end/108854, middle-end/109006, modula2/108261, modula2/108944,
	modula2/108956, pch/14940, sanitizer/108834, sanitizer/108894,
	target/51534, target/104882, target/108240, target/108876,
	target/108881, target/108883, target/108910, target/108919,
	target/108922, testsuite/79356, testsuite/91419, testsuite/108899,
	testsuite/108942, testsuite/108973, testsuite/108985,
	testsuite/108991, translation/108890, tree-optimization/108430,
	tree-optimization/108603, tree-optimization/108793,
	tree-optimization/108828, tree-optimization/108888,
	tree-optimization/108950, tree-optimization/108970,
	tree-optimization/108979, tree-optimization/108988,
	tree-optimization/109002

* Tue Feb 21 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.5
- update from trunk
  - PRs analyzer/108664, analyzer/108666, analyzer/108725, analyzer/108806,
	c++/52809, c++/53638, c++/87389, c++/89741, c++/92099, c++/97553,
	c++/101073, c++/104041, c++/104691, c++/107773, c++/108243,
	c++/108829, c/105660, c/108375, fortran/103608, fortran/104554,
	libstdc++/108030, target/90458, target/108805, target/108831,
	target/108832, target/108862, testsuite/108835,
	tree-optimization/108657, tree-optimization/108783,
	tree-optimization/108791, tree-optimization/108816,
	tree-optimization/108819, tree-optimization/108821,
	tree-optimization/108825, tree-optimization/108855,
	tree-optimization/108868

* Wed Feb 15 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.4
- update from trunk
  - PRs analyzer/108704, analyzer/108733, analyzer/108745, c++/106675,
	c++/107079, c++/108698, d/107469, fortran/69636, fortran/103259,
	fortran/103475, fortran/103779, fortran/107424, fortran/108512,
	ipa/108605, ipa/108679, libstdc++/103934, middle-end/26854,
	middle-end/106080, rtl-optimization/108681, sanitizer/108777,
	target/96373, target/100758, target/103109, target/108102,
	target/108516, target/108723, target/108738, target/108787,
	target/108790, testsuite/106120, tree-optimization/28614,
	tree-optimization/96921, tree-optimization/106722,
	tree-optimization/107561, tree-optimization/108316,
	tree-optimization/108355, tree-optimization/108520,
	tree-optimization/108571, tree-optimization/108684,
	tree-optimization/108687, tree-optimization/108688,
	tree-optimization/108691, tree-optimization/108692,
	tree-optimization/108724, tree-optimization/108782

* Wed Feb  8 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.3
- update from trunk
  - PRs analyzer/108616, analyzer/108633, analyzer/108661, c++/101071,
	c++/102870, c++/107461, c++/107593, c++/107755, c++/108158,
	c++/108559, c++/108579, c++/108597, c++/108607, c++/96745, c/108150,
	c/108192, debug/106746, debug/108573, driver/108572, fortran/103506,
	fortran/108450, fortran/108451, fortran/108453, fortran/108527,
	fortran/108592, fortran/108609, fortran/95107, ipa/107300, ipa/108384,
	ipa/108509, ipa/108511, libstdc++/108636, libstdc++/108672,
	middle-end/108435, middle-end/108500, middle-end/108625,
	modula2/107234, modula2/108135, modula2/108462, modula2/108551,
	modula2/108612, rtl-optimization/108086, rtl-optimization/108463,
	rtl-optimization/108508, rtl-optimization/108596, sanitizer/108106,
	target/104921, target/107674, target/108443, target/108484,
	target/108589, target/108599, testsuite/108604, testsuite/108632,
	tree-optimization/26854, tree-optimization/106433,
	tree-optimization/106923, tree-optimization/107570,
	tree-optimization/108356, tree-optimization/108359,
	tree-optimization/108385, tree-optimization/108574,
	tree-optimization/108582, tree-optimization/108601,
	tree-optimization/108608, tree-optimization/108639,
	tree-optimization/108647, tree-optimization/108655
- drop libgfortran dependency on libquadmath for F28+ or RHEL8+, gcc-gfortran
  still needs to depend on both libquadmath and libquadmath-devel though

* Sat Jan 28 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.2
- update from trunk
  - PRs analyzer/108455, analyzer/108507, analyzer/108524, bootstrap/90543,
	c++/53288, c++/53932, c++/105300, c++/107267, c++/107303, c++/107329,
	c++/107797, c++/108195, c++/108437, c++/108474, c++/108496,
	c++/108503, c++/108504, c++/108525, c++/108526, c/108424,
	fortran/102331, fortran/102595, fortran/108420, fortran/108434,
	fortran/108501, fortran/108502, fortran/108528, fortran/108529,
	fortran/108544, fortran/108558, ipa/106061, ipa/107944,
	libstdc++/102301, libstdc++/108530, libstdc++/108554,
	libstdc++/108568, lto/108445, middle-end/108086, middle-end/108459,
	middle-end/108543, modula2/102343, modula2/108144, modula2/108182,
	modula2/108405, modula2/108480, modula2/108553, modula2/108555,
	other/108560, target/107568, target/107678, target/107731,
	target/108177, target/108348, target/108396, target/108411,
	target/108436, target/108442, target/108505, testsuite/104756,
	testsuite/107808, testsuite/108533, tree-optimization/96373,
	tree-optimization/108306, tree-optimization/108440,
	tree-optimization/108447, tree-optimization/108449,
	tree-optimization/108457, tree-optimization/108482,
	tree-optimization/108498, tree-optimization/108500,
	tree-optimization/108522, tree-optimization/108523,
	tree-optimization/108540, tree-optimization/108547

* Tue Jan 17 2023 Jakub Jelinek <jakub@redhat.com> 13.0.1-0.1
- update from trunk
  - PRs c++/105593, fortran/108421, go/108426, ipa/106077, libstdc++/108288,
	libstdc++/108413, other/108413, target/55522, target/96795,
	target/105980, target/107515, target/108272, tree-optimization/94793,
	tree-optimization/106523
- don't build ppc64le unwinder with -fno-omit-frame-pointer (#2161595)

* Sun Jan 15 2023 Jakub Jelinek <jakub@redhat.com> 13.0.0-0.9
- new package
