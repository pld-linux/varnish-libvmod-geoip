#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	geoip
Summary:	GeoIP Varnish module by Varnish Software
Name:		varnish-libvmod-%{vmod}
Version:	0.2
Release:	2
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-geoip/archive/libvmod-%{vmod}-%{version}.tar.gz
# Source0-md5:	482204cf88cd5fe4302d14daf07d48ac
URL:		https://github.com/varnish/libvmod-geoip
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	varnish-source >= 3.0
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Varnish GeoIP Lookup Module

This Varnish module exports functions to look up GeoIP country codes.

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libvmod-%{vmod}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man3/vmod_%{vmod}.3*
