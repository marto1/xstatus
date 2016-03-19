# xstatus version
VERSION = 0.1

# paths
PREFIX = /usr/local
MANPREFIX = ${PREFIX}/share/man

INCS =
LIBS = -lX11
CFLAGS = -std=c99 -pedantic -Wall -Os ${INCS}
LDFLAGS = -s ${LIBS}
OBJ_NAME = xstatus


CC = gcc 
