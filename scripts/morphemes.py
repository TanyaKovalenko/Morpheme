# coding=utf-8
import codecs
from collections import defaultdict

class WordMorphemes:
    prefixes = set()
    roots = set()
    suffixes = set()
    main_part = set()
    connecting_vowel = set()
    endings = set()
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
            print "LOAD"

            actions = {u'корень': 'roots', u'корни': 'roots',
                       u'приставка': 'prefixes', u'приставки': 'prefixes',
                       u'суффикс': 'suffixes', u'суффиксы': 'suffixes',
                       u'основа слова': 'main_part', u'основы': 'main_part',
                       u'соединительная гласная': 'connecting_vowel',
                       u'соединительные гласные': 'connecting_vowel',
                       u'окончание': 'endings', u'окончания': 'endings'}

            with codecs.open(self.path_to_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word_morphems = WordMorphemes()
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

                            # TODO: just for check
                            morph_list = filter(lambda x: len(x) != 0,
                                           map(lambda x: x.strip(), morpheme.split(',')))
                            morph_set = set(morph_list)

                            # NOTE: some words has more than one same roots
                            #if len(morph_list) != len(morph_set):
                            #    print word, '|', line
                            # if

                            setattr(word_morphems, actions[morpheme_name], morph_set)
                        # if
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
        cls.add_dict('../dicts/words_like_morphemes.txt')
    # def

    @classmethod
    def get(cls, word):
        if len(cls.__dicts) == 0:
            # TODO: it's for current implementation
            cls.__load_default_dict()
        # if

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
        for d in cls.__dicts:
            if word in d:
                return True
            # if
        # for

        return False
    # def

    @classmethod
    def morphemes(cls):
        result = WordMorphemes()

        for d in cls.__dicts:
            for value in d.morphemes():
                result.roots += value.roots
            # for
        # for

        return result
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
    #morphs = WordMorphemeDicts.get(u'кусок')

    result = WordMorphemeDicts.morphemes()

    print len(result.roots)
# if
