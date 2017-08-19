# coding=utf-8
import os
import re
import codecs
import gensim
import logging
import numpy as np

from operator import itemgetter
from collections import defaultdict

import morphemes
import segmentation_JULIA as segmentation

from suffixes_prefix_parser import SuffixPrefixParser

class model(object):

    def __init__(self, path_to_model):

        self.model = gensim.models.Word2Vec.load_word2vec_format(path_to_model, binary=True)

        self.word_from_model_word = defaultdict(lambda: list())
        self.model_word_from_word = defaultdict(lambda: list())

        for inx in range(len(self.model.vocab)):
            self.word_from_model_word[self.model.index2word[inx]] = self.model.index2word[inx].split('_')[0]
            self.model_word_from_word[self.model.index2word[inx].split('_')[0]] = self.model.index2word[inx]


    def get_new_morphemes_model(self, path_to_pref, path_to_suff):
        # SuffixPrefixParser is used to get meanings of morphemes
        pref_parser = SuffixPrefixParser(path_to_pref)
        suff_parser = SuffixPrefixParser(path_to_suff)
        morpheme_parser = [pref_parser, suff_parser]
        new_model = {}
        good_mean = 0
        for word_inx in range(len(self.model.vocab)):
            # model_word is a word from w2v model (it contains part of speech for this word in format wordname_POSNAME)
            model_word = self.model.index2word[word_inx]

            # word - word from model after remove it's part of speech
            word = self.word_from_model_word[model_word]

            # old_vector - w2v vector of word
            old_vec = self.model[model_word]
            
            test_word = u"бездельник"
            # segment_word function returns the object with morphemes of a word
            word_morphemes = segmentation.getMorphemes(word)
            # check if it's possible to split the word into morphemes
             
            if word_morphemes is not None:
                morphemes_count = len(word_morphemes.prefixes) + len(word_morphemes.roots) + len(word_morphemes.suffixes)
            
                morphemes_lists = [word_morphemes.prefixes, word_morphemes.suffixes]
                morphemes_vects = list()
                for i in range(len(morphemes_lists)):
                    morphemes_list = morphemes_lists[i]
                    for inx in range(len(morphemes_list)):
                        # method suffixes_prefix_parser.parser.get return list of triples [[meaning1, examples, specs], [], [] ]
                        meanings, _, _ = morpheme_parser[i].get(morphemes_list[inx].strip())
                        sims_to_word = list()
                        if (len(meanings) > 0):
                            for mean in meanings:
                                if self.model_word_from_word.get(mean):
                                    sims_to_word.append((mean, abs(self.model.similarity(self.model_word_from_word[mean], self.model_word_from_word[word]))))
                        if len(sims_to_word) > 0:
                            max_sim = max(sims_to_word, key = lambda item:item[0])[1]
                            max_sim_mean = max(sims_to_word, key = lambda item:item[0])[0]
                            if (max_sim > 0.1):
                                good_mean += 1 
                                morphemes_vects.append((self.model[self.model_word_from_word[max_sim_mean]], max_sim))

                new_model[word] = old_vec
            
                if (len(morphemes_vects) > 0):
                    for morph_inx in range(morphemes_count - len(morphemes_vects)):
                        old_vec = np.add(old_vec, old_vec)
                    for vect, sim in morphemes_vects:
                        sim_vect_list = [item * sim for item in vect]
                        old_vec = np.add(old_vec, sim_vect_list)
                    new_vec = [item / morphemes_count for item in old_vec]
                    new_model[model_word] = new_vec

        return new_model

def load_model(file_name):
    # TODO: it's for current implementation
    print "Loading word2vec model..."
    dir_name = os.path.dirname(os.path.realpath(__file__))
    name = os.path.join(*[dir_name, '..', '..', file_name])
    the_model = model(name)
    return the_model


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
    ruwiki_model_file_name = 'ruwikiruscorpora.model.bin'

    dir_name = os.path.dirname(os.path.realpath(__file__))

    pref_file_name = os.path.join(*[dir_name, '..', 'dicts', 'prefixes.txt'])
    suff_file_name = os.path.join(*[dir_name, '..', 'dicts', 'suffixes.txt']) 

    ruwiki_model = load_model(ruwiki_model_file_name)

    my_new_model = ruwiki_model.get_new_morphemes_model(pref_file_name, suff_file_name)
    
    print my_new_model[u"поросятина"]
