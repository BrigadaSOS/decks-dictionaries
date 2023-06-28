PYTHON = python3
OUTPUT = output/

.PHONY = TangoN5 TangoN4

make: TangoN5 TangoN4

TangoN5:
	${PYTHON} build_deck.py tango_n5/ ${OUTPUT}

TangoN4:
	${PYTHON} build_deck.py tango_n4/ ${OUTPUT}
