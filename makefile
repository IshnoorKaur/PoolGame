CC = clang
CFLAGS = -std=c99 -Wall -pedantic 

all: myprog

clean:
	rm -f *.o *.so myprog

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

A1test1.o: A1test1.c phylib.h
	$(CC) $(CFLAGS) -c A1test1.c -o A1test1.o

myprog: A1test1.o phylib.o libphylib.so 
	$(CC) A1test1.o -L. -lphylib -lm -o myprog
	
