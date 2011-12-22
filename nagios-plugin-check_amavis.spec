%define		plugin	check_amavis
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin to check amavisd-new daemon
Name:		nagios-plugin-%{plugin}
Version:	1.1
Release:	1
License:	?
Group:		Networking
# Source0Download:	http://exchange.nagios.org/components/com_mtree/attachment.php?link_id=1257&cf_id=24#/%{plugin}.pl
Source0:	%{plugin}.pl
# Source0-md5:	d6505313047810f0c907b784d70f31d7
Source1:	%{plugin}.cfg
URL:		http://exchange.nagios.org/directory/Plugins/Anti-2DVirus/Amavis/check_amavis/details
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
check_amavis checks if amavisd-new daemon is working and if its
antivirus engine is working. This check talks with amavisd-new daemon.
It tests if the daemon is up and if it's able to scan an email with a
virus (EICAR test virus is sent).

Please note that if amavisd-new is run on a different machine, you
should enable the connection from nagios ip address (take a look at
amavisd.conf).

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{SOURCE0} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
