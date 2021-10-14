SOURCES = $(wildcard *.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCES))

lox: $(OBJECTS)
	$(CC) $^ -o $@

clean:
	rm -rf *.o lox
