OBJS = xstatus.c
CC = gcc 
COMPILER_FLAGS = -pedantic -Wall
LINKER_FLAGS = -lX11
OBJ_NAME = xstatus


all : $(OBJS) 
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
