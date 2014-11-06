SHELL=bash
PHRASE_EXTRACT=$${HOME}/Projects/smt/smt/phrase/phrase_extract.py
PYTHON=python3

main: train_bigram convformat bigram phrase

train_bigram: train_bigram.cpp
	g++ -O2 -Wall -std=c++11 train_bigram.cpp -o train_bigram

convformat:
	${PYTHON} fmtconverter.py keyword.lst >keyword.txt

bigram:
	./train_bigram <(awk -F"," '{print $$2}' keyword.txt) >bigram.model

phrase:
	cat keyword.txt | ${PYTHON} ${PHRASE_EXTRACT} keyword.txt | sort | uniq -c | awk '{ printf("%s\t%s\n", $$2, $$1) }' | ${PYTHON} phrasemodel.py >phrase.model

clean:
	rm keyword.txt bigram.model phrase.model train_bigram
