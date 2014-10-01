# based on PLD Linux spec git://git.pld-linux.org/packages/ppp.git
Summary:	ppp daemon package for Linux
Name:		ppp
Version:	2.4.7
Release:	1
License:	distributable
Group:		Networking/Daemons
Source0:	ftp://ftp.samba.org/pub/ppp/%{name}-%{version}.tar.gz
# Source0-md5:	78818f40e6d33a1d1de68a1551f6595a
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
Patch4:		%{name}-pidfile-owner.patch
Patch5:		%{name}-rp-pppoe-macaddr.patch
Patch6:		%{name}d-2.4.2-chapms-strip-domain.patch
Patch7:		%{name}-openssl.patch
Patch8:		%{name}-lib64.patch
URL:		http://www.samba.org/ppp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
Requires:	pam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the daemon and documentation for PPP support. It requires a
kernel greater than 2.2.11 which is built with PPP support. The
default kernels include PPP support as a module. This version supports
IPv6, too.

%package devel
Summary:	Stuff needed to build plugins for pppd
Group:		Development/Libraries

%description devel
Development files needed to build plugins for pppd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%ifarch %{x8664}
%patch8 -p1
%endif

%build
# note: not autoconf configure
%configure
%{__make}				\
	CC="%{__cc}"			\
	COPTS="%{rpmcflags}"		\
	OPTLDFLAGS="%{rpmldflags}"	\
	OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8}}	\
	$RPM_BUILD_ROOT{%{_sysconfdir}/{pam.d,ppp/peers},/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/pon
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/poff
install debian/plog $RPM_BUILD_ROOT%{_bindir}

install etc.ppp/chap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/pap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options.ttyXX $RPM_BUILD_ROOT%{_sysconfdir}/ppp

> $RPM_BUILD_ROOT/var/log/ppp.log

rm -f scripts/README

cd $RPM_BUILD_ROOT%{_libdir}/pppd
ln -s %{version}* plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux debian/README.debian scripts
%doc debian/win95.ppp README.MSCHAP8* FAQ debian/ppp-2.3.0.STATIC.README
%doc README.MPPE README.pppoe README.cbcp README.pwfd

%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/*.*
%dir %{_sysconfdir}/ppp/peers

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/pppd/*.*/minconn.so
%attr(755,root,root) %{_libdir}/pppd/*.*/openl2tp.so
%attr(755,root,root) %{_libdir}/pppd/*.*/pass*.so
%attr(755,root,root) %{_libdir}/pppd/*.*/pppoatm.so
%attr(755,root,root) %{_libdir}/pppd/*.*/pppol2tp.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rad*.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rp-pppoe.so
%attr(755,root,root) %{_libdir}/pppd/*.*/winbind.so

%attr(755,root,root) %{_sbindir}/chat
%attr(755,root,root) %{_sbindir}/ppp*
%{_libdir}/pppd/plugins

%{_mandir}/man8/*

%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/*-secrets
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ppp
%attr(640,root,root) %ghost /var/log/ppp.log
%config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/options*

%files devel
%defattr(644,root,root,755)
%{_includedir}/pppd

