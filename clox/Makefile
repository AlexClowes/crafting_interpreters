SOURCES = $(wildcard *.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCES))
CFLAGS = -MD

lox: $(OBJECTS)
	$(CC) $^ -o $@

.PHONY: clean
clean:
	rm -rf *.d *.o lox

-include $(OBJECTS:.o=.d)
