# coding=utf-8
import codecs

def tag(raw):
    d = { u'корень':  'r',
          u'суффикс': 's',
          u'нулевой суффикс': 'ns',
          u'формообразующий суффикс': 'fs',
          u'приставка': 'p',
          u'окончание': 'e',
          u'соединительная гласная': 'v',}

    if raw not in d:
        print raw
    # if
    assert raw in d

    return d[raw]
# def

with codecs.open("words_like_morhemes.txt", "r", encoding='utf-8') as fin:
    for line in fin:
        tokens = line.split(':')
        assert len(tokens) == 2

        word = tokens[0].strip().lower().replace(u'ё', u'е').replace(u'о́', u'о')
        word_morphs = []

        tokens = filter(lambda x: len(x), map(lambda x: x.strip(), tokens[1].split(';')))
        assert len(tokens) >= 1

        tokens_set = set()
        for token in tokens:
            if token in tokens_set:
                continue
            # if

            morphs = map(lambda x: x.strip().lower().replace(u'ё', u'е').replace(u'о́', u'').replace(u'е', u'е'), token.split(u'-'))
            
            try:
                assert len(morphs) == 2
            except:
                print word, token, len(morphs)
            # try

            if morphs[1] not in word:
                print token, morphs[1], word
            # if
            assert morphs[1] in word
                
            word_morphs.append((tag(morphs[0]), morphs[1]))

            tokens_set.add(token)
        # for
    # for
# with
