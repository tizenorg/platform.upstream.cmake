Name:           cmake
Version:        2.8.10.2
Release:        1
License:        BSD-3-Clause
Summary:        Cross-platform make system
Url:            http://www.cmake.org
Group:          Platfrom Development/Tools
Source0:        http://www.cmake.org/files/v2.8/cmake-%{version}.tar.gz
Source1:        macros.cmake
Source2:        TizenCommon.cmake
BuildRequires:  fdupes
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  procps
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  gcc-c++

%description
CMake is used to control the software compilation process using simple platform
and compiler independent configuration files. CMake generates native makefiles
and workspaces that can be used in the compiler environment of your choice.
CMake is quite sophisticated: it is possible to support complex environments
requiring system configuration, pre-processor generation, code generation, and
template instantiation.


%prep
%setup -q -n cmake-%{version}

%build
export CXXFLAGS="$RPM_OPT_FLAGS"
export CFLAGS="$CXXFLAGS"
./configure \
    --prefix=%{_prefix} \
    --datadir=/share/%{name} \
    --docdir=/share/doc/packages/%{name} \
    --mandir=/share/man \
    --system-libs \
    --parallel=0%jobs \
    --no-qt-gui
make VERBOSE=1 %{?_smp_mflags}

%install
%make_install 
mkdir -p %{buildroot}%{_libdir}/cmake
find %{buildroot}/usr/share/cmake -type f -print0 | xargs -0 chmod 644
cp %{SOURCE2} %{buildroot}/%{_datadir}/%{name}/Modules

# Install cmake rpm macros
install -D -p -m 0644 %{S:1} \
  %{buildroot}%{_sysconfdir}/rpm/macros.cmake

fdupes %buildroot/usr/share/cmake

%docs_package

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake
%doc %{_datadir}/doc/packages/%{name}
%{_datadir}/aclocal/cmake.m4
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/%{name}
