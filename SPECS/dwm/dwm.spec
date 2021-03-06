Summary:	dwm is a dynamic window manager for X
Name:		dwm
Version:	6.2
Release:	1%{?dist}
License:	MIT/X
URL:		https://dwm.suckless.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://dl.suckless.org/dwm/dwm-6.2.tar.gz
%define sha1 dwm=3b73a7830b060f46cb9165ea951be7c08f6eae33
Source1:	dwm.xinitrc
BuildRequires:	libXinerama-devel libXft-devel xfontconfig-devel libX11-devel
Requires:	xorg-server libXinerama libXft xfontconfig libX11
%description
dwm is a dynamic window manager for X
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
install -vdm 755 %{buildroot}/etc/skel
cp %{SOURCE1} %{buildroot}/etc/skel/.xinitrc

%post
if [ $1 -eq 1 ] ; then
    if [ ! -f "/root/.xinitrc" ] ; then
        cp /etc/skel/.xinitrc /root/.xinitrc
    fi
fi

%files
%defattr(-,root,root)
%{_sysconfdir}/skel/.xinitrc
%{_bindir}/*
%{_mandir}/*
%changelog
* Wed Jun 12 2019 Alexey Makhalov <amakhalov@vmware.com> 6.2-1
- initial version
