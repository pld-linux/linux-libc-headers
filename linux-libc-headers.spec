%define	basever	2.6.23
%define	postver	.1
Summary:	Linux kernel headers for use with C libraries
Summary(pl.UTF-8):	Nagłówki jądra Linuksa do użytku z bibliotekami C
Name:		linux-libc-headers
Version:	%{basever}%{postver}
Release:	2
Epoch:		7
License:	GPL v2
Group:		Development
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{basever}.tar.bz2
# Source0-md5:	2cc2fd4d521dc5d7cfce0d8a9d1b3472
%if "%{postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	896c5d4e7fd68d37b8c16e5d2842563b
%endif
# DROP? (these were always kept in private drivers dir, not exported)
#Source1:	%{name}-dv1394.h
#Source2:	%{name}-ieee1394-ioctl.h
# DROP for now? iptables accesses kernel headers/sources directly
#PatchX: %{name}-netfilter.patch
Patch0:		%{name}-esfq.patch
Patch1:		%{name}-wrr.patch
Patch2:		%{name}-fbsplash.patch
Patch3:		%{name}-imq.patch
Patch4:		%{name}-endian.patch
Patch5:		%{name}-pagesize.patch
Patch6:		%{name}-include.patch
Patch7:		%{name}-pom-set.patch
Patch8:		linux-kernel-headers.SuSE.TIOCGDEV.patch
Patch9:		%{name}-atm-vbr.patch
AutoReqProv:	no
BuildRequires:	rpmbuild(macros) >= 1.213
Requires(pre):	fileutils
Provides:	alsa-driver-devel
Provides:	glibc-kernel-headers = %{epoch}:%{version}-%{release}
Obsoletes:	alsa-driver-devel
Obsoletes:	glibc-kernel-headers
Obsoletes:	glibc-kernheaders
Conflicts:	lm_sensors-devel < 2.8.2-2
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip		1

%description
This package includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs. The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%description -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe C, które definiują interfejs
między jądrem Linuksa a bibliotekami i programami działającymi w
przestrzeni użytkownika. Pliki nagłówkowe definiują struktury i stałe
potrzebne do zbudowania większości standardowych programów, są także
potrzebne do przebudowania pakietu glibc.

%prep
%setup -qc
cd linux-%{basever}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p2
%patch9 -p1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C linux-%{basever} headers_install \
	INSTALL_HDR_PATH=$RPM_BUILD_ROOT%{_prefix} \
%ifarch ppc ppc64
	ARCH=powerpc
%else
	ARCH=%{_target_base_arch}
%endif

# provided by glibc-headers
rm -rf $RPM_BUILD_ROOT%{_includedir}/scsi

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
[ ! -L /usr/include/linux ] || rm -f /usr/include/linux
[ ! -L /usr/include/asm ] || rm -f /usr/include/asm
[ ! -L /usr/include/sound ] || rm -f /usr/include/sound
%ifarch sparc sparcv9 sparc64
[ ! -L /usr/include/asm-sparc ] || rm -f /usr/include/asm-sparc
[ ! -L /usr/include/asm-sparc64 ] || rm -f /usr/include/asm-sparc64
%endif

%files
%defattr(644,root,root,755)
%{_includedir}/linux
%{_includedir}/asm
%{_includedir}/asm-generic
%ifarch %{x8664}
%{_includedir}/asm-i386
%{_includedir}/asm-x86_64
%endif
%ifarch sparc64
%{_includedir}/asm-sparc
%{_includedir}/asm-sparc64
%endif
%{_includedir}/mtd
%{_includedir}/rdma
%{_includedir}/sound
%{_includedir}/video
