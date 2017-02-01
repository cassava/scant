DESTDIR=~/.local/bin

.PHONY: install

install:
	install -m755 scant.py ${DESTDIR}/scant
	install -m755 scant-combine.py ${DESTDIR}/scant-combine
