%global		_disable_ld_no_undefined	1
%global		module		Bcps

Name:		coin-or-%{module}

Summary:	Part of the COIN High Performance Parallel Search Framework
Version:	0.93.12
Release:	2%{?dist}
License:	EPL
URL:		https://projects.coin-or.org/CHiPPS
Source0:	http://www.coin-or.org/download/pkgsource/CHiPPS/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Alps-devel
BuildRequires:	coin-or-Cgl-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

# Remove deprecated doxygen option to avoid doxygen verbosity about it
Patch2:		%{name}-doxygen.patch

%description
BiCePS is one of the libraries that make up the CHiPPS (COIN High Performance
Parallel Search Framework) library hierarchy. It implements that data-handling
functions needed to support development of many types of relaxation-based
branch-and-bound algorithms, especially for solving mathematical programs. It
is intended to capture the implementation of methods common to all such
algorithms without assuming anything about the structure of the mathematical
program or the bounding method used. BLIS, which is another layer built on top
of BiCePS, is a concretization of Bcps for the case of mixed integer linear
programs. DIP is another implementation being developed using BLIS that
implements a decomposition-based bounding procedure.

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
make %{?_smp_mflags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
make test

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/bcps_addlibs.txt
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Wed Mar 12 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.12-2
- Remove deprecated doxygen option (#894591#c4).

* Sun Mar  9 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.12-1
- Update to latest upstream release.

* Sat Mar  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.11-1
- Update to latest upstream release.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> -  0.93.6-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.4-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.4-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.4-1
- Rename package to coin-or-Bcps.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.4-1
- Initial coinor-Bcps spec.
