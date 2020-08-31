#!/bin/bash

set -ex

gcc -x c $(rpm --eval %build_cflags) data/hello.c -o hello_c.out
./hello_c.out | grep -q "Hello World"

g++ -x c++ $(rpm --eval %build_cxxflags) data/hello.cpp -o hello_cpp.out
./hello_cpp.out | grep -q "Hello World"
