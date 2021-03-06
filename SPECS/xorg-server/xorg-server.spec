%global security_hardening nonow
Summary:	The Xorg Server
Name:		xorg-server
Version:	1.19.1
Release:	2%{?dist}
License:	MIT
URL:		http://www.x.org/
Group:		User Interface/X System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.x.org/pub/individual/xserver/%{name}-%{version}.tar.bz2
%define sha1 xorg-server=13c81e0ebb6ac1359a611d0503805c6dc0315477
Source1:	10-evdev.conf
BuildRequires:	xkeyboard-config xorg-fonts pixman-devel openssl-devel mesa-devel libxkbfile-devel libXfont2-devel libepoxy-devel xcb-util-keysyms-devel expat-devel
Requires:	xkeyboard-config xorg-fonts pixman openssl mesa libxkbfile libXfont2 libepoxy xcb-util-keysyms expat
%description
The Xorg Server is the core of the X Window system.
%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
Requires:	pixman-devel openssl-devel mesa-devel libxkbfile-devel libXfont2-devel libepoxy-devel xcb-util-keysyms-devel
%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' hw/xfree86/common/xf86Xinput.c
sed -i '/stat\.h/a #include <sys/sysmacros.h>' hw/xfree86/os-support/linux/lnx_init.c
sed -i '/stat\.h/a #include <sys/sysmacros.h>' hw/xfree86/xorg-wrapper.c

%configure \
		--enable-glamor          \
		--enable-install-setuid  \
		--enable-suid-wrapper    \
		--disable-systemd-logind \
		--with-xkb-output=/var/lib/xkb
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/etc/X11/xorg.conf.d &&
mkdir -pv %{buildroot}/etc/sysconfig &&
cat >> %{buildroot}/etc/sysconfig/createfiles << "EOF"
/tmp/.ICE-unix dir 1777 root root
/tmp/.X11-unix dir 1777 root root
EOF
cp %{SOURCE1} %{buildroot}/usr/share/X11/xorg.conf.d/
%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/pkgconfig
%exclude %{_prefix}/src/
%{_localstatedir}/*
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig
%changelog
* Thu Feb 13 2020 Alexey Makhalov <amakhalov@vmware.com> 1.19.1-2
- Added 10-evdev.conf conf file.
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 1.19.1-1
- Version update
* Wed May 20 2015 Alexey Makhalov <amakhalov@vmware.com> 1.17.1-1
- Initial version
