# coding=utf-8
import codecs
from utils.common import norm


def tag(raw):
    d = { u'корень':  'r',
          u'суффикс': 's',
          u'нулевой суффикс': 'ns',
          u'формообразующий суффикс': 'fs',
          u'приставка': 'p',
          u'окончание': 'e',
          u'соединительная гласная': 'v'}

    assert raw in d

    return d[raw]
# def

count = 0
error = 0
more_than_one_roots = 0

more_than_one_root_count = 0
more_than_one_root_length = 0
more_than_one_root_prcnt = 0
more_than_one_root_all = 0

with codecs.open("words_like_morhemes.txt", "r", encoding='utf-8') as fin:
    for line in fin:
        tokens = line.split(':')
        assert len(tokens) == 2

        word = norm(tokens[0])
        word_morphs = []

        tokens = filter(lambda x: len(x), map(lambda x: x.strip(), tokens[1].split(';')))
        assert len(tokens) >= 1

        word_to_check = ''
        for token in tokens:
            morphs = map(lambda x: norm(x), token.split(u'-'))

            assert len(morphs) == 2
            assert morphs[1] in word

            word_morphs.append((tag(morphs[0]), morphs[1]))
            word_to_check += morphs[1]
        # for

        assert word.replace('-', '') == word_to_check

        # ------------------------------------------ #
        # calculate statistic
        # check how many roots are there
        root_count = 0
        root_l = 0
        for t, m in word_morphs:
            if t == 'r':
                root_count += 1
                root_l += len(m)
            # if
        # for

        if root_count > 1:
            more_than_one_roots += 1

            more_than_one_root_count += root_count
            more_than_one_root_length += root_l

            for t, m in word_morphs:
                if t == 'r' and len(m) <= 4:
                    more_than_one_root_prcnt += 1
                # if

                more_than_one_root_all += 1
            # for
        # if
        # ------------------------------------------ #

        count += 1
    # for
# with

print count, ((error + 0.0) / count) * 100
print 'More than one root % :', ((more_than_one_roots + 0.0) / count) * 100
print 'Avg root length for more than one root % :', ((more_than_one_root_length + 0.0) / more_than_one_root_count)
print 'More than one root length prcnt :', ((more_than_one_root_prcnt + 0.0) / more_than_one_root_all) * 100