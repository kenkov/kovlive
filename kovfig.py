#! /usr/bin/env python
# coding:utf-8

from os import path


# the number of loop for train IBM Model 2
loop_count = 10
phrase_model_file = path.join(
    path.abspath(path.dirname(__file__)),
    "phrase.model"
)
bigram_model_file = path.join(
    path.abspath(path.dirname(__file__)),
    "bigram.model"
)

if __name__ == '__main__':
    print("{} = {}".format(
        "loop_count",
        loop_count))
    print("{} = {}".format(
        "phrase_model_file",
        phrase_model_file))
    print("{} = {}".format(
        "bigram_model_file",
        bigram_model_file))
