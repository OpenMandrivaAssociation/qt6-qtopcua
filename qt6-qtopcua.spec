#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtopcua
Version:	6.12.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
# Qt does not publish this module on download.qt.io. The tag archive
# unpacks as qtopcua-<version>.
Source0:	https://github.com/qt/qtopcua/archive/refs/tags/v%{version}%{?beta:-%{beta}}.tar.gz#/qtopcua-%{version}%{?beta:-%{beta}}.tar.gz
Group:		System/Libraries
Summary:	Qt %{major} OPC UA module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}CorePrivate)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}NetworkPrivate)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	qt%{major}-cmake
License:	(LGPLv3/GPLv3/GPLv2) and MPLv2.0 and CC0 and CC-BY-SA and BSD and Apache and MIT
# Library headers are LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
# (or commercial). The open62541 backend is the bundled 1.5.7
# amalgamation (MPL-2.0 AND CC0-1.0 AND CC-BY-SA-4.0 AND BSD-3-Clause
# AND Apache-2.0 AND MIT). Cooker has no open62541 package, and the
# plugin is written against that copy with OpenSSL encryption enabled,
# so the system library is not used.

%patchlist
# OpenSSL 4 makes X509_NAME getters const and ASN1_STRING opaque.
# Certificate requests allocate a name and set it. The bundled
# open62541 application-URI check uses ASN1_STRING accessors.
qtopcua-6.12.0-openssl-4.patch

%description
Client library for the OPC UA industrial communication protocol, the
open62541 backend, and Qt Quick bindings.

The open62541 backend is the bundled 1.5.7 amalgamation. Cooker has no
open62541 package, and the plugin is built against that copy with
OpenSSL encryption enabled.

# dlopened by libQt6OpcUa; the ELF generator does not see that dependency
%define extra_files_OpcUa \
%{_qtdir}/plugins/opcua

%define extra_devel_files_OpcUa \
%{_qtdir}/bin/qopcuaxmldatatypes2cpp \
%{_qtdir}/sbom/*

%define extra_files_DeclarativeOpcua \
%{_qtdir}/qml/QtOpcUa

%define extra_devel_files_DeclarativeOpcua \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6DeclarativeOpcuaplugin*

%qt6libs OpcUa DeclarativeOpcua

%package examples
Summary:	Examples for the Qt %{major} OPC UA module
Group:		Development/KDE and Qt

%description examples
Examples for the Qt %{major} OPC UA module

%files examples
%{_qtdir}/examples/opcua

%prep
%autosetup -p1 -n qtopcua-%{version}%{?beta:-%{beta}}
%cmake -G Ninja \
	-DQT_BUILD_TESTS:BOOL=OFF \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
