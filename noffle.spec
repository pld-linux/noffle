Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP przeznaczony dla niedu�ych serwer�w
Name:		noffle
Version:	1.0.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(cs):	S��ov�/D�moni
Group(da):	Netv�rks/D�moner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	R�seau/Serveurs
Group(is):	Net/P�kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	����/������
Group(sl):	Omre�ni/Stre�niki
Group(sv):	N�tverk/Demoner
Group(uk):	������/������
Source0:	http://noffle.sourceforge.net/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}.DESTDIR.patch
URL:		http://noffle.sourceforge.net
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
Noffle to serwer grup dyskusyjnych usenet zoptymalizowany pod k�tem
kilku u�ytkownik�w i wolnego ��cza komutowanego do internetu.
Zachowuje si� on jako serwer dla klient�w uruchamianych na maszynie
lokalnej, a wiadomo�ci �ci�ga ��cz�c si� jako klient do zdalnego
serwera.

%prep
%setup -q
%patch0 -p0
#%patch1 -p0

	#CFLAGS="%{rpmcflags} -DHAVE_POSIX_REGCOMP" \
%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
%{configure} 			\
	--prefix=/usr 		\
	--sysconfdir=%{_sysconfdir}

%{__make}

#	DESTDIR=$RPM_BUILD_ROOT 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_var}/spool/news

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DOCDIR=$RPM_BUILD_ROOT/usr/share/doc/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

gzip -9nf README TODO NEWS INSTALL AUTHORS

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
%doc *.gz
%config %dir %attr(770,root,news) %{_sysconfdir}/noffle
%ghost %attr(664,news,news) %{_sysconfdir}/noffle/*
#%attr(750,root,news) %{_sbindir}/*
%attr(2770,news,news) %{_var}/spool/news/
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
%{_mandir}/man1/*
%{_mandir}/man5/*