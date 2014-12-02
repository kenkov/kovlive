SHELL=bash
PYTHON=python3
DELIMITER=","
NOSETESTS=nosetests -v --all-modules

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
KEYWORD_FILE={{ KEYWORD_FILE }}
PHRASE={{ PHRASE }}
PHRASE_MOD={{ PHRASE_MOD }}
PHRASE_MODEL_MOD={{ PHRASE_MODEL_MOD }}
PHRASE_MODEL={{ PHRASE_MODEL }}

# bigram model
#     BIGRAM_MODEL という言語モデルを生成する。
#     [生成方法]
#
#     HALFWIDTHKATAKANA_FILE から言語モデルを生成し、その後で
#     * BIGRAM_MOD
#     を追加する。
BIGRAM={{ BIGRAM }}
BIGRAM_MODEL_MOD={{ BIGRAM_MODEL_MOD }}
BIGRAM_MODEL={{ BIGRAM_MODEL }}

.PHONY: main modmodel convformat bigram phrase test clean

main: modelmod convformat bigram phrase

modelmod:
	${PYTHON} make_mod.py

convformat:
	sed -e 's/./& /g' -e 's/ $$//' -e 's/ , /,/g' <${KEYWORD_FILE} >${PHRASE}

bigram:
	${PYTHON} train_bigram.py <(grep -P '^.{3,}$$' ${BIGRAM} | sed -e 's/./& /g' -e 's/ $$//') | sort >${BIGRAM_MODEL}
	cat ${BIGRAM_MODEL_MOD} >>${BIGRAM_MODEL}

phrase:
	${PYTHON} phrase_extract.py ${DELIMITER} ${PHRASE} <${PHRASE} \
		| sort \
		| uniq -c \
		| awk '{ printf("%s\t%s\n", $$2, $$1) }' \
		| ${PYTHON} phrasemodel.py ${PHRASE_MOD} >${PHRASE_MODEL}
	cat ${PHRASE_MODEL_MOD} >>${PHRASE_MODEL}

test:
	${NOSETESTS}

clean:
	for file in ${PHRASE} \
				${BIGRAM_MODEL} \
				${BIGRAM_MODEL_MOD} \
				${PHRASE_MODEL} \
				${PHRASE_MODEL_MOD} \
				TrainBigram \
				TrainBigram.o \
				TrainBigram.hi; do \
		if [ -e  $$file ]; then rm $$file; fi; \
	done
	if [ -d "__pycache__" ]; then rm -r __pycache__; fi
