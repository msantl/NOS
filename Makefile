PROJECT = naziv_programa
SOURCE = main.c drugi.c treci.c
HEADERS = glavni.h pomocni.h

CC = gcc
CFLAGS = -Wall -g
LDFLAGS =
OBJECTS = ${SOURCE:.c=.o}

$(PROJECT): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $(PROJECT) $(LDFLAGS)

$(OBJECTS): $(HEADERS)

clean:
	-rm -f $(PROJECT) $(OBJECTS) *.core
