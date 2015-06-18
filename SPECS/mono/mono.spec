%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac

Summary:	Open source implementation of Microsoft's .NET Framework.
Name:		mono
Version:	4.0.1
Release:	1
License:	MIT
URL:		http://www.mono-project.com
Group:		Applications/Internet
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.mono-project.com/sources/%{name}/%{name}-%{version}.44.tar.bz2
# This key was generated by Tom "spot" Callaway <tcallawa@redhat.com> on Dec 1, 2009
# by running the following command:
# sn -k mono.snk
# You should not regenerate this unless you have a really, really, really good reason.
Source1:	mono.snk
Patch0:		mono-4.0.0-ignore-reference-assemblies.patch
BuildRequires:	intltool gettext glib-devel tzdata libgdiplus-devel
#mono-core >= 4.0
Requires:	gettext glib libgdiplus

%define _use_internal_dependency_generator 0
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/redhat/find-provides && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}%{_prefix} %{buildroot}%{_bindir}/mono-find-provides; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/redhat/find-requires && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}%{_prefix} %{buildroot}%{_bindir}/mono-find-requires; } | sort | uniq | grep ^...'

%description
Mono is an open source implementation of Microsoft's .NET Framework based on the ECMA standards for C# and the Common Language Runtime.

%package core
Summary:	The Mono CIL runtime, suitable for running .NET code
Group:		Development/Languages
Requires:	libgdiplus
Provides:	mono(Mono.Cairo)
Provides:	mono(Mono.Posix)
Provides:	mono(Mono.Security)
Provides:	mono(System)
Provides:	mono(System.Core)
Provides:	mono(System.Drawing)
Provides:	mono(System.Data)
Provides:	mono(System.Design)
Provides:	mono(System.Configuration)
Provides:	mono(System.Runtime.Remoting)
Provides:	mono(System.Windows.Forms)
Provides:	mono(System.ComponentModel.Composition)
Provides:	mono(System.ComponentModel.DataAnnotations)
Provides:	mono(System.Data.Services.Client)
Provides:	mono(System.Runtime.Serialization)
Provides:	mono(System.Security)
Provides:	mono(System.ServiceModel)
Provides:	mono(System.Web)
Provides:	mono(System.Web.Mvc)
Provides:	mono(System.Web.Razor)
Provides:	mono(System.Web.Services)
Provides:	mono(System.Web.WebPages.Razor)
Provides:	mono(System.Xaml)
Provides:	mono(System.Xml)
Provides:	mono(System.Xml.Linq)
Provides:	mono(mscorlib)
Provides:	mono(monodoc)
Provides:	mono(ICSharpCode.SharpZipLib)
Provides:	mono(Microsoft.Build.Framework)
Provides:	mono(Microsoft.Build.Utilities.v4.0)
Provides:	mono(Microsoft.Build)
Provides:	mono(Microsoft.Build.Engine)
Provides:	mono(Microsoft.CSharp)
Provides:	mono(WindowsBase)

%description core
This package contains the core of the Mono runtime including its
Virtual Machine, Just-in-time compiler, C# compiler, security
tools and libraries (corlib, XML, System.Security, ZipLib,
I18N, Cairo and Mono.*).

%package devel
Summary: Development tools for Mono
Group: Development/Languages
Requires: mono-core = %{version}-%{release}

%description devel
This package completes the Mono developer toolchain with the mono profiler,
assembler and other various tools.

%package nunit
Summary:	NUnit Testing Framework
License:	zlib with acknowledgement
Group:		Development/Languages
Requires:	mono-core = %{version}-%{release}

%description nunit
NUnit is a unit-testing framework for all .Net languages. Initially
ported from JUnit, the current release, version 2.2, is the fourth
major release of this Unit based unit testing tool for Microsoft .NET.
It is written entirely in C# and has been completely redesigned to
take advantage of many .NET language features, for example
custom attributes and other reflection related capabilities. NUnit
brings xUnit to all .NET languages.

%package nunit-devel
Summary:	pkgconfig for nunit
Group:		Development/Libraries
Requires:	mono-core = %{version}-%{release}, pkg-config
Requires:	mono-nunit = %{version}-%{release}

%description nunit-devel
Development files for nunit

%package more
Summary: Provides all the files which are not in a core/nunit rpms.
Group: Development/Languages
Requires: mono-core = %{version}-%{release}
%description more
Provides all the files which are not in a core/nunit rpms.

%define gac_dll(dll)  %{_monogacdir}/%{1} \
  %{_monodir}/4.5/%{1}.dll \
  %{nil}
%define mono_bin(bin) %{_bindir}/%{1} \
  %{_monodir}/4.5/%{1}.exe \
  %{_monodir}/4.5/%{1}.exe.* \
  %{nil}

%prep
%setup -q 
%patch0	-p1
# modifications for Mono 4
sed -i "s#mono/2.0#mono/4.5#g" data/mono-nunit.pc.in
# Remove prebuilt binaries
#find . -name "*.dll" -not -path "./mcs/class/lib/monolite/*" -print -delete
#find . -name "*.exe" -not -path "./mcs/class/lib/monolite/*" -print -delete
#rm -rf mcs/class/lib/monolite/*

%build
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --disable-rpath \
            --with-moonlight=no

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

# copy the mono.snk key into /etc/pki/mono
mkdir -p %{buildroot}%{_sysconfdir}/pki/mono
install -p -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/mono/

# This was removed upstream:
# remove .la files (they are generally bad news)
rm -f %{buildroot}%{_libdir}/*.la
# remove Windows-only stuff
rm -rf %{buildroot}%{_monodir}/*/Mono.Security.Win32*
rm -f %{buildroot}%{_libdir}/libMonoSupportW.*
# remove .a files for libraries that are really only for us
rm %{buildroot}%{_libdir}/*.a
# remove libgc cruft
rm -rf %{buildroot}%{_datadir}/libgc-mono
# remove stuff that we don't package
rm -f %{buildroot}%{_bindir}/cilc
rm -f %{buildroot}%{_mandir}/man1/cilc.1*
rm -f %{buildroot}%{_monodir}/*/browsercaps-updater.exe*
rm -f %{buildroot}%{_monodir}/*/culevel.exe*
rm -f %{buildroot}%{_monodir}/2.0/cilc.exe*

rm -f %{buildroot}%{_monodir}/*/mscorlib.dll.so
rm -f %{buildroot}%{_monodir}/*/mcs.exe.so
rm -f %{buildroot}%{_monodir}/*/gmcs.exe.so
rm -rf %{buildroot}%{_monodir}/xbuild/Microsoft
rm -f %{buildroot}%{_monodir}/4.0/dmcs.exe.so
rm -rf %{buildroot}%{_bindir}/mono-configuration-crypto
rm -rf %{buildroot}%{_mandir}/man?/mono-configuration-crypto*

%find_lang mcs
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files core -f mcs.lang
%doc AUTHORS COPYING.LIB ChangeLog NEWS README.md
%{_bindir}/mono
%{_bindir}/mono-test-install
%{_bindir}/mono-gdb.py
%{_bindir}/mono-boehm
%{_bindir}/mono-service2
%{_bindir}/mono-sgen
%{_bindir}/mono-sgen-gdb.py
%{_libdir}/mono/lldb/mono.py*
%mono_bin csharp
%mono_bin cert-sync
%mono_bin chktrust
%mono_bin gacutil
%mono_bin ikdasm
%mono_bin lc
%{_bindir}/gacutil2
%{_bindir}/mcs
%{_monodir}/4.5/mcs.exe*
%mono_bin mozroots
%mono_bin pdb2mdb
%mono_bin setreg
%mono_bin sn
%{_bindir}/mono-heapviz
%{_bindir}/mprof-report
%{_mandir}/man1/certmgr.1.gz
%{_mandir}/man1/chktrust.1.gz
%{_mandir}/man1/gacutil.1.gz
%{_mandir}/man1/mcs.1.gz
%{_mandir}/man1/mono.1.gz
%{_mandir}/man1/mozroots.1.gz
%{_mandir}/man1/setreg.1.gz
%{_mandir}/man1/sn.1.gz
%{_mandir}/man5/mono-config.5.gz
%{_mandir}/man1/csharp.1.gz
%{_mandir}/man1/pdb2mdb.1.gz
%{_mandir}/man1/lc.1.gz
%{_mandir}/man1/mprof-report.1.gz
%{_libdir}/libMonoPosixHelper.so*
%dir %{_monodir}
%dir %{_monodir}/gac
%gac_dll Commons.Xml.Relaxng
%gac_dll ICSharpCode.SharpZipLib
%gac_dll Mono.Debugger.Soft
%{_monogacdir}/Mono.Cecil
%gac_dll cscompmgd
%gac_dll Microsoft.VisualC
%gac_dll Mono.C5
%gac_dll Mono.Cairo
%gac_dll Mono.CompilerServices.SymbolWriter
%gac_dll Mono.CSharp
%gac_dll System.Drawing
%gac_dll Mono.Management
%gac_dll Mono.Posix
%gac_dll Mono.Security
%gac_dll Mono.Simd
%gac_dll System
%gac_dll System.Configuration
%gac_dll System.Core
%gac_dll System.Security
%gac_dll System.Xml
%gac_dll Mono.Tasklets
%gac_dll System.Net
%gac_dll System.Xml.Linq
%dir %{_sysconfdir}/mono
%dir %{_sysconfdir}/mono/mconfig
%config (noreplace) %{_sysconfdir}/mono/config
%config (noreplace) %{_sysconfdir}/mono/2.0/machine.config
%config (noreplace) %{_sysconfdir}/mono/2.0/settings.map
%{_libdir}/libmono*-2.0.so.*
%{_libdir}/libmono-profiler-*.so.*
%config (noreplace) %{_sysconfdir}/mono/4.0/*.config
%config (noreplace) %{_sysconfdir}/mono/4.0/settings.map
%config (noreplace) %{_sysconfdir}/mono/4.0/DefaultWsdlHelpGenerator.aspx
%config (noreplace) %{_sysconfdir}/mono/4.5/DefaultWsdlHelpGenerator.aspx
%config (noreplace) %{_sysconfdir}/mono/4.5/machine.config
%config (noreplace) %{_sysconfdir}/mono/4.5/settings.map
%config (noreplace) %{_sysconfdir}/mono/4.5/web.config
%dir %{_sysconfdir}/mono/4.0
%{_bindir}/dmcs
%mono_bin ccrewrite
%{_monodir}/4.5/mscorlib.dll
%{_monodir}/4.5/mscorlib.dll.mdb
%gac_dll Microsoft.CSharp
%gac_dll System.Dynamic
%gac_dll Mono.Data.Tds
%gac_dll System.ComponentModel.Composition
%gac_dll System.EnterpriseServices
%gac_dll System.Data
%gac_dll System.Numerics
%gac_dll System.Runtime.Caching
%gac_dll System.Runtime.DurableInstancing
%gac_dll System.Transactions
%gac_dll System.Xaml
%gac_dll WebMatrix.Data
%gac_dll Mono.CodeContracts
%{_monodir}/mono-configuration-crypto/4.5/mono-config*
%{_monodir}/mono-configuration-crypto/4.5/Mono.Configuration.Crypto.dll*
%{_mandir}/man1/ccrewrite.1.gz
%gac_dll CustomMarshalers
%gac_dll I18N.West
%gac_dll I18N
%gac_dll System.Json
%gac_dll Mono.Parallel
%gac_dll System.Json.Microsoft
%{_monodir}/4.5/Facades/*.dll
%gac_dll System.IO.Compression
%gac_dll System.IO.Compression.FileSystem
%gac_dll System.Net.Http
%gac_dll System.Net.Http.WebRequest
%gac_dll System.Threading.Tasks.Dataflow

%files devel
%{_sysconfdir}/pki/mono/
%{_bindir}/mono-api-info
%{_monodir}/4.5/mono-api-info.exe
%{_monodir}/4.5/symbolicate.exe
%{_monodir}/4.5/symbolicate.exe.mdb
%mono_bin xbuild
%{_monodir}/4.5/xbuild.rsp
%mono_bin genxs
%{_monodir}/4.5/ictool*
%{_monodir}/4.5/mod*
%mono_bin al
%{_bindir}/al2
%mono_bin caspol
%mono_bin cert2spc
%mono_bin certmgr
%mono_bin dtd2rng
%mono_bin dtd2xsd
%mono_bin ilasm
%mono_bin installvst
%{_monodir}/4.5/installutil*
%mono_bin macpack
%mono_bin mkbundle
%mono_bin makecert
%mono_bin mono-cil-strip
%{_bindir}/mono-find-provides
%{_bindir}/mono-find-requires
%{_bindir}/monodis
%mono_bin monolinker
%mono_bin mono-shlib-cop
%mono_bin mono-xmltool
%mono_bin monop
%{_bindir}/monop2
%mono_bin permview
%{_bindir}/peverify
%{_bindir}/prj2make
%mono_bin resgen
%{_bindir}/resgen2
%mono_bin sgen
%mono_bin secutil
%mono_bin signcode
%mono_bin cccheck
%mono_bin crlupdate
%mono_bin mdbrebase
%{_prefix}/lib/mono-source-libs/
%{_bindir}/pedump
%{_mandir}/man1/resgen.1.gz
%{_mandir}/man1/al.1.gz
%{_mandir}/man1/cert2spc.1.gz
%{_mandir}/man1/dtd2xsd.1.gz
%{_mandir}/man1/genxs.1.gz
%{_mandir}/man1/ilasm.1.gz
%{_mandir}/man1/macpack.1.gz
%{_mandir}/man1/makecert.1.gz
%{_mandir}/man1/mkbundle.1.gz
%{_mandir}/man1/mono-cil-strip.1.gz
%{_mandir}/man1/monodis.1.gz
%{_datadir}/mono-2.0/mono/cil/cil-opcodes.xml
%{_mandir}/man1/monolinker.1.gz
%{_mandir}/man1/mono-shlib-cop.1.gz
%{_mandir}/man1/mono-xmltool.1.gz
%{_mandir}/man1/monop.1.gz
%{_mandir}/man1/permview.1.gz
%{_mandir}/man1/prj2make.1.gz
%{_mandir}/man1/secutil.1.gz
%{_mandir}/man1/sgen.1.gz
%{_mandir}/man1/signcode.1.gz
%{_mandir}/man1/xbuild.1.gz
%{_mandir}/man1/mono-api-info.1.gz
%{_mandir}/man1/cccheck.1.gz
%{_mandir}/man1/crlupdate.1.gz
%gac_dll PEAPI
%gac_dll Microsoft.Build
%gac_dll Microsoft.Build.Engine
%gac_dll Microsoft.Build.Framework
%{_monogacdir}/Microsoft.Build.Tasks.Core
%gac_dll Microsoft.Build.Tasks.v4.0
%gac_dll Microsoft.Build.Utilities.v4.0
%{_monogacdir}/Microsoft.Build.Utilities.Core
%{_monogacdir}/Microsoft.Build.Tasks.v12.0
%{_monogacdir}/Microsoft.Build.Utilities.v12.0
%gac_dll Mono.XBuild.Tasks
%gac_dll System.Windows
%gac_dll System.Xml.Serialization
%{_monodir}/4.5/Microsoft.Common.tasks
%{_monodir}/4.5/MSBuild/Microsoft.Build*
%{_monodir}/4.5/Microsoft.Build.xsd
%{_monodir}/4.5/Microsoft.CSharp.targets
%{_monodir}/4.5/Microsoft.Common.targets
%{_monodir}/4.5/Microsoft.VisualBasic.targets
%{_monodir}/xbuild/
%{_monodir}/xbuild-frameworks/
%{_libdir}/libikvm-native.so
%{_libdir}/libmono-profiler-*.so
%{_libdir}/libmono*-2.0.so
%{_libdir}/pkgconfig/dotnet.pc
%{_libdir}/pkgconfig/mono-cairo.pc
%{_libdir}/pkgconfig/mono.pc
%{_libdir}/pkgconfig/mono-2.pc
%{_libdir}/pkgconfig/monosgen-2.pc
%{_libdir}/pkgconfig/cecil.pc
%{_libdir}/pkgconfig/dotnet35.pc
%{_libdir}/pkgconfig/mono-lineeditor.pc
%{_libdir}/pkgconfig/mono-options.pc
%{_libdir}/pkgconfig/wcf.pc
%{_libdir}/pkgconfig/xbuild12.pc
%{_includedir}/mono-2.0/mono/jit/jit.h
%{_includedir}/mono-2.0/mono/metadata/*.h
%{_includedir}/mono-2.0/mono/utils/*.h
%{_includedir}/mono-2.0/mono/cil/opcode.def

%files nunit
%mono_bin nunit-console
%{_bindir}/nunit-console2
%{_bindir}/nunit-console4
%gac_dll nunit-console-runner
%gac_dll nunit.core
%gac_dll nunit.core.extensions
%gac_dll nunit.core.interfaces
%gac_dll nunit.framework
%gac_dll nunit.framework.extensions
%gac_dll nunit.mocks
%gac_dll nunit.util

%files nunit-devel
%{_libdir}/pkgconfig/mono-nunit.pc

%files more
#%files locale-extras
%gac_dll I18N.CJK
%gac_dll I18N.MidEast
%gac_dll I18N.Other
%gac_dll I18N.Rare
#%files extras
%mono_bin mono-service
%{_monogacdir}/mono-service
%gac_dll System.Configuration.Install
%gac_dll System.Management
%gac_dll System.Messaging
%gac_dll System.ServiceProcess
%gac_dll System.Runtime.Caching
%gac_dll System.Xaml
%gac_dll Mono.Messaging.RabbitMQ
%gac_dll Mono.Messaging
%gac_dll RabbitMQ.Client
%{_monodir}/4.5/RabbitMQ.Client.Apigen*
%{_mandir}/man1/mono-service.1.gz
#%files reactive
%gac_dll System.Reactive.Core
%gac_dll System.Reactive.Debugger
%gac_dll System.Reactive.Experimental
%gac_dll System.Reactive.Interfaces
%gac_dll System.Reactive.Linq
%gac_dll System.Reactive.Observable.Aliases
%gac_dll System.Reactive.PlatformServices
%gac_dll System.Reactive.Providers
%gac_dll System.Reactive.Runtime.Remoting
#%files reactive-winforms
%gac_dll System.Reactive.Windows.Forms
%gac_dll System.Reactive.Windows.Threading
#%files reactive-devel
%_libdir/pkgconfig/reactive.pc
#%files wcf
%gac_dll System.IdentityModel
%gac_dll System.IdentityModel.Selectors
%gac_dll System.ServiceModel
%gac_dll System.ServiceModel.Activation
%gac_dll System.ServiceModel.Discovery
%gac_dll System.ServiceModel.Routing
%gac_dll System.ServiceModel.Web
#%files web
%mono_bin disco
%mono_bin httpcfg
%mono_bin mconfig
%mono_bin soapsuds
%mono_bin svcutil
%mono_bin wsdl
%{_bindir}/wsdl2
%mono_bin xsd
%gac_dll Microsoft.Web.Infrastructure
%gac_dll Mono.Http
%gac_dll System.ComponentModel.DataAnnotations
%gac_dll System.Net.Http.Formatting
%gac_dll System.Runtime.Remoting
%gac_dll System.Runtime.Serialization.Formatters.Soap
%gac_dll System.Web
%gac_dll System.Web.Abstractions
%gac_dll System.Web.DynamicData
%gac_dll System.Web.Routing
%gac_dll System.Web.Services
%gac_dll System.Web.ApplicationServices
%gac_dll System.Web.Http
%gac_dll System.Web.Http.SelfHost
%gac_dll System.Web.Http.WebHost
%gac_dll System.Web.Razor
%gac_dll System.Web.WebPages
%gac_dll System.Web.WebPages.Deployment
%gac_dll System.Web.WebPages.Razor
%{_mandir}/man1/disco.1.gz
%{_mandir}/man1/httpcfg.1.gz
%{_mandir}/man1/mconfig.1.gz
%{_mandir}/man1/soapsuds.1.gz
%{_mandir}/man1/wsdl.1.gz
%{_mandir}/man1/xsd.1.gz
%config (noreplace) %{_sysconfdir}/mono/browscap.ini
%config (noreplace) %{_sysconfdir}/mono/2.0/Browsers/Compat.browser
%config (noreplace) %{_sysconfdir}/mono/4.0/Browsers/Compat.browser
%config (noreplace) %{_sysconfdir}/mono/4.5/Browsers/Compat.browser
%config (noreplace) %{_sysconfdir}/mono/2.0/DefaultWsdlHelpGenerator.aspx
%config (noreplace) %{_sysconfdir}/mono/mconfig/config.xml
%config (noreplace) %{_sysconfdir}/mono/2.0/web.config
#%files web-devel
%{_libdir}/pkgconfig/aspnetwebstack.pc
#%files winforms
%gac_dll Accessibility
%gac_dll Mono.WebBrowser
%gac_dll System.Design
%gac_dll System.Drawing.Design
%gac_dll System.Windows.Forms
%gac_dll System.Windows.Forms.DataVisualization
#%files mvc
%gac_dll System.Web.DynamicData
%gac_dll System.Web.Extensions
%gac_dll System.Web.Extensions.Design
%gac_dll System.Web.Mvc
#%files mvc-devel
%{_libdir}/pkgconfig/system.web.extensions.design_1.0.pc
%{_libdir}/pkgconfig/system.web.extensions_1.0.pc
%{_libdir}/pkgconfig/system.web.mvc.pc
%{_libdir}/pkgconfig/system.web.mvc2.pc
%{_libdir}/pkgconfig/system.web.mvc3.pc
#%files winfx
%gac_dll System.Data.Services.Client
%gac_dll WindowsBase
#%files data
%mono_bin sqlsharp
%mono_bin sqlmetal
%gac_dll System.Data
%gac_dll System.Data.DataSetExtensions
%gac_dll System.Data.Entity
%gac_dll System.Data.Linq
%gac_dll System.Data.Services
%gac_dll System.Data.Services.Client
%gac_dll System.DirectoryServices
%gac_dll System.DirectoryServices.Protocols
%gac_dll System.EnterpriseServices
%gac_dll System.Runtime.Serialization
%gac_dll System.Transactions
%gac_dll Mono.Data.Tds
%gac_dll Novell.Directory.Ldap
%gac_dll WebMatrix.Data
%{_mandir}/man1/sqlsharp.1.gz
#%files data-sqlite
%gac_dll Mono.Data.Sqlite
#%files data-oracle
%gac_dll System.Data.OracleClient
#%files -n ibm-data-db2
%gac_dll IBM.Data.DB2
#%files -n monodoc
%{_monogacdir}/monodoc
%{_monodir}/monodoc/*
%{_prefix}/lib/monodoc
%mono_bin mdoc
%{_bindir}/mod
%{_bindir}/mdoc-*
%{_bindir}/mdass*
%{_bindir}/mdval*
%{_bindir}/monodoc*
%{_mandir}/man1/md*
%{_mandir}/man1/monodoc*
%{_mandir}/man5/mdoc*
#%files -n monodoc-devel
%{_libdir}/pkgconfig/monodoc.pc

%changelog
*	Tue Jun 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.1.44-1
-	initial version
