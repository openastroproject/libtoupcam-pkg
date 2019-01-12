%define debug_package %{nil}

Name:           libtoupcam
Version:        1.33.13725
Release:        0
Summary:        Touptek camera support libraries
License:	GPLv2+
URL:            http://touptek.com/
Prefix:         %{_prefix}
Provides:       libtoupcam = %{version}-%{release}
Obsoletes:      libtoupcam < 1.33.13725
Source:         libtoupcam-%{version}.tar.gz
Patch0:         pkg-config.patch

%description
libtoupcam is a user-space driver for Touptek astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libtoupcam-devel = %{version}-%{release}
Obsoletes:      libtoupcam-devel < 1.33.13725

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libtoupcam.pc.in > libtoupcam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}

case %{_arch} in
  x86_64)
    cp linux/x64/libtoupcam.so %{buildroot}%{_libdir}/libtoupcam.so.%{version}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp inc/*.h %{buildroot}%{_includedir}
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp doc/* %{buildroot}%{_docdir}/%{name}-%{version}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/toupcam*.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_docdir}/%{name}-%{version}/*.html

%changelog
* Sun Jul 30 2017 James Fidell <james@openastroproject.org> - 1.33.13725-0
- Initial RPM release

