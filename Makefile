SHELL=bash
PYTHON=python3
DELIMITER=","
NOSETESTS=nosetests -v --all-modules
DOCTEST=doctest

# phrase model
#     PHRASE_MODEL というフレーズモデルを生成する。
#     [生成方法]
#     まずKEYWORD_FILE から PHRASE に変換される。
#     次に
#     * PHRASE
#     * PHRASE_MOD
#     からフレーズモデルを生成し、その後で
#     * PHRASE_MODEL_MOD
#     をモデルに追加する。
KEYWORD_FILE=keyword.txt
PHRASE=phrase.txt
PHRASE_MOD=phrase.mod.txt
PHRASE_MODEL_MOD=phrase.mod.model
PHRASE_MODEL=phrase.model

# bigram model
#     BIGRAM_MODEL という言語モデルを生成する。
#     [生成方法]
#
#     HALFWIDTHKATAKANA_FILE から言語モデルを生成し、その後で
#     * BIGRAM_MOD
#     を追加する。
BIGRAM=halfwidthkatakana.txt
BIGRAM_MODEL_MOD=bigram.mod.model
BIGRAM_MODEL=bigram.model

.PHONY: main convformat bigram phrase clean

main: train_bigram modmodel convformat bigram phrase

train_bigram: TrainBigram.hs
	ghc -O2 -Wall TrainBigram.hs -o TrainBigram

modmodel:
	${PYTHON} make_mod.py

convformat:
	sed -e 's/./& /g' -e 's/ $$//' -e 's/ , /,/g' <${KEYWORD_FILE} >${PHRASE}

bigram:
	./TrainBigram <(ggrep -P '^.{3,}$$' ${BIGRAM} | sed -e 's/./& /g' -e 's/ $$//') | sort >${BIGRAM_MODEL}
	cat ${BIGRAM_MODEL_MOD} >>${BIGRAM_MODEL}

bigramsource:
	#./train_bigram <(awk -F"," '{print $$2}' ${FORMATED_KEYWORD_FILE}) >${BIGRAM_MODEL}
	#./train_bigram <(sed -e 's/./& /g' -e 's/ $$//' raw.txt) >${BIGRAM_MODEL}

phrase:
	${PYTHON} phrase_extract.py ${DELIMITER} ${PHRASE} <${PHRASE} \
		| sort \
		| uniq -c \
		| awk '{ printf("%s\t%s\n", $$2, $$1) }' \
		| ${PYTHON} phrasemodel.py ${PHRASE_MOD} >${PHRASE_MODEL}
	cat ${PHRASE_MODEL_MOD} >>${PHRASE_MODEL}

test:
	${NOSETESTS}
	${DOCTEST} TrainBigram.hs

clean:
	for file in ${PHRASE} \
				${BIGRAM_MODEL} \
				${PHRASE_MODEL} \
				TrainBigram \
				TrainBigram.o \
				TrainBigram.hi; do \
		if [ -e  $$file ]; then rm $$file; fi; \
	done
	if [ -d "__pycache__" ]; then rm -r __pycache__; fi
