# coding=utf-8
from scripts.morphemes import WordMorphemeDicts
from collections import defaultdict

def morpheme_pos(word):
    morphemes = WordMorphemeDicts.get(word)

    morphs = []

    # Make order of search following: endings first, the suffixes, they are ordered by decreasing length
    for x in morphemes.endings: morphs.append(('e', -len(x), x))
    for x in morphemes.suffixes: morphs.append(('s', -len(x), x))
    for x in morphemes.connecting_vowel: morphs.append(('v', -len(x), x))
    morphs = sorted(morphs)

    result = []
    pos = len(word)
    repeat = 0

    try:
        while len(morphs):
            inx = 0
            found = False

            for tag, _, m in morphs:
                tail = word[pos - len(m): pos]

                #if word.find('-') != -1:
                #    print word, tail, m, pos, inx
                # if

                if tail == m:
                    #s = ''
                    #for _, _, t in morphs:
                    #    s += ',' + t

                    #print 'MATCH', s
                    pos -= len(m)

                    result.append((tag, m))
                    found = True
                    break
                # if

                inx += 1
            # for

            """
            if not found:
                # check whether word with two roots and dash
                dash_pos = word.find('-')

                # check that no infinit loops here
                if repeat == 3:
                    break
                # if

                if dash_pos != -1:
                    pos = dash_pos
                    repeat += 1
                    continue
                # if
            # if
            """

            morphs.pop(inx)
        # while
    except:
        """
        s = ''
        for _, _, t in morphs:
            s += ', ' + t
        # for

        print word, ' | ', s

        for tag, m in result:
            print tag, m
        # for
        """

        return False
    # try

    return True
# def

def get(word, inx):
    if inx < 0 or inx >= len(word):
        return ''
    # if

    return word[inx]
# def

two_letter_morpheme = defaultdict(lambda: 0)
two_letter_morpheme_all = 0

inx = 0

#morpheme_pos(u'покаявшийся')
#morpheme_pos(u'феодально-крепостнический')
#morpheme_pos(u'купля-продажа')
#morpheme_pos(u'каштаново-бурый')

count = 0

for word in WordMorphemeDicts.words():
    morphemes = WordMorphemeDicts.get(word)

    if not morpheme_pos(word):
        count += 1
    # if
# for

print count
