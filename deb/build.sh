#!/bin/bash

export DEBEMAIL=james@openastroproject.org
export DEBFULLNAME="James Fidell"

version=`cat version`

srcdir=libtoupcam-$version
debdir=debian
debsrc=$debdir/source
quiltconf=$HOME/.quiltrc-dpkg

mkdir $srcdir
cd $srcdir
tar zxf ../libtoupcam-$version.tar.gz
test -d demo && ( chmod -x demo/*.* Makefile )
YFLAG=-y
dh_make -v | fgrep -q '1998-2011'
if [ $? -eq 0 ]
then
  YFLAG=''
fi
dh_make $YFLAG -l -f ../libtoupcam-$version.tar.gz

cp ../debfiles/control $debdir
cp ../debfiles/copyright $debdir
cp ../debfiles/changelog $debdir
cp ../debfiles/docs $debdir
cp ../debfiles/watch $debdir
cp ../debfiles/libtoupcam.dirs $debdir
cp ../debfiles/libtoupcam.install $debdir
cp ../debfiles/libtoupcam.symbols $debdir
cp ../debfiles/libtoupcam.doc-base $debdir
cp ../debfiles/libtoupcam-dev.dirs $debdir
cp ../debfiles/libtoupcam-dev.install $debdir

echo 10 > $debdir/compat

sed -e '/^.*[ |]configure./a\
        ldconfig\
	udevadm control --reload-rules || true' < $debdir/postinst.ex > $debdir/postinst
chmod +x $debdir/postinst
sed -e '/^.*[ |]remove./a\
        ldconfig\
	udevadm control --reload-rules || true' < $debdir/postrm.ex > $debdir/postrm
chmod +x $debdir/postrm
echo "3.0 (quilt)" > $debsrc/format

sed -e "s/DEBVERSION/$version/g" < ../debfiles/rules.overrides >> $debdir/rules

rm $debdir/README.Debian
rm $debdir/README.source
rm $debdir/libtoupcam-docs.docs
rm $debdir/libtoupcam1.*
rm $debdir/*.[Ee][Xx]


export QUILT_PATCHES="debian/patches"
export QUILT_PATCH_OPTS="--reject-format=unified"
export QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
export QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
mkdir -p $QUILT_PATCHES

for p in `ls -1 ../debfiles/patches`
do
  quilt --quiltrc=$quiltconf new $p
  for f in `egrep '^\+\+\+' ../debfiles/patches/$p | awk '{ print $2; }'`
  do
    quilt --quiltrc=$quiltconf add $f
  done
pwd
  patch -p0 < ../debfiles/patches/$p
  quilt --quiltrc=$quiltconf refresh
done

dpkg-buildpackage -us -uc

echo "Now run:"
echo
echo "    lintian -i -I --show-overrides libtoupcam_$version-2_amd64.changes"
