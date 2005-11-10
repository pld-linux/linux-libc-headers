Summary:	Linux kernel headers for use with C libraries
Summary(pl):	Nag³ówki j±dra Linuksa do u¿ytku z bibliotekami C
Name:		linux-libc-headers
Version:	2.6.12.0
Release:	8
Epoch:		7
License:	GPL
Group:		Development
Source0:	http://ep09.pld-linux.org/~mmazur/linux-libc-headers/%{name}-%{version}.tar.bz2
# Source0-md5:	eae2f562afe224ad50f65a6acfb4252c
Source1:	%{name}-dv1394.h
Source2:	%{name}-ieee1394-ioctl.h
Patch0:		%{name}-esfq.patch
Patch1:		%{name}-wrr.patch
Patch2:		%{name}-netfilter.patch
Patch3:		%{name}-fbsplash.patch
Patch4:		%{name}-tc-u32-mark.patch
Patch5:		%{name}-imq.patch
Patch6:		%{name}-endian.patch
# based on http://people.redhat.com/sgrubb/audit/audit.h
Patch7:		%{name}-audit.patch
Patch8:		%{name}-partial-2.6.14.patch
AutoReqProv:	no
BuildRequires:	rpmbuild(macros) >= 1.213
Requires(pre):	fileutils
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

%ifarch %{x8664} ppc64 s390x sparc sparc64 sparcv9
%define		dodual	1
%else
%define		dodual	0
%endif

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
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%ifarch %{x8664}
a1=i386
a2=x86_64
c1='defined(__i386__)'
c2='defined(__x86_64__)'
cond1=
%endif
%ifarch ppc64
a1=ppc
a2=ppc64
c1='defined(__powerpc__) && !defined(__powerpc64__)'
c2='defined(__powerpc64__)'
%endif
%ifarch s390 s390x
a1=sparc
a2=sparc64
c1='defined(__s390__) && !defined(__s390x__)'
c2='defined(__s390x__)'
%endif
%ifarch sparc sparcv9 sparc64
a1=sparc
a2=sparc64
c1='defined(__sparc__) && !defined(__arch64__)'
c2='defined(__sparc__) && defined(__arch64__)'
%endif

%if %{dodual}
cd include
rm -f asm
mkdir asm

for h in `( ls asm-${a1}; ls asm-${a2} ) | grep '\.h$' | sort -u`; do
	name=`echo $h | tr a-z. A-Z_`
	# common header
	cat > asm/$h << EOF
/* All asm/ files are generated and point to the corresponding
 * file in asm-${a1} or asm-${a2}.
 */

#ifndef __ASM_STUB_${name}__
#define __ASM_STUB_${name}__

#  if ${c1}
EOF

	if [ -f asm-${a1}/$h ]; then
		echo "#    include <asm-${a1}/$h>" >> asm/$h
	else
		echo "#    error <asm-${a1}/$h> does not exist" >> asm/$h
	fi

	cat >> asm/$h <<EOF
#  endif
#  if ${c2}
EOF

	if [ -f asm-${a2}/$h ]; then
		echo "#    include <asm-${a2}/$h>" >> asm/$h
	else
		echo "#    error <asm-${a2}/$h> does not exist" >> asm/$h
	fi

	# common footer
	cat >> asm/$h <<EOF
#  endif

#endif /* !__ASM_STUB_${name}__ */
EOF

done
echo "asm asm-${a1} asm-${a2}" > asmdirs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

cd include
%if %{dodual}
cp -a `cat asmdirs` $RPM_BUILD_ROOT%{_includedir}
%else
cp -a asm-%{_target_base_arch} $RPM_BUILD_ROOT%{_includedir}/asm
%endif
cp -a linux $RPM_BUILD_ROOT%{_includedir}
cp -a sound $RPM_BUILD_ROOT%{_includedir}

install -d $RPM_BUILD_ROOT%{_includedir}/linux/ieee1394/
install %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/linux/ieee1394/dv1394.h
install %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/linux/ieee1394/ieee1394-ioctl.h

find $RPM_BUILD_ROOT%{_includedir} -type f \
	'(' -name '*.orig' -o -name '*~' ')' | xargs -r rm

%clean
rm -rf $RPM_BUILD_ROOT

%pre
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
%{_includedir}/asm*
%{_includedir}/sound
