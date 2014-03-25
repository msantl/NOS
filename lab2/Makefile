PROJECT = cjevovod
SOURCE = main.c kriptiraj.c dekriptiraj.c
HEADERS = kriptiraj.h dekriptiraj.h

CC = gcc
CFLAGS = -Wall -g
LDFLAGS =
OBJECTS = ${SOURCE:.c=.o}

$(PROJECT): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(PROJECT)

$(OBJECTS): $(HEADERS)

clean:
	-rm -f $(PROJECT) $(OBJECTS) *.core
