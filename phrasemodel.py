#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    from collections import defaultdict
    import sys

    unigram = defaultdict(int)
    bigram = defaultdict(int)

    delimiter = ","
    for line in sys.stdin:
        words, prob = line.rstrip().split("\t")
        prob = int(prob)
        w1, w2 = words.split(delimiter)
        unigram[w1] += 1
        bigram[(w1, w2)] += 1

    for (w1, w2), cnt in bigram.items():
        print("{}{}{}\t{}".format(
            w1, delimiter, w2,
            bigram[(w1, w2)] / unigram[w1]))
