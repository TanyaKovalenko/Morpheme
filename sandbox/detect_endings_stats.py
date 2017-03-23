# coding=utf-8
from scripts.morphemes import WordMorphemeDicts
import codecs

# стеснительно
morphemes = WordMorphemeDicts.get(u'прорезывая')

for t, m in morphemes.all_in_order:
    print t, m
# for

#for word in WordMorphemeDicts.words():
#    morphemes = WordMorphemeDicts.get(word)

#    morphemes.all_in_or
# for
