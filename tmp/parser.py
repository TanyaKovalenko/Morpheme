# coding=utf-8
import codecs

def norm(word):
    return word.strip().lower().replace(u'ё', u'e')
# def

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
    # for
# with
