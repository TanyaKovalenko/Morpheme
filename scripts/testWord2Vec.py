# coding=utf-8
import os
import codecs
import gensim
import logging
import re
import numpy as np
import morphemes
import parse_word
from operator import itemgetter
from suffixes_prefix_parser import SuffixPrefixParser
from collections import defaultdict

class model(object):

    def __init__(self, path_to_model):

        self.model = gensim.models.Word2Vec.load_word2vec_format(path_to_model, binary=True)

        self.word_from_model_word = defaultdict(lambda: list())
        self.model_word_from_word = defaultdict(lambda: list())

        for inx in range(len(self.model.vocab)):
            self.word_from_model_word[self.model.index2word[inx]] = self.model.index2word[inx].split('_')[0]
            self.model_word_from_word[self.model.index2word[inx].split('_')[0]] = self.model.index2word[inx]


    def get_new_morphemes_model(self, path_to_pref, path_to_suff):
        print "get new model..."
        # SuffixPrefixParser is used to get meanings of morphemes
        pref_parser = SuffixPrefixParser(path_to_pref)
        suff_parser = SuffixPrefixParser(path_to_suff)
        morpheme_parser = [pref_parser, suff_parser]
        new_model = {}

        for inx in range(len(self.model.vocab)):
            # model_word is a word from w2v model (it contains part of speech for this word in format wordname_POSNAME)
            model_word = self.model.index2word[inx]

            # word - word from model after remove it's part of speech
            word = self.word_from_model_word[model_word]

            # old_vector - w2v vector of word
            old_vec = self.model[model_word]
            if word == u"поросятина":
                print "WORD = " + word

            # getMorphemes function returns the object with morphemes of a word
            word_morphemes = parse_word.getMorphemes(word)

            if word == u"поросятина":
                print "PREF = "
                print ', '.join(word_morphemes.prefixes)
                print "ROOTS = "
                print ', '.join(word_morphemes.roots)
                print "SUFF = "
                print ', '.join(word_morphemes.suffixes)

            morphemes_lists = [word_morphemes.prefixes, word_morphemes.suffixies]

            morphemes_vects = list()
            for i in range(len(morphemes_lists)):
                morphemes_list = morphemes_lists[i]
                for inx in range(len(morphemes_list)):
                    # methon suffixes_prefix_parser.parser.get return list of triples [[meaning1, examples, specs], [], [] ]
                    if word == u"поросятина":
                        print "morpheme: "
                        print morphemes_list[inx].strip()
                    meanings, _, _ = morpheme_parser[i].get(morphemes_list[inx].strip())
                    if word == u"поросятина":
                        print ' ,'.join(meanings)
                    sims_to_word = list()
                    if (len(meanings) > 0):
                        for mean in meanings:
                            if self.model_word_from_word.get(mean):
                                sims_to_word.append((mean, abs(self.model.similarity(self.model_word_from_word[mean], self.model_word_from_word[word]))))
                    if len(sims_to_word) > 0:
                        max_sim = max(sims_to_word, key = lambda item:item[0])[1]
                        max_sim_mean = max(sims_to_word, key = lambda item:item[0])[0]
                        if word == u"поросятина":
                            print "Max sim = " + max_sim
                            print "Max mean = " + max_sim_mean
                        morphemes_vects.append((self.model[self.model_word_from_word[max_sim_mean]], max_sim))

            new_model[model_word] = old_vec

            for vect, sim in morphemes_vects:
                sim_vect_list = [item * sim for item in vect]
                old_vec = np.add(old_vec, sim_vect_list)
                new_vec = [item / len(morphemes_vects) for item in old_vec]
            new_model[model_word] = new_vec

        return new_model


# --------------------------------------------------------- Form vocabulary from input data ( start ) ---------------------------------------------------------------------- 
dataDir = '/Users/ruslan/Tanya/ArticleMorphems/data'
sentences = list()
vocab_set = set()
for fname in os.listdir(dataDir):
    for line in codecs.open(os.path.join(dataDir, fname), 'r', encoding='utf-8'):
        sentences.append(line.split())
        line=line.replace('.',' ')
        line=line.replace('!',' ')
        line=line.replace(',',' ')
        line=line.replace('?',' ')
        line=line.replace(':',' ')
        line=line.replace('(',' ')
        line=line.replace(')',' ')
        line=line.replace('[',' ')
        line=line.replace(']',' ')
        line=line.replace('"',' ')
        line=line.replace(';',' ')
        line=line.replace('-',' ')
        line=line.replace('0',' ')
        line=line.replace('1',' ')
        line=line.replace('2',' ')
        line=line.replace('3',' ')
        line=line.replace('4',' ')
        line=line.replace('5',' ')
        line=line.replace('6',' ')
        line=line.replace('7',' ')
        line=line.replace('8',' ')
        line=line.replace('9',' ')
        for word in line.split():
            vocab_set.add(word.lower())
# --------------------------------------------------------- Form vocabulary from input data ( end ) ----------------------------------------------------------------------
#
#
#
#
# --------------------------------------------------------- Form dict of russian words (start) ---------------------------------------------------------------------------
#russianDictDir = '/Users/ruslan/Tanya/ArticleMorphems/dicts'
#russian_dict_set = set()
#for fname in os.listdir(russianDictDir):
#        for line in codecs.open(os.path.join(russianDictDir, fname), 'r', encoding='utf-8'):
#                if '"' in line:
#			word=line.split('"')[1]
#			if len(word) > 2: 
#                		russian_dict_set.add(word.lower())
# --------------------------------------------------------- Form dict of russian words ( end ) ---------------------------------------------------------------------------
#

if __name__ == "__main__":
    # ------------ web --------------------
    #web_model_size = 353608
    #web_model_file_name = 'web.model.bin'

    # ------------ news ------------------
    #news_model_size = 124590
    #news_model_file_name = 'news.model.bin'

    # ---------- ruscorpora -------------
    #rus_model_size = 184973
    #rus_model_file_name = 'ruscorpora.model.bin'

    # ---------- ruwikiruscorpora -------------
    ruwiki_model_size = 392339
    ruwiki_model_file_name = '../../ruwikiruscorpora.model.bin'

    pref_file_name = "../dicts/prefixes.txt"
    suff_file_name = "../dicts/suffixes.txt"

    ruwiki_model = model(ruwiki_model_file_name)

    my_new_model = ruwiki_model.get_new_morphemes_model(pref_file_name, suff_file_name)

