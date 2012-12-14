
%global _use_internal_dependency_generator 0
%global __find_requires /usr/lib/rpm/ocaml-find-requires.sh
%global __find_provides /usr/lib/rpm/ocaml-find-provides.sh

# These is the exact upstream version we are packaging
%define ver_maj 2
%define ver_min 40
%define ver_patch 102

# All Unison versions sharing ver_compat are compatible
# Examples are 2.13.15 and 2.13.16 -> ver_compat == 2.13
# In older versions, even patch levels were not compatible
# Examples are ver_compat==2.9.0 and ver_compat==2.9.1
%define ver_compat      %{ver_maj}.%{ver_min}
%define ver_compat_name %{ver_maj}%{ver_min}
%define ver_noncompat   .%{ver_patch}

# ver_priority is the first component of ver_compat, catenated with the second
# component of ver_compat zero-filled to 3 digits, catenated with a final
# zero-filled 3-digit field. The final field contains the 3rd component of
# ver_compat (if there is one), otherwise 0.
%define ver_priority %(printf %%d%%03d%%03d `echo %{ver_compat}|sed 's/\\./ /g'`)

# Is this package the unisonNNN package with the highest ${ver_compat}
# available in this Fedora branch/release? If so, we provide unison.
%define provide_unison 1

Name:      unison%{ver_compat_name}
Version:   %{ver_compat}%{ver_noncompat}
Release:   2%{?dist}

Summary:   Multi-master File synchronization tool

Group:     Applications/File
License:   GPLv3+
URL:       http://www.cis.upenn.edu/~bcpierce/unison
Source0:   http://www.cis.upenn.edu/~bcpierce/unison/download/releases/unison-%{version}/unison-%{version}.tar.gz
Source1:   unison.png
Source2:   http://www.cis.upenn.edu/~bcpierce/unison/download/releases/unison-%{ver_compat}%{ver_noncompat}/unison-%{ver_compat}%{ver_noncompat}-manual.html

#Add documentation, already fixed in trunk (upstream)
Patch1:    %{name}-missing-documentation.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires: ocaml
BuildRequires: ocaml-lablgtk-devel
BuildRequires: desktop-file-utils
# for lablgtk
BuildRequires: gtk2-devel

Requires(posttrans): %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/alternatives

# Enforce the switch from unison to unisonN.NN
Obsoletes: unison < 2.27.57-3
# Let users just install "unison" if they want
%if 0%{?provide_unison}
Provides: unison = %{version}-%{release}
%endif

%description
Unison is a multi-master file-synchronization tool. It allows two
replicas of a collection of files and directories to be stored on
different hosts (or different locations on the same host), modified
separately, and then brought up to date by propagating the changes
in each replica to the other.

Note that this package contains Unison version %{ver_compat}, and
will never be upgraded to a different major version. Other packages
exist if you require a different major version.


%prep
%setup -q -n unison-%{version}

%patch1 -p1 -b .documentation

cat > %{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=unison-%{ver_compat}
Name=Unison File Synchronizer (version %{ver_compat})
GenericName=File Synchronizer
Comment=Multi-master File synchronization tool
Terminal=false
Icon=%{name}
StartupNotify=true
Categories=Utility;
EOF

#additional documentation
cp -a %{SOURCE2} unison-manual.html


%build
make NATIVE=true UISTYLE=gtk2 THREADS=true


%install
mkdir -p %{buildroot}%{_bindir}
cp -a unison %{buildroot}%{_bindir}/unison-%{ver_compat}
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
    %{name}.desktop

%posttrans
alternatives \
  --install \
  %{_bindir}/unison \
  unison \
  %{_bindir}/unison-%{ver_compat} \
  %{ver_priority}


%postun
if [ $1 -eq 0 ]; then
  alternatives --remove unison \
    %{_bindir}/unison-%{ver_compat}
fi
exit 0


%files
%doc COPYING NEWS README unison-manual.html
%{_bindir}/unison-%{ver_compat}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%changelog
* Fri Dec 14 2012 Richard W.M. Jones <rjones@redhat.com> - 2.40.102-2
- Rebuild for OCaml 4.00.1.

* Thu Nov 15 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.102-1
- 2.40.102
- fixes incompatibility between unison ocaml3 and ocaml4 builds

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Gregor Tätzner <brummbq@fedoraproject.com> - 2.40.63-6
- Patch built-in documentation.

* Sat Jan 21 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-5
- Add unison-manual.html.

* Fri Jan 13 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-4
- Remove ocaml minimum version.
- Add Requires and provides scripts.

* Tue Sep 27 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-3
- Remove vendor tag.

* Sun Sep 04 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-2
- Remove xorg-x11-font-utils Requirement.
- Enable THREADS=true.

* Thu Aug 30 2011 Gregor Tätzner <brummbq@fedoraproject.org> - 2.40.63-1
- Version bump.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.57-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.57-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 8 2009 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-11
- Add Requires: xorg-x11-fonts-misc

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.27.57-10
- Rebuild for OCaml 3.11.0+rc1.

* Sat May 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.27.57-9
- Rebuild with OCaml 3.10.2-2 (fixes bz 441685, 445545).

* Sun Mar 30 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-8
- Don't use alternatives for desktop and icon files, to avoid duplicate
  menu entries.

* Wed Mar 19 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-7
- Fix license to match correct interpretation of source & GPL
- Remove Excludes for ppc64, since ocaml is available there now, in devel

* Sat Mar 15 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-6
- Rename package unison2.27 -> unison227 to match Fedora naming rules
- Automatically calculate ver_priority using the shell; easier maintenance

* Sat Mar 1 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-5
- Use Provides/Obsoletes to provide upgrade path, per:
  http://fedoraproject.org/wiki/Packaging/NamingGuidelines

* Thu Feb 28 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-4
- Explicitly conflict with existing unison package

* Fri Feb 22 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2.27.57-3
- Derived unison2.27 package from unison2.13 package

* Mon Feb  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.27.57-2
- exclude arch ppc64

* Mon Feb  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.27.57-1
- new release 2.27.57

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-3
- Rebuild for FE6

* Tue Feb 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-2
- Rebuild for Fedora Extras 5

* Thu Sep  1 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.13.16-1
- New Version 2.13.16

* Sun Jul 31 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.12.0-0
- New Version 2.12.0

* Fri May 27 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.10.2-7
- Bump and rebuild with new ocaml and new lablgtk

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.10.2-6
- rebuild on all arches

* Mon May 16 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.10.2-5
- Patch: http://groups.yahoo.com/group/unison-users/message/3200

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.10.2-2
- BR gtk2-devel
- Added NEWS and README docs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.10.2-1
- New Version 2.10.2

* Wed Apr 28 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.74-0.fdr.1
- New Version 2.9.74
- Added icon

* Tue Jan 13 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.72-0.fdr.1
- New Version 2.9.72

* Tue Dec  9 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.70-0.fdr.2
- Changed Summary
- Added .desktop file

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.9.70-0.fdr.1
- First Fedora release

