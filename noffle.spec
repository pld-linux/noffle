Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP przeznaczony dla niedu¿ych serwerów
Name:		noffle
Version:	1.0.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://noffle.sourceforge.net/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}.DESTDIR.patch
URL:		http://noffle.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires(post,postun):rc-inetd
Requires:	inetdaemon
Provides:	nntpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Noffle is a Usenet news server optimized for few users and low speed
dial-up connections to the Internet. It acts as a server to news
clients running on the local host, but gets its news feed by acting as
a client to a remote server.

%description -l pl
Noffle to serwer grup dyskusyjnych usenet zoptymalizowany pod k±tem
kilku u¿ytkowników i wolnego ³±cza komutowanego do internetu.
Zachowuje siê on jako serwer dla klientów uruchamianych na maszynie
lokalnej, a wiadomo¶ci ¶ci±ga ³±cz±c siê jako klient do zdalnego
serwera.

%prep
%setup -q
%patch0 -p0

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
	
install %{name}.conf.example $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
#rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README TODO NEWS INSTALL AUTHORS docs/FAQ docs/INTERNALS docs/NOTES
%config %dir %attr(770,root,news) %{_sysconfdir}/noffle
%ghost %attr(664,news,news) %{_sysconfdir}/noffle/*
%attr(640,root,news) %config %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
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
