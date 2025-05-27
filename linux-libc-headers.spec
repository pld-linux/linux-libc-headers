%define	basever	6.15
%define	postver	0
Summary:	Linux kernel headers for use with C libraries
Summary(pl.UTF-8):	Nagłówki jądra Linuksa do użytku z bibliotekami C
Name:		linux-libc-headers
Version:	%{basever}.%{postver}
Release:	1
Epoch:		7
License:	GPL v2
Group:		Development
Source0:	https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{basever}.tar.xz
# Source0-md5:	c0f205cc27982a875c519f644a6288c4
%if "%{postver}" > "0"
Source1:	https://www.kernel.org/pub/linux/kernel/v6.x/patch-%{version}.xz
# Source1-md5:	fe8d59cd4ec0adf30396a7d040007f6a
%endif
Patch0:		%{name}-esfq.patch
Patch1:		%{name}-wrr.patch
Patch2:		%{name}-fbsplash.patch
Patch3:		%{name}-imq.patch
Patch4:		%{name}-pom-set.patch
Patch5:		%{name}-atm-vbr.patch
Patch6:		vserver.patch
URL:		https://www.kernel.org/
AutoReqProv:	no
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.568
BuildRequires:	rsync
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(pretrans):	coreutils
Obsoletes:	alsa-driver-devel < 1.1
Obsoletes:	glibc-kernel-headers < 7:2.6.2
Obsoletes:	glibc-kernheaders < 2.6
Conflicts:	lm_sensors-devel < 2.8.2-2
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch ppc ppc64
%define	target_arch powerpc
%else
%ifarch x32
%define	target_arch x86_64
%else
%ifarch aarch64
%define	target_arch arm64
%else
%define	target_arch %{_target_base_arch}
%endif
%endif
%endif

# no objects to extract debug info from
%define		_enable_debug_packages	0

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
%setup -q -c
cd linux-%{basever}
%if "%{postver}" > "0"
bzip2 -dc %{SOURCE1} | patch -p1
%endif
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C linux-%{basever} headers_install \
	INSTALL_HDR_PATH=$RPM_BUILD_ROOT%{_prefix} \
	ARCH=%{target_arch}

# provided by glibc-headers
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/scsi

# currently provided by libdrm-devel
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/drm

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
[ ! -L /usr/include/linux ] || rm -f /usr/include/linux
[ ! -L /usr/include/asm ] || rm -f /usr/include/asm
[ ! -L /usr/include/sound ] || rm -f /usr/include/sound

%files
%defattr(644,root,root,755)
%{_includedir}/asm
%{_includedir}/asm-generic
%{_includedir}/cxl
%{_includedir}/fwctl
%{_includedir}/linux
%{_includedir}/misc
%{_includedir}/mtd
%{_includedir}/rdma
%{_includedir}/regulator
%{_includedir}/sound
%{_includedir}/video
%{_includedir}/xen
