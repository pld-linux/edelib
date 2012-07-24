#
# Conditional build:
%bcond_without	apidocs		# don't build documentation
%bcond_without	static_libs	# don't build static library
#
Summary:	edelib library for EDE
Summary(pl.UTF-8):	Biblioteka pomocnicza dla EDE
Name:		edelib
Version:	2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://download.sourceforge.net/ede/%{name}-%{version}.tar.gz
# Source0-md5:	4964c7395a097bf747ebf9da1f836e6e
Patch0:		%{name}-ksh.patch
Patch1:		%{name}-am.patch
URL:		http://equinox-project.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fltk-devel >= 1.1.7
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
Requires:	glib2 >= 1:2.26.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
edelib is small and portable C++ library for EDE (Equinox Desktop Environment).

Aims are to provide enough background for easier EDE components construction
and development.

%description -l pl.UTF-8
edelib jest małą przenośną biblioteką C++ dla środowiska EDE.

Jej celem jest dostarczenie wystarczającej podstawy dla konstruowania i rozwijania
komponentów środowiska EDE.

%package devel
Summary:	edelib header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki edelib
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for edelib-based programs development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów opartych o edelib.

%package static
Summary:	Static edelib library
Summary(pl.UTF-8):	Statyczna biblioteka edelib
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static edelib library.

%description static -l pl.UTF-8
Statyczna biblioteka edelib.

%package apidocs
Summary:	edelib API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki edelib
Group:		Documentation

%description apidocs
edelib API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki edelib.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_static_libs:--disable-static} \
	--enable-shared

%{__make} V=1
%if %{with apidocs}
%{__make} html V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedelib.so.2
%attr(755,root,root) %ghost %{_libdir}/libedelib_dbus.so.2
%attr(755,root,root) %ghost %{_libdir}/libedelib_gui.so.2
%dir %{_libdir}/edelib
%{_libdir}/edelib/sslib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedelib.so
%attr(755,root,root) %{_libdir}/libedelib_dbus.so
%attr(755,root,root) %{_libdir}/libedelib_gui.so
%{_pkgconfigdir}/*.pc
%{_includedir}/edelib

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
