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
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            word_morphems = Word_Morpheme()
            word = line.split(':')[0]
            start_inx = line.find(': ') + len(': ')
            line = line[start_inx:len(line)]
            morphemes = line.split(';')
            for item in morphemes:
                morpheme = item.split(u'—')[0].strip()
                if (len(item.split(u'—')) > 1):
                    morpheme_name = item.split(u'—')[1].strip()
                    if (morpheme_name == u'корень') or (morpheme_name == u'корни'):
                        roots = morpheme.split(',')
                        word_morphems.roots = roots
                    if (morpheme_name == u'приставка') or (morpheme_name == u'приставки'):
                        prefixies = morpheme.split(',')
                        word_morphems.prefixies = prefixies
                    if (morpheme_name == u'суффикс') or (morpheme_name == u'суффиксы'):
                        suffixies = morpheme.split(',')
                        word_morphems.suffixies = suffixies
                    if (morpheme_name == u'основа слова'):
                        main_part = morpheme.split(',')
                        word_morphems.main_part = main_part
                    if (morpheme_name == u'соединительная гласная'):
                        connecting_vowel = morpheme.split(',')
                        word_morphems.connecting_vowel = connecting_vowel
                    if (morpheme_name == u'окончание'):
                        ending = morpheme.split(',')
                        word_morphems.ending = ending
            word_morhemes_dict[word] = word_morphems

def getMorphemes(word):
    form_dict()
    return word_morhemes_dict[word]

if __name__ == "__main__":
    form_dict()

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

        if count <= 2:
            print suf, "(%s): " % (str(count)), ', '.join(d_words[suf])
        # if
    # for
# if
