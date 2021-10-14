OBJECTS = chunk.o debug.o main.o memory.o

lox: $(OBJECTS)
	$(CC) $^ -o $@

clean:
	rm -rf *.o lox
