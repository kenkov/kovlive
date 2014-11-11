#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    from collections import defaultdict
    import sys

    unigram = defaultdict(int)
    bigram = defaultdict(int)
    delimiter = ","

    default_kanas = set()
    for line in open(sys.argv[1]):
        # load hiragana_phrase.model
        fullk, halfk = line.rstrip().split(delimiter)
        default_kanas.add(fullk)
        unigram[fullk] += 1
        bigram[(fullk, halfk)] += 1

    for line in sys.stdin:
        words, prob = line.rstrip().split("\t")
        prob = int(prob)
        w1, w2 = words.split(delimiter)
        if w1 not in default_kanas:
            unigram[w1] += 1
            bigram[(w1, w2)] += 1

    for (w1, w2), cnt in bigram.items():
        print("{}{}{}\t{}".format(
            w1, delimiter, w2,
            bigram[(w1, w2)] / unigram[w1]))
