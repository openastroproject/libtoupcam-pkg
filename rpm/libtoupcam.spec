%define debug_package %{nil}

Name:           libtoupcam
Version:        1.55.24621
Release:        1
Summary:        Touptek camera support libraries
License:	GPLv2+
URL:            http://touptek.com/
Prefix:         %{_prefix}
Provides:       libtoupcam = %{version}-%{release}
Obsoletes:      libtoupcam < 1.55.24621
Source:         libtoupcam-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libtoupcam is a user-space driver for Touptek astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libtoupcam-devel = %{version}-%{release}
Obsoletes:      libtoupcam-devel < 1.55.24621

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libtoupcam.pc.in > libtoupcam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mkdir -p %{buildroot}%{_udevrulesdir}

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
cp 70-touptek-cameras.rules %{buildroot}%{_udevrulesdir}

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_udevrulesdir}/*.rules

%files devel
%{_includedir}/toupcam*.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_docdir}/%{name}-%{version}/*.html

%changelog
* Sat Jan 6 2024 James Fidell <james@openastroproject.org> - 1.55.24621-1
- Update from upstream
* Mon Dec 25 2023 James Fidell <james@openastroproject.org> - 1.50.19728-1
- Update from upstream
* Wed Jun 30 2021 James Fidell <james@openastroproject.org> - 1.48.18081-1
- Update from upstream
* Wed Dec 2 2020 James Fidell <james@openastroproject.org> - 1.48.18042-1
- Update from upstream
* Mon May 19 2020 James Fidell <james@openastroproject.org> - 1.46.17118-1
- Update from upstream
* Mon May 18 2020 James Fidell <james@openastroproject.org> - 1.46.16880-1
- Update from upstream
* Fri Sep 12 2019 James Fidell <james@openastroproject.org> - 1.39.15529-1
- Update from upstream
* Sun Jul 30 2017 James Fidell <james@openastroproject.org> - 1.33.13725-1
- Update from upstream
* Sun Jul 30 2017 James Fidell <james@openastroproject.org> - 1.33.13725-0
- Update from upstream
* Sun Jul 30 2017 James Fidell <james@openastroproject.org> - 1.6.5660-0
- Initial RPM release
