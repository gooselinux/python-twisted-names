%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{python}-twisted-names
Version:        8.2.0
Release:        3.2%{?dist}
Summary:        Twisted DNS implementation
Group:          Development/Libraries
License:        MIT
URL:            http://www.twistedmatrix.com/trac/wiki/TwistedNames
Source0:        http://tmrc.mit.edu/mirror/twisted/Names/8.2/TwistedNames-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{python}-twisted-core >= 8.2.0
BuildRequires:  %{python}-devel
Requires:       %{python}-twisted-core >= 8.2.0

# a noarch-turned-arch package should not have debuginfo
%define debug_package %{nil}

%description
Twisted is an event-based framework for internet applications.

Twisted Names is both a domain name server as well as a client resolver
library. Twisted Names comes with an "out of the box" nameserver that can read
most BIND-syntax zone files as well as a simple Python-based configuration
format. Twisted Names can act as an authoritative server, perform zone
transfers from a master to act as a secondary, act as a caching nameserver, or
any combination of these. Twisted Names' client resolver library provides
functions to query for all commonly-used record types as well as a replacement
for the blocking gethostbyname() function provided by the Python stdlib socket
module.

%prep
%setup -q -n TwistedNames-%{version}

# Fix doc file deps
chmod -x doc/examples/*.py

%build
%{python} setup.py build

%install
rm -rf %{buildroot}

# This is a pure python package, but extending the twisted namespace from
# python-twisted-core, which is arch-specific, so it needs to go in sitearch
%{python} setup.py install -O1 --skip-build \
    --install-purelib %{python_sitearch} --root %{buildroot}

# See if there's any egg-info
if [ -f %{buildroot}%{python_sitearch}/Twisted*.egg-info ]; then
    echo %{buildroot}%{python_sitearch}/Twisted*.egg-info |
        sed -e "s|^%{buildroot}||"
fi > egg-info

%clean
rm -rf %{buildroot}

%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%files -f egg-info
%defattr(-,root,root,-)
%doc README LICENSE doc/* NEWS
%{python_sitearch}/twisted/names/
%{python_sitearch}/twisted/plugins/twisted_names.py*

%changelog
* Wed Jan 27 2010 David Malcolm <dmalcolm@redhat.com> - 8.2.0-3.2
- fix source URL

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 8.2.0-3.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Merge back changes from Paul Howarth.
- Make sure the scriplets never return a non-zero exit status.

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-5
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-4
- Rebuild for Python 2.6

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.4.0-3
- Fix the egg info, drop the pyver stuff.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-2
- Autorebuild for GCC 4.3

* Fri Aug 31 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.0-1
- updated to latest version

* Thu Dec 14 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.0-3
- add python-devel BR
- chmod the examples

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.0-2
- no longer ghost .pyo files
- rebuild dropin.cache

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.3.0-1
- new upstream release
- remove noarch
- remove dependency on flow

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-2
- disttag

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- final release

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a2
- prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- prep for split

