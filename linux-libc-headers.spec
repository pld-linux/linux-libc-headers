Summary:	Linux kernel headers for use with C libraries
Summary(pl):	Nag³ówki j±dra Linuksa do u¿ytku z bibliotekami C
Name:		linux-libc-headers
Version:	2.6.11.2
Release:	3
Epoch:		7
License:	GPL
Group:		Development
Source0:	http://ep09.pld-linux.org/~mmazur/linux-libc-headers/%{name}-%{version}.tar.bz2
# Source0-md5:	2d21d8e7ff641da74272b114c786464e
Patch0:		%{name}-esfq.patch
Patch1:		%{name}-wrr.patch
Patch2:		%{name}-netfilter.patch
Patch3:		%{name}-fbsplash.patch
Patch4:		%{name}-tc-u32-mark.patch
BuildRequires:	rpmbuild(macros) >= 1.153
AutoReqProv:	no
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

%ifarch amd64 ppc64 s390x sparc sparc64 sparcv9
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
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%ifarch amd64
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
 * file in asm-${a1} or asm-${a2}. To regenerate, run "generate-asm"
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
