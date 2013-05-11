# TODO
# - initscript
Summary:	An Open Source MQTT v3.1 Broker
Name:		mosquitto
Version:	1.1.3
Release:	0.1
License:	BSD
Group:		Applications
Source0:	http://mosquitto.org/files/source/%{name}-%{version}.tar.gz
# Source0-md5:	fd0cae17221d778b0a002c31e6c3de9e
URL:		http://mosquitto.org/
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sqlite3-devel >= 3.5
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(mosquitto)
Provides:	user(mosquitto)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mosquitto is an open source (BSD licensed) message broker that
implements the MQ Telemetry Transport protocol version 3.1. MQTT
provides a lightweight method of carrying out messaging using a
publish/subscribe model. This makes it suitable for "machine to
machine" messaging such as with low power sensors or mobile devices
such as phones, embedded computers or micro-controllers like the
Arduino.

%package clients
Summary:	Mosquitto command line pub/sub clients
Group:		Applications/Networking
Requires:	libmosquitto = %{version}-%{release}

%description clients
This is two MQTT version 3 clients. The first can publish messages to
a broker, the second can subscribe to multiple topics on a broker.

%package -n libmosquitto
Summary:	MQTT C client library
Group:		Development/Libraries

%description -n libmosquitto
This is a library that provides a means of implementing MQTT version 3
clients. MQTT provides a lightweight method of carrying out messaging
using a publish/subscribe model.

%package -n libmosquitto-devel
Summary:	MQTT C client library development files
Group:		Development/Libraries
Group:		Development/Libraries
Requires:	libmosquitto = %{version}-%{release}

%description -n libmosquitto-devel
This is a library that provides a means of implementing MQTT version 3
clients. MQTT provides a lightweight method of carrying out messaging
using a publish/subscribe model.

%package -n libmosquittopp
Summary:	MQTT C++ client library
Group:		Development/Libraries

%description -n libmosquittopp
This is a library that provides a means of implementing MQTT version 3
clients. MQTT provides a lightweight method of carrying out messaging
using a publish/subscribe model.

%package -n libmosquittopp-devel
Summary:	MQTT C++ client library development files
Group:		Development/Libraries
Requires:	libmosquittopp = %{version}-%{release}

%description -n libmosquittopp-devel
This is a library that provides a means of implementing MQTT version 3
clients. MQTT provides a lightweight method of carrying out messaging
using a publish/subscribe model.

%package -n python-%{name}
Summary:	MQTT Python client library
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n python-%{name}
This is a library that provides a means of implementing MQTT version 3
clients. MQTT provides a lightweight method of carrying out messaging
using a publish/subscribe model.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DUSE_LIBWRAP:BOOL=ON \
	..
%{__make}
cd ..

cd lib/python
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/*.example

cd lib/python
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root $RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 293 -r mosquitto
%useradd -u 293 -r -g mosquitto -d %{_sysconfdir}/%{name} -s /sbin/nologin -c "Mosquitto Broker" mosquitto

if [ "$1" = "0" ]; then
	%userremove mosquitto
	%groupremove mosquitto
fi

%post	-n libmosquitto -p /sbin/ldconfig
%postun	-n libmosquitto -p /sbin/ldconfig

%post	-n libmosquittopp -p /sbin/ldconfig
%postun	-n libmosquittopp -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt readme.txt *.example
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(755,root,root) %{_bindir}/mosquitto_passwd
%attr(755,root,root) %{_sbindir}/mosquitto
%{_mandir}/man1/mosquitto_passwd.1*
%{_mandir}/man5/mosquitto.conf.5*
%{_mandir}/man7/mosquitto-tls.7*
%{_mandir}/man7/mqtt.7*
%{_mandir}/man8/mosquitto.8*

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mosquitto_pub
%attr(755,root,root) %{_bindir}/mosquitto_sub
%{_mandir}/man1/mosquitto_pub.1*
%{_mandir}/man1/mosquitto_sub.1*

%files -n libmosquitto
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmosquitto.so.*.*.*
%ghost %{_libdir}/libmosquitto.so.1

%files -n libmosquitto-devel
%defattr(644,root,root,755)
%{_mandir}/man3/libmosquitto.3*
%{_libdir}/libmosquitto.so
%{_includedir}/mosquitto.h
%{_includedir}/mosquitto_plugin.h

%files -n libmosquittopp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmosquittopp.so.*.*.*
%ghost %{_libdir}/libmosquittopp.so.1

%files -n libmosquittopp-devel
%defattr(644,root,root,755)
%{_libdir}/libmosquittopp.so
%{_includedir}/mosquittopp.h

%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitescriptdir}/mosquitto.py[co]
%{py_sitescriptdir}/mosquitto-%{version}-*.egg-info
