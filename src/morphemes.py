# coding=utf-8
import codecs
from collections import defaultdict
from utils.common import norm
import os

class WordMorphemes:

    TAGS = ['P', 'R', 'S', 'C', 'E']

    def __init__(self):
        self.prefixes = list()
        self.roots = list()
        self.suffixes = list()
        self.main_part = list()
        self.connecting_vowel = list()
        self.endings = list()

        # it contains pairs (tag, morpheme)
        self.all_in_order = list()
        # it has length the same as a word,
        # every element contains corresponding tags for every letter
        self.tag_for_letter = list()
    # def
# class

class WordMorphemeDicts:

    # ------------------- #
    # Nested private class
    # ------------------- #
    class __WordMorphemeDict(object):

        def __init__(self, path_to_file=None):
            if not path_to_file:
                raise Exception("Path to dictionary with word-morphemes mapping is not specified!")
            # if

            self.path_to_file = path_to_file.strip()
            self.is_init = False
            self.words_morphemes = {}
            
            self.__check_on_load()
        # def

        def __load(self):
            actions = {u'корень': 'roots', u'корни': 'roots',
                       u'приставка': 'prefixes', u'приставки': 'prefixes',
                       u'суффикс': 'suffixes', u'суффиксы': 'suffixes',
                       u'формообразующий суффикс': 'suffixes',
                       u'основа слова': 'main_part', u'основы': 'main_part',
                       u'соединительная гласная': 'connecting_vowel',
                       u'соединительные гласные': 'connecting_vowel',
                       u'окончание': 'endings', u'окончания': 'endings'}

            with codecs.open(self.path_to_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word_morphems = WordMorphemes()
                    word = norm(line.split(':')[0])

                    start_inx = line.find(': ') + len(': ')
                    line = line[start_inx:len(line)]
                    morphemes = line.split(';')
                    for item in morphemes:
                        pos = item.find('-', 0)

                        if pos != -1:
                            item = item.replace('.', '')
                            morpheme_name = item[:pos].strip()
                            morpheme = item[pos + 1:].strip()

                            morph_list = filter(lambda x: len(x) != 0,
                                           map(norm, morpheme.split(',')))
                            
                            # Lets add morheme in order with corresponding tag
                            # to identify morpheme further. Tag is made from
                            # the first letter, then 'suffixes' will stay 'S'.
                            # Exlude 'M', because 'main_part' is not a morpheme.
                            for m in morph_list:
                                try:
                                    TAG = actions[morpheme_name][:1].upper()
                                except:
                                    continue
                                # try
                                
                                if TAG != 'M' and len(m):
                                    word_morphems.all_in_order.append((TAG, m))
                                # if
                            # for

                            morph_set = set(morph_list)

                            # NOTE: some words has more than one same roots
                            #if len(morph_list) != len(morph_set):
                            #    print word, '|', line
                            # if
                            
                            try:
                                setattr(word_morphems, actions[morpheme_name], list(morph_set))
                            except:
                                # NOTE: skip key-errors, ie when morpheme_name is not in actions
                                pass
                            # try
                        # if
                    # for

                    # map tag for every letter
                    word_morphems.tag_for_letter = [''] * len(word)
                    letter_inx = 0
                    for tag, sub in word_morphems.all_in_order: 
                        for _ in range(len(sub)):
                            word_morphems.tag_for_letter[letter_inx] = tag
                            letter_inx += 1
                            # for
                    # for

                    self.words_morphemes[word] = word_morphems
                # for
            # with

            self.is_init = True
        # def

        def __check_on_load(self):
            if not self.is_init:
                self.__load()

                if not self.is_init:
                    raise Exception("Dictionary still not initialized. Check that '__load' method works fine")
                # if
             # if
        # def

        def get(self, word):
            self.__check_on_load()
            return self.words_morphemes[word]
        # def

        def __contains__(self, word):
            return word in self.words_morphemes
        # def

        def words(self):
            self.__check_on_load()
            return self.words_morphemes.keys()
        # def

        def morphemes(self):
            self.__check_on_load()
            return self.words_morphemes.values()
        # def

        def __len__(self):
            return len(self.words_morphemes)
        # def
    # class
    # ------------------- #

    __dicts = []

    @classmethod
    def __load_default_dict(cls):
        # TODO: it's for current implementation
        if len(cls.__dicts) == 0:
            dir_name = os.path.dirname(os.path.realpath(__file__))
            file_name = os.path.join(*[dir_name, '..', 'dicts', 'all_words_like_morphemes.txt'])

            cls.add_dict(file_name)
        # if
    # def

    @classmethod
    def get(cls, word):
        cls.__load_default_dict()

        for d in cls.__dicts:
            # TODO: it returns the first entrance, it could be wrong
            #       but no need more for the first implementation
            if word in d:
                return d.get(word)
            # if
        # for

        return None
    # def

    @classmethod
    def contains(cls, word):
        cls.__load_default_dict()

        for d in cls.__dicts:
            if word in d:
                return True
            # if
        # for

        return False
    # def

    @classmethod
    def words(cls):
        cls.__load_default_dict()

        set_words = set()

        for d in cls.__dicts:
            set_words.update(set(d.words()))
        # for

        return set_words
    # def

    @classmethod
    def morphemes(cls):
        cls.__load_default_dict()

        # local func-helper
        def apply_to_attr(obj, func):
            for name in WordMorphemes.__dict__.keys():
                if name.find('__') == -1:
                    func(obj, name)
                # if
            # for
        # def

        res_obj = WordMorphemes()

        # transform to sets
        apply_to_attr(res_obj, lambda o, name: setattr(o, name, set()))

        for d in cls.__dicts:
            for value in d.morphemes():
                apply_to_attr(res_obj, lambda o, name:
                    getattr(o, name).update(getattr(value, name)))
            # for
        # for

        # transform to lists
        apply_to_attr(res_obj, lambda o, name: setattr(o, name, list(getattr(o, name))))

        return res_obj
    # def

    @classmethod
    def add_dict(cls, path_to_file=None):
        for d in cls.__dicts:
            if d.path_to_file == path_to_file.strip():
                raise Exception("File with the same name is already uploaded!")
            # if
        # for

        cls.__dicts.append(cls.__WordMorphemeDict(path_to_file))
    # def
# class

if __name__ == "__main__":
    result = WordMorphemeDicts.morphemes()
# if
