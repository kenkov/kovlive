#! /usr/bin/env python
# coding:utf-8

import collections
import decimal
from decimal import Decimal as D

# set deciaml context
decimal.getcontext().prec = 4
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def mkcorpus(
        sentences: [(str, str)]):
    return [(es.split(), fs.split()) for (es, fs) in sentences]


def matrix(
        m, n, lst,
        m_text: list=None,
        n_text: list=None):
    """
    m: row
    n: column
    lst: items

    >>> print(matrix(2, 3, [(1, 1), (2, 3)]))
    |x| | |
    | | |x|
    """

    fmt = ""
    if n_text:
        fmt += "     {}\n".format(" ".join(n_text))
    for i in range(1, m+1):
        if m_text:
            fmt += "{:<4.4} ".format(m_text[i-1])
        fmt += "|"
        for j in range(1, n+1):
            if (i, j) in lst:
                fmt += "x|"
            else:
                fmt += " |"
        fmt += "\n"
    return fmt


def _train_ibmmodel1(corpus, loop_count=10):

    def _constant_factory(value):
        '''define a local function for uniform probability initialization'''
        #return itertools.repeat(value).next
        return lambda: value

    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            f_keys.add(f)
    # default value provided as uniform probability)
    t = collections.defaultdict(_constant_factory(D(1/len(f_keys))))

    # loop
    for i in range(loop_count):
        count = collections.defaultdict(D)
        total = collections.defaultdict(D)
        s_total = collections.defaultdict(D)
        for (es, fs) in corpus:
            # compute normalization
            for e in es:
                s_total[e] = D()
                for f in fs:
                    s_total[e] += t[(e, f)]
            for e in es:
                for f in fs:
                    count[(e, f)] += t[(e, f)] / s_total[e]
                    total[f] += t[(e, f)] / s_total[e]
                    #if e == u"に" and f == u"always":
                    #    print(" BREAK:", i, count[(e, f)])
        # estimate probability
        for (e, f) in count.keys():
            #if count[(e, f)] == 0:
            #    print(e, f, count[(e, f)])
            t[(e, f)] = count[(e, f)] / total[f]

    return t


def _train_ibmmodel2(corpus, loop_count=10):

    class _keydefaultdict(collections.defaultdict):
        '''define a local function for uniform probability initialization'''
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            else:
                ret = self[key] = self.default_factory(key)
                return ret

    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            f_keys.add(f)
    # initialize t
    t = _train_ibmmodel1(corpus, loop_count)
    # default value provided as uniform probability)

    def key_fun(key):
        ''' default_factory function for keydefaultdict '''
        i, j, l_e, l_f = key
        return D("1") / D(l_f + 1)
    a = _keydefaultdict(key_fun)

    # loop
    for _i in range(loop_count):
        # variables for estimating t
        count = collections.defaultdict(D)
        total = collections.defaultdict(D)
        # variables for estimating a
        count_a = collections.defaultdict(D)
        total_a = collections.defaultdict(D)

        s_total = collections.defaultdict(D)
        for (es, fs) in corpus:
            l_e = len(es)
            l_f = len(fs)
            # compute normalization
            for (j, e) in enumerate(es, 1):
                s_total[e] = 0
                for (i, f) in enumerate(fs, 1):
                    s_total[e] += t[(e, f)] * a[(i, j, l_e, l_f)]
            # collect counts
            for (j, e) in enumerate(es, 1):
                for (i, f) in enumerate(fs, 1):
                    c = t[(e, f)] * a[(i, j, l_e, l_f)] / s_total[e]
                    count[(e, f)] += c
                    total[f] += c
                    count_a[(i, j, l_e, l_f)] += c
                    total_a[(j, l_e, l_f)] += c

        # estimate probability
        for (e, f) in count.keys():
            try:
                t[(e, f)] = count[(e, f)] / total[f]
            except decimal.DivisionByZero:
                print(u"e: {e}, f: {f}, count[(e, f)]: {ef}, total[f]: \
                      {totalf}".format(e=e, f=f, ef=count[(e, f)],
                                       totalf=total[f]))
                raise
        for (i, j, l_e, l_f) in count_a.keys():
            a[(i, j, l_e, l_f)] = count_a[(i, j, l_e, l_f)] / \
                total_a[(j, l_e, l_f)]
    # output
    #for (e, f), val in t.items():
    #    print("{} {}\t{}".format(e, f, float(val)))
    #for (i, j, l_e, l_f), val in a.items():
    #    print("{} {} {} {}\t{}".format(i, j, l_e, l_f, float(val)))

    return (t, a)


def train_ibmmodel1(sentences, loop_count=10):
    #for i, j in sentences:
    #    print(i, j)
    corpus = mkcorpus(sentences)
    return _train_ibmmodel1(corpus, loop_count)


def train_ibmmodel2(sentences, loop_count=10):
    #for i, j in sentences:
    #    print(i, j)
    corpus = mkcorpus(sentences)
    return _train_ibmmodel2(corpus, loop_count)


def viterbi_alignment(es, fs, t, a):
    '''
    return
        dictionary
            e in es -> f in fs
    '''
    max_a = collections.defaultdict(float)
    l_e = len(es)
    l_f = len(fs)
    for (j, e) in enumerate(es, 1):
        current_max = (0, -1)
        for (i, f) in enumerate(fs, 1):
            val = t[(e, f)] * a[(i, j, l_e, l_f)]
            # select the first one among the maximum candidates
            if current_max[1] < val:
                current_max = (i, val)
        max_a[j] = current_max[0]
    return max_a


def show_matrix(es, fs, t, a):
    '''
    print matrix according to viterbi alignment like

         fs
      |x| | | |
    e | | |x| |
    s | | | |x|
      | | |x| |
    '''
    max_a = viterbi_alignment(es, fs, t, a).items()
    m = len(es)
    n = len(fs)
    return matrix(m, n, max_a, es, fs)


def _alignment(elist, flist, e2f, f2e):
    '''
    elist, flist
        wordlist for each language
    e2f
        translatoin alignment from e to f
        alignment is
        [(e, f)]
    f2e
        translatoin alignment from f to e
        alignment is
        [(e, f)]
    return
        alignment: {(f, e)}
             flist
          -----------------
        e |               |
        l |               |
        i |               |
        s |               |
        t |               |
          -----------------

    '''
    neighboring = {(-1, 0), (0, -1), (1, 0), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)}
    e2f = set(e2f)
    f2e = set(f2e)
    m = len(elist)
    n = len(flist)
    alignment = e2f.intersection(f2e)
    # marge with neighborhood
    while True:
        set_len = len(alignment)
        for e_word in range(1, m+1):
            for f_word in range(1, n+1):
                if (e_word, f_word) in alignment:
                    for (e_diff, f_diff) in neighboring:
                        e_new = e_word + e_diff
                        f_new = f_word + f_diff
                        if not alignment:
                            if (e_new, f_new) in e2f.union(f2e):
                                alignment.add((e_new, f_new))
                        else:
                            if ((e_new not in list(zip(*alignment))[0]
                                    or f_new not in list(zip(*alignment))[1])
                                    and (e_new, f_new) in e2f.union(f2e)):
                                alignment.add((e_new, f_new))
        if set_len == len(alignment):
            break
    # finalize
    for e_word in range(1, m+1):
        for f_word in range(1, n+1):
            # for alignment = set([])
            if not alignment:
                if (e_word, f_word) in e2f.union(f2e):
                    alignment.add((e_word, f_word))
            else:
                if ((e_word not in list(zip(*alignment))[0]
                        or f_word not in list(zip(*alignment))[1])
                        and (e_word, f_word) in e2f.union(f2e)):
                    alignment.add((e_word, f_word))
    return alignment


def alignment(es, fs, e2f, f2e):
    """
    es: English words
    fs: Foreign words
    f2e: alignment for translation from fs to es
        [(e, f)] or {(e, f)}
    e2f: alignment for translation from es to fs
        [(f, e)] or {(f, e)}
    """
    _e2f = list(zip(*reversed(list(zip(*e2f)))))
    return _alignment(es, fs, _e2f, f2e)


def symmetrization(es, fs, corpus):
    '''
    forpus
        for translation from fs to es
    return
        alignment **from fs to es**
    '''
    f2e_train = _train_ibmmodel2(corpus, loop_count=10)
    f2e = viterbi_alignment(es, fs, *f2e_train).items()

    e2f_corpus = list(zip(*reversed(list(zip(*corpus)))))
    e2f_train = _train_ibmmodel2(e2f_corpus, loop_count=10)
    e2f = viterbi_alignment(fs, es, *e2f_train).items()

    return alignment(es, fs, e2f, f2e)


def phrase_extract(es, fs, alignment):
    ext = extract(es, fs, alignment)
    ind = {((x, y), (z, w)) for x, y, z, w in ext}
    es = tuple(es)
    fs = tuple(fs)
    return {(es[e_s-1:e_e], fs[f_s-1:f_e])
            for (e_s, e_e), (f_s, f_e) in ind}


def _extract(es, fs, e_start, e_end, f_start, f_end, alignment):
    if f_end == 0:
        return {}
    for (e, f) in alignment:
        if (f_start <= f <= f_end) and (e < e_start or e > e_end):
            return {}
    ex = set()
    f_s = f_start
    while True:
        f_e = f_end
        while True:
            ex.add((e_start, e_end, f_s, f_e))
            f_e += 1
            if f_e in list(zip(*alignment))[1] or f_e > len(fs):
                break
        f_s -= 1
        if f_s in list(zip(*alignment))[1] or f_s < 1:
            break
    return ex


def extract(es, fs, alignment):
    """
    caution:
        alignment starts from 1 - not 0
    """
    phrases = set()
    len_es = len(es)
    for e_start in range(1, len_es+1):
        for e_end in range(e_start, len_es+1):
            # find the minimally matching foreign phrase
            f_start, f_end = (len(fs), 0)
            for (e, f) in alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)
            phrases.update(_extract(es, fs, e_start,
                                    e_end, f_start,
                                    f_end, alignment))
    return phrases


def test_train_ibmmodel1_loop1():
    sent_pairs = [("the house", "das Haus"),
                  ("the book", "das Buch"),
                  ("a book", "ein Buch"),
                  ]
    #t0 = train(sent_pairs, loop_count=0)
    t1 = train_ibmmodel1(sent_pairs, loop_count=1)

    loop1 = [(('house', 'Haus'), D("0.5")),
             (('book', 'ein'), D("0.5")),
             (('the', 'das'), D("0.5")),
             (('the', 'Buch'), D("0.25")),
             (('book', 'Buch'), D("0.5")),
             (('a', 'ein'), D("0.5")),
             (('book', 'das'), D("0.25")),
             (('the', 'Haus'), D("0.5")),
             (('house', 'das'), D("0.25")),
             (('a', 'Buch'), D("0.25"))]
    # assertion
    # next assertion doesn't make sence because
    # initialized by defaultdict
    #self.assertEqual(self._format(t0.items()), self._format(loop0))
    assert set(t1.items()) == set(loop1)


def test_train_ibmmodel1_loop2():
    sent_pairs = [("the house", "das Haus"),
                  ("the book", "das Buch"),
                  ("a book", "ein Buch"),
                  ]
    #t0 = train(sent_pairs, loop_count=0)
    t2 = train_ibmmodel1(sent_pairs, loop_count=2)

    loop2 = [(('house', 'Haus'), D("0.5713")),
             (('book', 'ein'), D("0.4284")),
             (('the', 'das'), D("0.6367")),
             (('the', 'Buch'), D("0.1818")),
             (('book', 'Buch'), D("0.6367")),
             (('a', 'ein'), D("0.5713")),
             (('book', 'das'), D("0.1818")),
             (('the', 'Haus'), D("0.4284")),
             (('house', 'das'), D("0.1818")),
             (('a', 'Buch'), D("0.1818"))]
    # assertion
    # next assertion doesn't make sence because
    # initialized by defaultdict
    #self.assertEqual(self._format(t0.items()), self._format(loop0))
    assert set(t2.items()) == set(loop2)


def test_viterbi_alignment():
    x = viterbi_alignment([1, 2, 1],
                          [2, 3, 2],
                          collections.defaultdict(int),
                          collections.defaultdict(int))
    # Viterbi_alignment selects the first token
    # if t or a doesn't contain the key.
    # This means it returns NULL token
    # in such a situation.
    ans = {1: 1, 2: 1, 3: 1}
    assert dict(x) == ans


def test_alignment():
    elist = "michael assumes that he will stay in the house".split()
    flist = "michael geht davon aus , dass er im haus bleibt".split()
    e2f = [(1, 1), (2, 2), (2, 3), (2, 4), (3, 6),
           (4, 7), (7, 8), (9, 9), (6, 10)]
    f2e = [(1, 1), (2, 2), (3, 6), (4, 7), (7, 8),
           (8, 8), (9, 9), (5, 10), (6, 10)]
    ans = set([(1, 1),
               (2, 2),
               (2, 3),
               (2, 4),
               (3, 6),
               (4, 7),
               (5, 10),
               (6, 10),
               (7, 8),
               (8, 8),
               (9, 9)])
    assert _alignment(elist, flist, e2f, f2e) == ans


def test_symmetrization():
    sentenses = [("僕 は 男 です", "I am a man"),
                 ("私 は 女 です", "I am a girl"),
                 ("私 は 先生 です", "I am a teacher"),
                 ("彼女 は 先生 です", "She is a teacher"),
                 ("彼 は 先生 です", "He is a teacher"),
                 ]
    corpus = mkcorpus(sentenses)
    es = "私 は 先生 です".split()
    fs = "I am a teacher".split()
    syn = symmetrization(es, fs, corpus)
    ans = set([(1, 1), (1, 2), (2, 3), (3, 4), (4, 3)])
    assert syn == ans


def test_extract():

    # next alignment matrix is like
    #
    # | |x|x| | |
    # |x| | |x| |
    # | | | | |x|
    #
    es = range(1, 4)
    fs = range(1, 6)
    alignment = [(2, 1),
                 (1, 2),
                 (1, 3),
                 (2, 4),
                 (3, 5)]
    ans = set([(1, 1, 2, 3), (1, 3, 1, 5), (3, 3, 5, 5), (1, 2, 1, 4)])
    extract(es, fs, alignment) == ans

    # next alignment matrix is like
    #
    # |x| | | | | | | | | |
    # | |x|x|x| | | | | | |
    # | | | | | |x| | | | |
    # | | | | | | |x| | | |
    # | | | | | | | | | |x|
    # | | | | | | | | | |x|
    # | | | | | | | |x| | |
    # | | | | | | | |x| | |
    # | | | | | | | | |x| |
    #
    es = "michael assumes that he will stay in the house".split()
    fs = "michael geht davon aus , dass er im haus bleibt".split()
    alignment = set([(1, 1),
                     (2, 2),
                     (2, 3),
                     (2, 4),
                     (3, 6),
                     (4, 7),
                     (5, 10),
                     (6, 10),
                     (7, 8),
                     (8, 8),
                     (9, 9)])
    ans = set([(1, 1, 1, 1),
               (1, 2, 1, 4),
               (1, 2, 1, 5),
               (1, 3, 1, 6),
               (1, 4, 1, 7),
               (1, 9, 1, 10),
               (2, 2, 2, 4),
               (2, 2, 2, 5),
               (2, 3, 2, 6),
               (2, 4, 2, 7),
               (2, 9, 2, 10),
               (3, 3, 5, 6),
               (3, 3, 6, 6),
               (3, 4, 5, 7),
               (3, 4, 6, 7),
               (3, 9, 5, 10),
               (3, 9, 6, 10),
               (4, 4, 7, 7),
               (4, 9, 7, 10),
               (5, 6, 10, 10),
               (5, 9, 8, 10),
               (7, 8, 8, 8),
               (7, 9, 8, 9),
               (9, 9, 9, 9)])

    extract(es, fs, alignment) == ans


def test_phrase_extract():
    # next alignment matrix is like
    #
    # |x| | | | | | | | | |
    # | |x|x|x| | | | | | |
    # | | | | | |x| | | | |
    # | | | | | | |x| | | |
    # | | | | | | | | | |x|
    # | | | | | | | | | |x|
    # | | | | | | | |x| | |
    # | | | | | | | |x| | |
    # | | | | | | | | |x| |
    #
    es = "michael assumes that he will stay in the house".split()
    fs = "michael geht davon aus , dass er im haus bleibt".split()
    alignment = set([(1, 1),
                     (2, 2),
                     (2, 3),
                     (2, 4),
                     (3, 6),
                     (4, 7),
                     (5, 10),
                     (6, 10),
                     (7, 8),
                     (8, 8),
                     (9, 9)])
    ans = set([(('assumes',), ('geht', 'davon', 'aus')),
               (('assumes',), ('geht', 'davon', 'aus', ',')),
               (('assumes', 'that'),
                ('geht', 'davon', 'aus', ',', 'dass')),
               (('assumes', 'that', 'he'),
                ('geht', 'davon', 'aus', ',', 'dass', 'er')),
               (('assumes', 'that', 'he',
                 'will', 'stay', 'in', 'the', 'house'),
                ('geht', 'davon', 'aus', ',', 'dass',
                 'er', 'im', 'haus', 'bleibt')),
               (('he',), ('er',)),
               (('he', 'will', 'stay', 'in', 'the', 'house'),
                ('er', 'im', 'haus', 'bleibt')),
               (('house',), ('haus',)),
               (('in', 'the'), ('im',)),
               (('in', 'the', 'house'), ('im', 'haus')),
               (('michael',), ('michael',)),
               (('michael', 'assumes'),
                ('michael', 'geht', 'davon', 'aus')),
               (('michael', 'assumes'),
                ('michael', 'geht', 'davon', 'aus', ',')),
               (('michael', 'assumes', 'that'),
                ('michael', 'geht', 'davon', 'aus', ',', 'dass')),
               (('michael', 'assumes', 'that', 'he'),
                ('michael', 'geht', 'davon', 'aus', ',', 'dass', 'er')),
               (('michael',
                 'assumes',
                 'that',
                 'he',
                 'will',
                 'stay',
                 'in',
                 'the',
                 'house'),
                ('michael',
                 'geht',
                 'davon',
                 'aus',
                 ',',
                 'dass',
                 'er',
                 'im',
                 'haus',
                 'bleibt')),
               (('that',), (',', 'dass')),
               (('that',), ('dass',)),
               (('that', 'he'), (',', 'dass', 'er')),
               (('that', 'he'), ('dass', 'er')),
               (('that', 'he', 'will', 'stay', 'in', 'the', 'house'),
                (',', 'dass', 'er', 'im', 'haus', 'bleibt')),
               (('that', 'he', 'will', 'stay', 'in', 'the', 'house'),
                ('dass', 'er', 'im', 'haus', 'bleibt')),
               (('will', 'stay'), ('bleibt',)),
               (('will', 'stay', 'in', 'the', 'house'),
                ('im', 'haus', 'bleibt'))])

    phrase_extract(es, fs, alignment) == ans


if __name__ == '__main__':

    from sys import argv, stdin
    import kovfig

    delimiter = argv[1]
    # load file which will be trained
    modelfd = open(argv[2])
    sentenses = [line.rstrip().split(delimiter) for line
                 in modelfd.readlines()]
    # make corpus
    corpus = mkcorpus(sentenses)

    # train model from corpus
    f2e_train = _train_ibmmodel2(corpus, loop_count=kovfig.LOOP_COUNT)
    e2f_corpus = list(zip(*reversed(list(zip(*corpus)))))
    e2f_train = _train_ibmmodel2(e2f_corpus, loop_count=kovfig.LOOP_COUNT)

    # phrase extraction
    for line in stdin:
        _es, _fs = line.rstrip().split(delimiter)
        es = _es.split()
        fs = _fs.split()

        f2e = viterbi_alignment(es, fs, *f2e_train).items()
        e2f = viterbi_alignment(fs, es, *e2f_train).items()
        align = alignment(es, fs, e2f, f2e)  # symmetrized alignment

        # output matrix
        #from smt.utils.utility import matrix
        #print(matrix(len(es), len(fs), align, es, fs))

        ext = phrase_extract(es, fs, align)
        for e, f in ext:
            print("{}{}{}".format(''.join(e), delimiter, ''.join(f)))
