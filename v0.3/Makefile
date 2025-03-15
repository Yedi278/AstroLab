CXX=g++
CXXFLAGS=-Wall -g -std=c++11
LDFLAGS=
LDLIBS=-Iinclude -Ilib\SDL3-3.2.8\x86_64-w64-mingw32\include -Llib\SDL3-3.2.8\x86_64-w64-mingw32\lib

all: main

main: main.o
	$(CXX) $(LDFLAGS) -o $@ $^

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<