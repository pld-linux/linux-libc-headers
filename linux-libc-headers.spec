Summary:	Linux kernel headers for use with C libraries
Summary(pl):	Nag³ówki j±dra Linuksa do u¿ytku z bibliotekami C
Name:		linux-libc-headers
Version:	2.6.3.0
Release:	3
Epoch:		7
License:	GPL
Group:		Development
Source0:	http://ep09.pld-linux.org/~mmazur/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	9fc8b73da76ce34a10c5b56b173966ee
Patch0:		%{name}-netfilter.patch
Requires(pre):	fileutils
AutoReqProv:	no
Provides:	alsa-driver-devel
Provides:	i2c-devel = 2.8.2
Provides:	glibc-kernel-headers = %{epoch}:%{version}-%{release}
Obsoletes:	alsa-driver-devel
Obsoletes:	glibc-kernheaders
Obsoletes:	glibc-kernel-headers
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

%description -l pl
Ten pakiet zawiera pliki nag³ówkowe C, które definiuj± interfejs
miêdzy j±drem Linuksa a bibliotekami i programami dzia³aj±cymi w
przestrzeni u¿ytkownika. Pliki nag³ówkowe definiuj± struktury i sta³e
potrzebne do zbudowania wiêkszo¶ci standardowych programów, s± tak¿e
potrzebne do przebudowania pakietu glibc.

%prep
%setup -q
#%patch0 -p1

%build

%ifarch sparc sparcv6 sparc64
cd include
rm -f asm
mkdir asm

for h in `( ls asm-sparc; ls asm-sparc64 ) | grep '\.h$' | sort -u`; do
	name=`echo $h | tr a-z. A-Z_`
	# common header
	cat > asm/$h << EOF
/* All asm/ files are generated and point to the corresponding
 * file in asm-sparc or asm-sparc64. To regenerate, run "generate-asm"
 */

#ifndef __SPARCSTUB__${name}__
#define __SPARCSTUB__${name}__

EOF

	# common for sparc and sparc64
	if [ -f asm-sparc/$h -a -f asm-sparc64/$h ]; then
		cat >> asm/$h <<EOF
#ifdef __arch64__
#include <asm-sparc64/$h>
#else
#include <asm-sparc/$h>
#endif
EOF

	# sparc only
	elif [ -f asm-sparc/$h ]; then
		cat >> asm/$h <<EOF
#ifndef __arch64__
#include <asm-sparc/$h>
#endif
EOF

	# sparc64 only
	else
		cat >> asm/$h <<EOF
#ifdef __arch64__
#include <asm-sparc64/$h>
#endif
EOF

	fi

	# common footer
	cat >> asm/$h <<EOF

#endif /* !__SPARCSTUB__${name}__ */
EOF

done

%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%ifarch %{ix86}
arch=i386
%else
arch=%{_arch}
%endif

%ifarch sparc sparcv9 sparc64
cp -a include/asm-sparc $RPM_BUILD_ROOT%{_includedir}
cp -a include/asm-sparc64 $RPM_BUILD_ROOT%{_includedir}
%endif

cp -a include/asm-$arch $RPM_BUILD_ROOT%{_includedir}/asm
cp -a include/linux $RPM_BUILD_ROOT%{_includedir}
cp -a include/sound $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
[ ! -L /usr/include/linux ] || rm -f /usr/include/linux
[ ! -L /usr/include/asm ] || rm -f /usr/include/asm
[ ! -L /usr/include/sound ] || rm -f /usr/include/sound
%ifarch sparc
[ ! -L /usr/include/asm-sparc ] || rm -f /usr/include/asm-sparc
[ ! -L /usr/include/asm-sparc64 ] || rm -f /usr/include/asm-sparc64
%endif

%files
%defattr(644,root,root,755)
%{_includedir}/linux
%{_includedir}/asm*
%{_includedir}/sound
