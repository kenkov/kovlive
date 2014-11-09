SHELL=bash
PYTHON=python3
DELIMITER=","
NOSETESTS=nosetests -v

KEYWORD_FILE=keyword.txt
FORMATED_KEYWORD_FILE=keyword.input.txt
HALFWIDTHKATAKANA_FILE=halfwidthkatakana.txt

BIGRAM_MODEL=bigram.model
PHRASE_MODEL=phrase.model

.PHONY: main convformat bigram phrase clean

main: train_bigram convformat bigram phrase

train_bigram: train_bigram.cpp
	g++ -O2 -Wall -std=c++11 train_bigram.cpp -o train_bigram

convformat:
	sed -e 's/./& /g' -e 's/ $$//' -e 's/ , /,/g' <${KEYWORD_FILE} >${FORMATED_KEYWORD_FILE}

bigram:
	./train_bigram <(ggrep -P '^.{3,}$$' ${HALFWIDTHKATAKANA_FILE} | sed -e 's/./& /g' -e 's/ $$//') >${BIGRAM_MODEL}
	cat ./hiragana_bigram.model >>bigram.model

bigramsource:
	#./train_bigram <(awk -F"," '{print $$2}' ${FORMATED_KEYWORD_FILE}) >${BIGRAM_MODEL}
	#./train_bigram <(sed -e 's/./& /g' -e 's/ $$//' raw.txt) >${BIGRAM_MODEL}

phrase:
	${PYTHON} phrase_extract.py ${DELIMITER} ${FORMATED_KEYWORD_FILE} <${FORMATED_KEYWORD_FILE} | sort | uniq -c | awk '{ printf("%s\t%s\n", $$2, $$1) }' | ${PYTHON} phrasemodel.py >${PHRASE_MODEL}
	cat hiragana_phrase.model >>${PHRASE_MODEL}

test:
	${NOSETESTS} *.py

clean:
	rm ${FORMATED_KEYWORD_FILE} ${BIGRAM_MODEL} ${PHRASE_MODEL} train_bigram
