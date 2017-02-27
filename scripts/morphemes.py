# coding=utf-8
import codecs
from collections import defaultdict

file_name = '../dicts/words_like_morhemes.txt'

class Word_Morpheme:
    prefixies = list()
    roots = list()
    suffixies = list()
    main_part = list()
    connecting_vowel = list()
    ending = list()

word_morhemes_dict = {}

def form_dict():
    actions = {u'корень': 'roots', u'корни': 'roots',
               u'приставка': 'prefixies', u'приставки': 'prefixies',
               u'суффикс': 'suffixies', u'суффиксы': 'suffixies',
               u'основа слова': 'main_part', u'основы': 'main_part',
               u'соединительная гласная': 'connecting_vowel',
               u'соединительные гласные': 'connecting_vowel',
               u'окончание': 'ending', u'окончания': 'ending'}

    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            word_morphems = Word_Morpheme()
            word = line.split(':')[0]
            start_inx = line.find(': ') + len(': ')
            line = line[start_inx:len(line)]
            morphemes = line.split(';')
            for item in morphemes:
                pos = item.rfind('-', 0)

                if pos != -1:
                    item = item.replace('.', '')
                    morpheme = item[:pos - 1].strip()
                    morpheme_name = item[pos + 1:].strip()

                    setattr(word_morphems, actions[morpheme_name], morpheme.split(','))
                # if
            # for

            word_morhemes_dict[word] = word_morphems
        # for
    # with
# def

def getMorphemes(word):
    form_dict()
    return word_morhemes_dict[word]

if __name__ == "__main__":
    form_dict()

    print word_morhemes_dict[u'наибольший'].ending

    """
    d = defaultdict(lambda: 0)
    d_words = defaultdict(list)

    for k, obj in word_morhemes_dict.iteritems():
        for suf in obj.suffixies:
            d[suf.strip()] += 1
            d_words[suf.strip()].append(k.strip())
        # for
    # for

    # ------------ #
    l = [(value, key) for key, value in d.iteritems()]

    for t in sorted(l):
        count, suf = t

        if count <= 10:
            print suf, "(%s): " % (str(count)), ', '.join(d_words[suf])
        # if
    # for
    """
# if
