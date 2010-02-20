#!/bin/bash

mkdir -p pyreaper/src
cp ../setup.py pyreaper/
cp -R ../src/* pyreaper/src/
rm pyreaper/src/PyReaper/*.pyc
# 7z a pyreaper.7z pyreaper
tar cfvz pyreaper.tar.gz pyreaper
rm -rf pyreaper
