Summary:	A System for Allowing the Control of Process State on UNIX
Name:		supervisor
Version:	4.2.4
%define		prever 20180710
Release:	1

License:	ZPLv2.1 and BSD and MIT
Group:		System/Base
URL:		http://supervisord.org
Source0:	http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
#git archive --prefix=supervisor-4.0`date +%Y%m%d`/ -o supervisor-4.0`date +%Y%m%d`.tar.gz HEAD
#Source1:	supervisord.init
Source1:	supervisord.conf
Source2:        supervisor.logrotate
Source3:	supervisord.service
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:  python-setuptools
BuildRequires:	systemd

#Requires:	python-meld3 >= 0.6.5
Requires:	python-setuptools
Requires(preun): systemd


%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q -n %{name}-%{version}

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
mkdir -p %{buildroot}/%{_unitdir}
chmod 770 %{buildroot}/%{_localstatedir}/log/%{name}
install -p -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/supervisord.conf
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
install -p -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}/supervisord.service
install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable supervisord.service
EOF

sed -i s'/^#!.*//' $( find %{buildroot}/%{python_sitelib}/supervisor/ -type f)


%files
%defattr(-,root,root,-)
%doc README.rst LICENSES.txt COPYRIGHT.txt
%dir %{_localstatedir}/log/%{name}
%{python_sitelib}/*
%{_bindir}/supervisor*
%{_bindir}/echo_supervisord_conf
%{_bindir}/pidproxy
%{_unitdir}/supervisord.service
%{_presetdir}/86-supervisor.preset

%config(noreplace) %{_sysconfdir}/supervisord.conf
%dir %{_sysconfdir}/supervisord.d
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor

