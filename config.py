#! /usr/bin/env python
# coding:utf-8

from os import path


def filepath(fp):
    '''
    このシクリプトが存在するディレクトリからの
    絶対パスに変換する
    '''
    return path.join(
        path.abspath(path.dirname(__file__)),
        fp
    )


# the number of loop for train IBM Model 2
LOOP_COUNT = 10
PHRASE_MODEL_FILE = filepath("phrase.model")
BIGRAM_MODEL_FILE = filepath("bigram.model")

PHRASE_MOD_MODEL_FILE = filepath("phrase.mod.model")
BIGRAM_MOD_MODEL_FILE = filepath("bigram.mod.model")

XTU_REPLACE = {
    "。", "、", "."
}

XTU_ADD = {
    "</s>", "…",
    "！", "？", "!", "♡", "☆", "♪", "♡", "ｗ",
    ">", ")", "/",
    "＞", "）",
}


if __name__ == '__main__':
    print("{} = {}".format(
        "LOOP_COUNT",
        LOOP_COUNT))
    print("{} = {}".format(
        "phrase_model_file",
        PHRASE_MODEL_FILE))
    print("{} = {}".format(
        "bigram_model_file",
        BIGRAM_MODEL_FILE))
