#!/bin/bash

rm *.o *.so

g++ -Wall -c -g -fPIC plasma_source.cpp -o plasma_source.o
g++ -c -g -fPIC source_sampling.cpp -o source_sampling.o

g++ -Wall -Wl,-soname,source_sampling.so -I/openmc/include -I/openmc/vendor/pugixml -L/openmc/lib -lopenmc -fPIC -shared source_sampling.cpp -o source_sampling.so *.o
