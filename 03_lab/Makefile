PROJECT = sha3sum
SOURCE = main.cc keccak.cc
HEADERS = keccak.hh

CC = g++
CFLAGS = -Wall -g
LDFLAGS = 
OBJECTS = ${SOURCE:.cc=.o}

$(PROJECT): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $(PROJECT) $(LDFLAGS)

$(OBJECTS): $(HEADERS)

clean:
	-rm -f $(PROJECT) $(OBJECTS) *.core
