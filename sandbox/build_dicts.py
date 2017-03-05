# coding=utf-8
from scripts.morphemes import WordMorphemeDicts
from collections import defaultdict
import pymorphy2
import codecs

morph = pymorphy2.MorphAnalyzer()

def flush_to_file(d, file_name):
    with codecs.open(file_name, 'w', encoding='utf-8') as fout:
        for key, values in d.iteritems():
            # -------------- #
            specs = defaultdict(set)

            for v in values:
                p = morph.parse(v)[0]
                #specs[(p.tag.POS, p.tag.gender)].add(v)
                specs[p.tag.POS].add(v)
            # for
            # -------------- #

            line = key + ': '

            for spec, words in specs.iteritems():
                pos = spec
                line += '[' + ', '.join(words) + ']'
                line += '{' + str(pos) +  '};' #', ' + str(gender) + '};'
            # for

            fout.write(line + '\n')
        # for
    # with
# def

suffixes_words = defaultdict(set)
prefixes_words = defaultdict(set)
roots_words = defaultdict(set)
endings_words = defaultdict(set)

for word in WordMorphemeDicts.words():
    morphemes = WordMorphemeDicts.get(word)

    for x in morphemes.suffixes: suffixes_words[x].add(word)
    for x in morphemes.prefixes: prefixes_words[x].add(word)
    for x in morphemes.roots: roots_words[x].add(word)
    for x in morphemes.endings: endings_words[x].add(word)
# for

flush_to_file(suffixes_words, 'suffixes_words')
#flush_to_file(prefixes_words, 'prefixes_words')
#flush_to_file(roots_words, 'roots_words')
flush_to_file(endings_words, 'endings_words')