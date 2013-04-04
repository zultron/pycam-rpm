Name:           pycam
Version:        0.5.1
Release:        1%{?dist}
Summary:        Open Source CAM - Toolpath Generation for 3-Axis CNC machining 
Group:          Applications/Engineering
License:        GPLv3+
URL:            http://sourceforge.net/projects/%{name}/
BuildArch:      noarch

Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python-devel
BuildRequires:  ccache
BuildRequires:  desktop-file-utils

Requires:       PyOpenGL
Requires:       pygtk2
Requires:       pygtkglext


%description
PyCAM is a toolpath generator for 3-axis CNC machining. It loads 3D
models in STL format or 2D contour models from DXF or SVG files. The
resulting GCode can be used with EMC2 or any other machine controller.

PyCAM supports a wide range of toolpath strategies for 3D models and
2D contour models.


%prep
%setup -q

for f in ./*.{txt,TXT} ./Changelog ./PKG-INFO; do
    iconv -f iso-8859-1 -t utf-8 $f |sed 's|\r||g' > $f.utf8
    touch -c -r $f $f.utf8
    mv $f.utf8 $f
done


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

desktop-file-install  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
    share/desktop/%{name}.desktop

pushd $RPM_BUILD_ROOT%{python_sitelib}/%{name}/
# remove shebang lines from top of module files
for lib in `find . -path "*.py"`; do
    echo $lib
    sed '/\/usr\/bin\/env/d' $lib > $lib.new && \
        touch -r $lib $lib.new && \
        mv $lib.new $lib
done
popd


%files 
%doc *.TXT *.txt Changelog PKG-INFO
%{_datadir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/pycam.desktop
%{python_sitelib}/*


%changelog
* Thu Apr  4 2013 John Morris <john@zultron.com> - 0.5.1-1
- Use pycam.desktop from upstream; remove Source1
- Cleanups for Fedora review

* Sat May  5 2012  <john@zultron.com> - 0.5.1-0
- Update to v.0.5.1

* Fri Aug 20 2010 Fabian Kanngießer <underscores@fedoraproject.org> - 0.3-3
- added a pygtk2 as said in the install textfile as dependency

* Fri Aug 20 2010 Fabian Kanngießer <underscores@fedoraproject.org> - 0.3-2
- updated license to version given in the license textfile 

* Thu Aug 19 2010 Fabian Kanngießer <underscores@fedoraproject.org> - 0.3-1
- removed unneeded files, comments and added dependencies so that the
  application works correctly, added desktop file

* Wed Aug 18 2010 Fabian Kanngießer <underscores@fedoraproject.org> - 0.3-0
- initial packaging
