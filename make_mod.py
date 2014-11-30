#! /usr/bin/env python
# coding:utf-8

import config


def make_model_mod(
    phrase,
    bigram,
):
    '''
    特別な語用の mod ファイルを生成する。

    phrase で変換したい語を指定する。
    bigram で組み合わせてはいけない語を指定する。
    '''
    phrase_fd = open(phrase, "w")
    bigram_fd = open(bigram, "w")

    # phrase
    for word in config.XTU_REPLACE:
        print("{0},っ\t0.9".format(word), file=phrase_fd)
        print("{0},{0}\t0.9".format(word), file=phrase_fd)
    for word in config.XTU_ADD:
        print("{0},っ{0}\t0.9".format(word), file=phrase_fd)
        print("{0},{0}\t0.1".format(word), file=phrase_fd)

    print("make mod.model file: {}".format(phrase))

    # bigram
    print("っ っ\t1e-10", file=bigram_fd)
    print("ｯ っ\t1e-10", file=bigram_fd)
    print("っ ｯ\t1e-10", file=bigram_fd)
    print("ｯ ｯ\t1e-10", file=bigram_fd)
    for word in config.XTU_REPLACE:
        print("{0} っ\t1e-10".format(word), file=bigram_fd)
        print("っ {0}\t1e-10".format(word), file=bigram_fd)
    for word in config.XTU_ADD:
        print("{0} っ\t1e-10".format(word), file=bigram_fd)

    print("make mod.model file: {}".format(bigram))


if __name__ == '__main__':
    make_model_mod(
        config.PHRASE_MODEL_MOD,
        config.BIGRAM_MODEL_MOD
    )
