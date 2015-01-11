#! /usr/bin/env python
# coding:utf-8

from os import path


def filepath(*fp):
    '''
    このシクリプトが存在するディレクトリからの
    絶対パスに変換する
    '''
    return path.join(
        path.abspath(path.dirname(__file__)),
        *fp
    )

modeldir = "model"

# the number of loop for train IBM Model 2
LOOP_COUNT = 10
PHRASE_MODEL = filepath(
    modeldir,
    "phrase.model"
)
PHRASE = filepath(
    modeldir,
    "phrase.txt"
)
BIGRAM = filepath(
    modeldir,
    "halfwidthkatakana.txt"
)
PHRASE_MOD = filepath(
    modeldir,
    "phrase.mod.txt"
)
BIGRAM_MODEL = filepath(
    modeldir,
    "bigram.model"
)
PHRASE_MODEL_MOD = filepath(
    modeldir,
    "phrase.mod.model"
)
BIGRAM_MODEL_MOD = filepath(
    modeldir,
    "bigram.mod.model"
)
KEYWORD_FILE = filepath(
    modeldir,
    "keyword.txt"
)

XTU_REPLACE = {
    "。", "、", "."
}

XTU_ADD = {
    "</s>", "…",
    "！", "？", "!", "♡", "☆", "♪", "♡", "ｗ",
    "/",
    #">", ")"
    #"＞", "）",
}


if __name__ == '__main__':
    from jinja2 import Environment, FileSystemLoader
    env = Environment(
        loader=FileSystemLoader('.')
    )
    template = env.get_template('Makefile.tpl')
    makefile = template.render(
        PHRASE=PHRASE,
        PHRASE_MODEL=PHRASE_MODEL,
        PHRASE_MODEL_MOD=PHRASE_MODEL_MOD,
        PHRASE_MOD=PHRASE_MOD,
        BIGRAM=BIGRAM,
        BIGRAM_MODEL=BIGRAM_MODEL,
        BIGRAM_MODEL_MOD=BIGRAM_MODEL_MOD,
        KEYWORD_FILE=KEYWORD_FILE,
    )
    print(makefile, file=open("Makefile", "w"))
    print("generating Makefile ... done")
