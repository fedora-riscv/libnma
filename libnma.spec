%global gtk3_version    %(pkg-config --modversion gtk+-3.0 2>/dev/null || echo bad)
%global gtk4_version    %(pkg-config --modversion gtk4 2>/dev/null || echo bad)
%global glib2_version   %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global nm_version      1:1.8.0

%if 0%{?fedora} > 31 || 0%{?rhel} > 8
%bcond_with libnma_gtk4
%else
%bcond_without libnma_gtk4
%endif

Name:           libnma
Summary:        NetworkManager GUI library
Version:        1.8.26
Release:        1%{?dist}
License:        GPLv2+
URL:            https://gitlab.gnome.org/GNOME/libnma/
Source0:        https://download.gnome.org/sources/libnma/1.8/%{name}-%{version}.tar.xz

BuildRequires:  NetworkManager-libnm-devel >= %{nm_version}
BuildRequires:  ModemManager-glib-devel >= 1.0
BuildRequires:  glib2-devel >= 2.32
BuildRequires:  gtk3-devel >= 3.10
%if %{with libnma_gtk4}
BuildRequires:  gtk4-devel >= 3.96
%endif
BuildRequires:  gobject-introspection-devel >= 0.10.3
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig
BuildRequires:  meson
BuildRequires:  gtk-doc
BuildRequires:  iso-codes-devel
BuildRequires:  gcr-devel
BuildRequires:  mobile-broadband-provider-info-devel

%description
This package contains the library used for integrating GUI tools with
NetworkManager.


%package devel
Summary:        Header files for NetworkManager GUI library
Requires:       NetworkManager-libnm-devel >= %{nm_version}
Obsoletes:      NetworkManager-gtk-devel < 1:0.9.7
Requires:       libnma = %{version}-%{release}
Requires:       gtk3-devel
Requires:       pkgconfig

%description devel
This package contains header and pkg-config files to be used for integrating
GUI tools with NetworkManager.


%package gtk4
Summary:        Experimental GTK 4 version of NetworkManager GUI library
Requires:       gtk4 >= %{gtk4_version}
Requires:       mobile-broadband-provider-info >= 0.20090602

%description gtk4
This package contains the experimental GTK4 version of library used for
integrating GUI tools with NetworkManager.


%package gtk4-devel
Summary:        Header files for exerimental GTK4 version of NetworkManager GUI library
Requires:       NetworkManager-libnm-devel >= %{nm_version}
Requires:       libnma = %{version}-%{release}
Requires:       gtk4-devel
Requires:       pkgconfig

%description gtk4-devel
This package contains the experimental GTK4 version of header and pkg-config
files to be used for integrating GUI tools with NetworkManager.


%prep
%autosetup -p1


%build
%meson \
        -Dgcr=true \
        -Ddisable-static=true \
%if %{with libnma_gtk4}
        -Dlibnma_gtk4=true
%else
        -Dlibnma_gtk4=false
%endif
%meson_build


%install
%meson_install
%find_lang %{name}


%check
%meson_test


%ldconfig_scriptlets -n libnma
%ldconfig_scriptlets -n libnma-gtk4


%files -f %{name}.lang
%{_libdir}/libnma.so.*
%{_libdir}/girepository-1.0/NMA-1.0.typelib
%doc NEWS CONTRIBUTING
%license COPYING


%files devel
%{_includedir}/libnma
%{_libdir}/pkgconfig/libnma.pc
%{_libdir}/libnma.so
%{_datadir}/gir-1.0/NMA-1.0.gir
%{_datadir}/gtk-doc


%if %{with libnma_gtk4}
%files gtk4
%{_libdir}/libnma-gtk4.so.*
%{_libdir}/girepository-1.0/NMA4-1.0.typelib


%files gtk4-devel
%{_includedir}/libnma
%{_libdir}/pkgconfig/libnma-gtk4.pc
%{_libdir}/libnma-gtk4.so
%{_datadir}/gir-1.0/NMA4-1.0.gir
%endif


%changelog
* Fri Oct 18 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.26-1
- Initial package split from nm-connection-editor
