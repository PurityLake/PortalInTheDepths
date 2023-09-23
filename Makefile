CXX=g++
SRCDIR=src
SRCS=$(shell find $(SRCDIR) -name '*.cpp')
OBJS=$(SRCS:%.cpp=%.o)
BIN?=pitd
CFLAGS=-g -Wall -Wextra $(shell pkg-config -static -cflags SDL2)
LDFLAGS=$(shell pkg-config -static -libs SDL2)

all: $(OBJS)
	$(CXX) $(CFLAGS) $(OBJS) -o $(BIN) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CFLAGS) -Iinclude/ -o $@ -c $< $(LDFLAGS)
