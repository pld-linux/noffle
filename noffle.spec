Summary:	NNTP server for small sites
Summary(pl.UTF-8):	Serwer NNTP przeznaczony dla niedużych serwerów
Name:		noffle
Version:	1.0.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/noffle/%{name}-%{version}.tar.gz
# Source0-md5:	fe6b49a43e7fd0341b055d558e1a8202
Source1:	%{name}.inetd
Patch0:		%{name}.DESTDIR.patch
Patch1:		%{name}-overflows.patch
URL:		http://noffle.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	rc-inetd
Requires:	inetdaemon
Provides:	nntpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Noffle is a Usenet news server optimized for few users and low speed
dial-up connections to the Internet. It acts as a server to news
clients running on the local host, but gets its news feed by acting as
a client to a remote server.

%description -l pl.UTF-8
Noffle to serwer grup dyskusyjnych usenet zoptymalizowany pod kątem
kilku użytkowników i wolnego łącza komutowanego do internetu.
Zachowuje się on jako serwer dla klientów uruchamianych na maszynie
lokalnej, a wiadomości ściąga łącząc się jako klient do zdalnego
serwera.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_var}/spool/%{name}/{data,global,lock,outgoing,overview,requested}
touch $RPM_BUILD_ROOT%{_var}/spool/%{name}/{fetchlist,groupinfo.lastupdate}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DOCDIR=$RPM_BUILD_ROOT%{_datadir}/doc/%{name}

install %{name}.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
#rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README TODO NEWS INSTALL AUTHORS docs/FAQ docs/INTERNALS docs/NOTES
%attr(770,root,news) %dir %{_sysconfdir}/noffle
%attr(664,news,news) %ghost %{_sysconfdir}/noffle/*
%attr(640,root,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(750,root,news) %{_bindir}/noffle
%attr(2770,news,news) %dir %{_var}/spool/%{name}/data
%attr(2770,news,news) %dir %{_var}/spool/%{name}/global
%attr(2770,news,news) %dir %{_var}/spool/%{name}/lock
%attr(2770,news,news) %dir %{_var}/spool/%{name}/outgoing
%attr(2770,news,news) %dir %{_var}/spool/%{name}/overview
%attr(2770,news,news) %dir %{_var}/spool/%{name}/requested
%attr(2770,news,news) %dir %{_var}/spool/%{name}
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
%{_mandir}/man1/*
%{_mandir}/man5/*
