Summary:	Header files for the Linux kernel for use by glibc
Summary(pl):	Nag³ówki j±dra Linuksa do u¿ytku w glibc
Name:		glibc-kernel-headers
Version:	2.6.0.1
Release:	1
Epoch:		7
License:	GPL
Group:		Development
Source0:	http://www.kernel.pl/~mmazur/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	423e294118b6df14372ec301674d2a4c
Requires(pre):	fileutils
AutoReqProv:	no
Provides:	alsa-driver-devel
Provides:	i2c-devel = 2.8.2
Obsoletes:	alsa-driver-devel
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

%description -l pl
Ten pakiet zawiera pliki nag³ówkowe C, które definiuj± interfejs
miêdzy j±drem Linuksa a bibliotekami i programami dzia³aj±cymi w
przestrzeni u¿ytkownika. Pliki nag³ówkowe definiuj± struktury i sta³e
potrzebne do zbudowania wiêkszo¶ci standardowych programów, s± tak¿e
potrzebne do przebudowania pakietu glibc.

%prep
%setup -q

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

cp -a include/asm-generic $RPM_BUILD_ROOT%{_includedir}
cp -a include/asm-$arch $RPM_BUILD_ROOT%{_includedir}/asm
cp -a include/linux $RPM_BUILD_ROOT%{_includedir}
cp -a include/sound $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
[ ! -L /usr/include/linux ] || rm -f /usr/include/linux
[ ! -L /usr/include/asm ] || rm -f /usr/include/asm
%ifarch sparc
[ ! -L /usr/include/asm-sparc ] || rm -f /usr/include/asm-sparc
[ ! -L /usr/include/asm-sparc64 ] || rm -f /usr/include/asm-sparc64
%endif

%files
%defattr(644,root,root,755)
%{_includedir}/linux
%{_includedir}/asm*
%{_includedir}/sound
