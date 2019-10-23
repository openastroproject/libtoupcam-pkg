#!/bin/bash

version=`cat version`

rm -fr libtoupcam-$version
rm -fr libtoupcam_*
rm -fr libtoupcam-dev_*
rm -f debfiles/compat
rm -f debfiles/patches/*
