Summary:	Header files for the Linux kernel for use by glibc
Summary(pl):	Nag³ówki j±dra Linuksa do u¿ytku w glibc
Name:		glibc-kernel-headers
Version:	1
Release:	2
Epoch:		1
License:	GPL
Group:		Development
Source0:	ftp://ftp.debian.org/debian/pool/main/l/linux-kernel-headers/linux-kernel-headers_2.5.999-test7-bk.orig.tar.gz
# Source0-md5: 181b3ea32207f82720300a68449cc2f2
Patch0:		%{name}-alpha-asm-param.patch
Patch1:		%{name}-asm-i386-byteorder-u64.patch
Patch2:		%{name}-ia64-modutils.patch
Patch3:		%{name}-ia64-pt-unwind-warning.patch
Patch4:		%{name}-linux-fb-compilefix.patch
Patch5:		%{name}-linux-radix-tree.patch
Patch6:		%{name}-linux-types-ustat.patch
Patch7:		%{name}-linux-unistd-errno.patch
Patch8:		%{name}-no-linux-compiler-h.patch
Patch9:		%{name}-other.patch
Requires(pre):	fileutils
AutoReqProv:	no
ExclusiveOS:	Linux
Obsoletes:	glibc-kernheaders
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
%setup -q -n linux-2.6.0-test7-bk
%patch0 
%patch1
%patch2
%patch3 -p1
%patch4 -p1
%patch5
%patch6 -p1
%patch7
%patch8
%patch9 -p1


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

%clean
rm -rf $RPM_BUILD_ROOT

%pre
[ -L /usr/include/linux ] && rm -f /usr/include/linux || :
[ -L /usr/include/asm ] && rm -f /usr/include/asm || :
%ifarch sparc
[ -L /usr/include/asm-sparc ] && rm -f /usr/include/asm-sparc
[ -L /usr/include/asm-sparc64 ] && rm -f /usr/include/asm-sparc64
%endif

%files
%defattr(644,root,root,755)
%{_includedir}/linux
%{_includedir}/asm*
