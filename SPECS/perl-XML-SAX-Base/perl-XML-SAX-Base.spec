Summary:        XML::SAX::Base module
Name:           perl-XML-SAX-Base
Version:        1.08
Release:        1
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/XML-SAX-Base
Source0:        http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-SAX-Base-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:	perl libxml2-devel zlib-devel
Requires:	perl libxml2 zlib

%description
Base class for Perl SAX drivers and filters.

%prep
%setup -q -n XML-SAX-Base-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
rm %{buildroot}%{perl_vendorlib}/x86_64-linux/auto/XML/SAX/Base/.packlist
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%{perl_vendorlib}
%{_mandir}

%changelog
*	Thu Jun 4 2015 Alexey Makhalov <amakhalov@vmware.com> 1.08-1
-	Initial version.



