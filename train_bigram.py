#! /usr/bin/env python
# coding:utf-8


from collections import defaultdict


def add_symbol(
    lst: [str],
    start_symbol: str="<s>",
    end_symbol: str="</s>"
):
    return [start_symbol] + lst + [end_symbol]


def _train(
    lst: [[str]],
    start_symbol: str="<s>",
    end_symbol: str="</s>"
) -> ({int}, {int}):
    bigram = defaultdict(int)
    unigram = defaultdict(int)
    total = 0

    for words in lst:
        lst = words
        for w1, w2 in zip(lst, lst[1:]):
            bigram[(w1, w2)] += 1
            unigram[w1] += 1
            total += 1
        unigram[w2] += 1
        total += 1

    # unigram model では P(<s>) = 1 なので、<s> は含まないようにする。
    unigram_without_start = {key: num for key, num in unigram.items()
                             if key != start_symbol}
    unilen = sum(unigram_without_start.values())
    return (
        {key: val/unilen for key, val in unigram_without_start.items()},
        {(w1, w2): val/unigram[w1] for (w1, w2), val in bigram.items()}
    )


def test_train():
    slist = [
        "a b c",
        "b c a"
    ]
    _train(add_symbol(snt.split()) for snt in slist) == \
        ({'a': 0.25,
          'b': 0.25,
          'c': 0.25,
          '</s>': 0.25
          },
         {('<s>', 'a'): 0.5,
          ('<s>', 'b'): 0.5,
          ('a', '</s>'): 0.5,
          ('a', 'b'): 0.5,
          ('b', 'c'): 1.0,
          ('c', '</s>'): 0.5,
          ('c', 'a'): 0.5
          })


def train(
    filename: str,
    start_symbol: str="<s>",
    end_symbol: str="</s>",
    start_end_symbol=True
):

    with open(filename) as f:
        unimodel, bimodel = _train(add_symbol(line.split()) for line in f)

    for (w1, w2), val in bimodel.items():
        print("{} {}\t{:.6f}".format(w1, w2, val))

    for key, val in unimodel.items():
        print("{}\t{:.6f}".format(key, val))


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    train(filename=filename)
