PYTHON = python3
OUTPUT = output/

.PHONY = n5

n5:
	${PYTHON} build_deck.py tango_n5/ ${OUTPUT}
