#!/bin/bash

cp ../patches/*.patch .
rm -f makefile.patch

rm -f libtoupcam-1.39.15529.tar.gz
ln ../libtoupcam-1.39.15529.tar.gz .
rel=`cut -d' ' -f3 < /etc/redhat-release`
fedpkg --release f$rel local
