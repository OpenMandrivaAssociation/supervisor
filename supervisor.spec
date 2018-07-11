Summary:	A System for Allowing the Control of Process State on UNIX
Name:		supervisor
#Version:	3.0
Version:	4.0
%define		prever 20180710
Release:	1

License:	ZPLv2.1 and BSD and MIT
Group:		System/Base
URL:		http://supervisord.org
Source0:	http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}%{?prever}.tar.gz
#Source0:	http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
#git archive --prefix=supervisor-4.0`date +%Y%m%d`/ -o supervisor-4.0`date +%Y%m%d`.tar.gz HEAD
#Source1:	supervisord.init
Source1:	supervisord.conf
Source2:        supervisor.logrotate
Source3:	supervisord.service
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools

Requires:	python-meld3 >= 0.6.5
Requires:	python-setuptools
Requires(preun): /bin/systemctl
Requires(postun): /bin/systemctl


%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q -n %{name}-%{version}%{?prever}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_sysconfdir}/supervisord.d
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d/
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}/lib/systemd/system
chmod 770 %{buildroot}/%{_localstatedir}/log/%{name}
install -p -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/supervisord.conf
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
install -p -m 644 %{SOURCE3} %{buildroot}/lib/systemd/system/supervisord.service

sed -i s'/^#!.*//' $( find %{buildroot}/%{python_sitelib}/supervisor/ -type f)

rm -rf %{buildroot}/%{python_sitelib}/supervisor/meld3/
rm -f %{buildroot}%{_prefix}/doc/*.txt

%clean
rm -rf %{buildroot}

%post
/bin/systemctl enable %{name}d || :
/bin/systemctl start %{name}d || :

%preun
if [ $1 = 0 ]; then
    /bin/systemctl stop supervisord > /dev/null 2>&1 || :
    /bin/systemctl disable  %{name}d || :
    /bin/rm -f /lib/systemd/system/supervisord.service
fi

%files
%defattr(-,root,root,-)
%doc README.rst LICENSES.txt CHANGES.txt COPYRIGHT.txt
%dir %{_localstatedir}/log/%{name}
%{python_sitelib}/*
%{_bindir}/supervisor*
%{_bindir}/echo_supervisord_conf
%{_bindir}/pidproxy
/lib/systemd/system/supervisord.service

%config(noreplace) %{_sysconfdir}/supervisord.conf
%dir %{_sysconfdir}/supervisord.d
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor


%changelog
* Tue Nov 01 2011 Alexander Khrukin <akhrukin@mandriva.org> 3.0-1mdv2012.0
+ Revision: 709304
- imported package supervisor

