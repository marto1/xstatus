# See LICENSE file for copyright and license details.

include config.mk

SRC = xstatus.c
OBJ = ${SRC:.c=.o}
BIN = ${OBJ:.o=}

all: options ${BIN}

options:
	@echo xstatus build options:
	@echo "CFLAGS   = ${CFLAGS}"
	@echo "LDFLAGS  = ${LDFLAGS}"
	@echo "CC       = ${CC}"

.c.o:
	@echo CC $<
	@${CC} -c ${CFLAGS} $<

${OBJ}: config.h config.mk

config.h:
	@echo creating $@ from config.def.h
	@cp config.def.h $@

.o:
	@echo CC -o $@
	@${CC} -o $@ $< ${LDFLAGS}

clean:
	@echo cleaning
	@rm -f ${BIN} ${OBJ} *.pyc

dist: clean
	@echo creating dist tarball
	@mkdir -p xstatus-${VERSION}
	@cp -R LICENSE Makefile README config.def.h config.mk \
		xstatus.1 ${SRC} xstatus-${VERSION}
	@tar -cf xstatus-${VERSION}.tar xstatus-${VERSION}
	@gzip xstatus-${VERSION}.tar
	@rm -rf xstatus-${VERSION}

install: all
	@echo installing executable files to ${DESTDIR}${PREFIX}/bin
	@mkdir -p "${DESTDIR}${PREFIX}/bin"
	@cp -f ${BIN} "${DESTDIR}${PREFIX}/bin"
	@chmod 755 "${DESTDIR}${PREFIX}/bin/xstatus"
	@echo installing manual pages to ${DESTDIR}${MANPREFIX}/man1
	@mkdir -p "${DESTDIR}${MANPREFIX}/man1"
	@sed "s/VERSION/${VERSION}/g" < xstatus.1 > "${DESTDIR}${MANPREFIX}/man1/xstatus.1"
	@chmod 644 "${DESTDIR}${MANPREFIX}/man1/xstatus.1"

uninstall:
	@echo removing executable files from ${DESTDIR}${PREFIX}/bin
	@rm -f "${DESTDIR}${PREFIX}/bin/xstatus"
	@rm -f "${DESTDIR}${PREFIX}/bin/xembed"
	@echo removing manual pages from ${DESTDIR}${MANPREFIX}/man1
	@rm -f "${DESTDIR}${MANPREFIX}/man1/xstatus.1"
	@rm -f "${DESTDIR}${MANPREFIX}/man1/xembed.1"

.PHONY: all options clean dist install uninstall


# all : $(OBJS) 
# 	$(CC) $(OBJS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
