#!/bin/bash

rm -f libtoupcam-1.33.13725.tar.gz
ln ../libtoupcam-1.33.13725.tar.gz .
rel=`cut -d' ' -f3 < /etc/redhat-release`
fedpkg --release f$rel local
