Name:           ogdi
Version:        3.2.1
Release:        3
Summary:        Open Geographic Datastore Interface
License:        BSD
URL:            http://ogdi.sourceforge.net/
# https://github.com/libogdi/ogdi/archive/ogdi_3_2_1.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        http://ogdi.sourceforge.net/ogdi.pdf

#To modify sprintf without a format string
Patch0000:      ogdi-3.2.0.beta2-sailer.patch
#To switch to libtirpc
Patch0001:      ogdi-3.2.1-cleanup.patch
#https://github.com/libogdi/ogdi/pull/6/
Patch0002:      ogdi-3.2.1-rpc.patch
Patch0003:      ogdi-3.2.1-rpc-flags.patch

BuildRequires:  gcc unixODBC-devel zlib-devel expat-devel
BuildRequires:  proj-devel tcl-devel libtirpc-devel

%description
OGDI is an open geographic data storage interface. OGDI is an application
programming interface (API) that uses standardized access methods in combination
with GIS software packages (the application) and various geospatial data products.
OGDI uses a client / server architecture to facilitate the dissemination of
geospatial data products on any TCP / IP network, and uses a driver-oriented
approach to facilitate access to several geospatial data products / formats.

%package devel
Summary:        OGDI header files and documentation
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig zlib-devel expat-devel proj-devel

%description devel
OGDI header files and developer's documentation.

%package odbc
Summary:        ODBC driver for OGDI
Requires:       %{name} = %{version}-%{release}

%description odbc
ODBC driver for OGDI.

%package tcl
Summary:        TCL wrapper for OGDI
Requires:       %{name} = %{version}-%{release}

%description tcl
TCL wrapper for OGDI.

%prep
%autosetup -p1 -n %{name}-ogdi_3_2_1
cp -p %{SOURCE1} .

%build
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
INST_LIB=%{_libdir}/;export INST_LIB
export CFG=debug

export CFLAGS="$RPM_OPT_FLAGS -DDONT_TD_VOID -DUSE_TERMIO"
%configure --with-binconfigs --with-expat \
           --with-proj --with-zlib

make
make -C ogdi/tcl_interface \
          TCL_LINKLIB="-ltcl"

make -C contrib/gdal

make -C ogdi/attr_driver/odbc \
          ODBC_LINKLIB="-lodbc"

%install
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET

make install INST_INCLUDE=%{buildroot}%{_includedir}/%{name} \
        INST_LIB=%{buildroot}%{_libdir} INST_BIN=%{buildroot}%{_bindir}

make install -C ogdi/tcl_interface INST_LIB=%{buildroot}%{_libdir} 
make install -C contrib/gdal INST_LIB=%{buildroot}%{_libdir}
make install -C ogdi/attr_driver/odbc INST_LIB=%{buildroot}%{_libdir}
rm %{buildroot}%{_bindir}/example?

touch -r ogdi-config.in ogdi-config

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m 644 ogdi.pc %{buildroot}%{_libdir}/pkgconfig/
install -p -m 755 ogdi-config %{buildroot}%{_bindir}/ogdi-config-64

cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | aarch64 )
ogdi-config-64 \${*}
;;
*)
ogdi-config-32 \${*}
;;
esac
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}-config
touch -r ogdi-config.in %{buildroot}%{_bindir}/%{name}-config

%files
%doc LICENSE NEWS ChangeLog README
%{_bindir}/gltpd
%{_bindir}/ogdi_*
%{_libdir}/libogdi.so.*
%dir %{_libdir}/ogdi
%exclude %{_libdir}/%{name}/{liblodbc.so,libecs_tcl.so}
%{_libdir}/%{name}/lib*.so

%files devel
%doc ogdi.pdf
%doc ogdi/examples/example1/{example1.c,example2.c}
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-64
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/libogdi.so

%files odbc
%{_libdir}/%{name}/liblodbc.so

%files tcl
%{_libdir}/%{name}/libecs_tcl.so


%changelog
* Wed Mar 04 2020 yangjian<yangjian79@huawei.com> - 3.2.1-3
- Package init