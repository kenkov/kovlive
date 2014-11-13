#! /usr/bin/env python
# coding:utf-8

from os import path


# the number of loop for train IBM Model 2
LOOP_COUNT = 10
PHRASE_MODEL_FILE = path.join(
    path.abspath(path.dirname(__file__)),
    "phrase.model"
)
BIGRAM_MODEL_FILE = path.join(
    path.abspath(path.dirname(__file__)),
    "bigram.model"
)

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
