#!/bin/bash
#

cd base_ubuntu
sh build.sh
cd ..

cd nb
sh build_py2.sh
sh build_py3.sh
cd ..
