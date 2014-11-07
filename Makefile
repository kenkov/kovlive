SHELL=bash
PYTHON=python3
DELIMITER=","
NOSETESTS=nosetests -v

main: train_bigram convformat bigram phrase

train_bigram: train_bigram.cpp
	g++ -O2 -Wall -std=c++11 train_bigram.cpp -o train_bigram

convformat:
	sed -e 's/./& /g' -e 's/ $$//' -e 's/ , /,/g' <keyword.lst >keyword.txt

bigram:
	./train_bigram <(awk -F"," '{print $$2}' keyword.txt) >bigram.model

phrase:
	${PYTHON} phrase_extract.py ${DELIMITER} keyword.txt <keyword.txt | sort | uniq -c | awk '{ printf("%s\t%s\n", $$2, $$1) }' | ${PYTHON} phrasemodel.py >phrase.model

test:
	${NOSETESTS} *.py

clean:
	rm keyword.txt bigram.model phrase.model train_bigram
