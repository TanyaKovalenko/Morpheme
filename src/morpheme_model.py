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
from morphemes import WordMorphemeDicts

class model(object):

    def __init__(self, path_to_model):

        self.model = gensim.models.Word2Vec.load_word2vec_format(path_to_model, binary=True)

        self.word_from_modelWord = defaultdict(lambda: list())
        self.modelWord_from_word = defaultdict(lambda: list())

        for inx in range(len(self.model.vocab)):
            self.word_from_modelWord[self.model.index2word[inx]] = self.model.index2word[inx].split('_')[0]
            self.modelWord_from_word[self.model.index2word[inx].split('_')[0]] = self.model.index2word[inx]
        
        self.roots_avg_vects = self.form_roots_vects()

    def form_roots_vects(self):
        roots_vects = defaultdict(list)
        roots_avg_vects = dict()
        for word in WordMorphemeDicts.words():
            if word in self.modelWord_from_word:
                model_word = self.modelWord_from_word[word]
                for root in WordMorphemeDicts.get(word).roots:
                    vect = self.model[model_word]
                    roots_vects[root].append(vect)
                                                                                             
        for root in roots_vects:
            roots_avg_vects[root] = sum(roots_vects[root]) / len(roots_vects[root])
        
        return roots_avg_vects

    def recalculate_vect(self, word, path_to_pref, path_to_suff, min_sim_value):
        # SuffixPrefixParser is used to get meanings of morphemes
        pref_parser = SuffixPrefixParser(path_to_pref)
        suff_parser = SuffixPrefixParser(path_to_suff)
        morpheme_parser = [pref_parser, suff_parser]
        # segment_word function returns the object with morphemes of a word
        word_morphemes = segmentation.getMorphemes(word)
        if word_morphemes is not None:
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
                            if self.modelWord_from_word.get(mean):
                                if self.modelWord_from_word.get(word):
                                    sims_to_word.append((mean, abs(self.model.similarity(self.modelWord_from_word[mean], self.modelWord_from_word[word]))))
                                else:
                                    list_words_for_sim = self.model.similar_by_vector(self.roots_avg_vects[word], topn=1, restrict_vocab=None)
                                    word_for_sim, _ = list_words_for_sim[0]
                                    sims_to_word.append((mean, abs(self.model.similarity(self.modelWord_from_word[mean], word_for_sim))))
                        if len(sims_to_word) > 0:
                            max_sim = max(sims_to_word, key = lambda item:item[0])[1]
                            max_sim_mean = max(sims_to_word, key = lambda item:item[0])[0]          
                            if (max_sim > min_sim_value):
                                morphemes_vects.append((self.model[self.modelWord_from_word[max_sim_mean]], max_sim))                
        
        result_new_vect = list()
        
        if word not in self.modelWord_from_word:
            if word not in self.roots_avg_vects:
                return None
            else:
                result_new_vect = self.roots_avg_vects[word]
        else:
            # model_word is a word from w2v model (it contains part of speech for this word in format wordname_POSNAME)
            model_word = self.modelWord_from_word[word]        
            # old_vector - w2v vector of word
            old_vec = self.model[model_word]
            result_new_vect = old_vec
         
        sims = list()
        for _, sim in morphemes_vects:
            sims.append(sim)
        
        sum_of_sims = sum(sims)    
        if ((len(morphemes_vects) > 0) and (sum_of_sims != 0)):
            for vect, sim in morphemes_vects:
                morpheme_vect = [item * (sim / sum_of_sims) for item in vect]
                result_new_vect = np.add(result_new_vect,  morpheme_vect)
            result_new_vect = 0.5 * result_new_vect
            
        return result_new_vect
           
    def get_new_morphemes_model(self):
        new_model = {}
        for word_inx in range(len(self.model.vocab)):
            # model_word is a word from w2v model (it contains part of speech for this word in format wordname_POSNAME)
            model_word = self.model.index2word[word_inx]

            # word - word from model after remove it's part of speech
            word = self.word_from_modelWord[model_word]
             
            #recalculate vector of the word
            new_model[model_word] = recalculate_vect(word, 0.1)

        return new_model

def load_model(file_name):
    # TODO: it's for current implementation
    print "Loading word2vec model..."
    dir_name = os.path.dirname(os.path.realpath(__file__))
    name = os.path.join(*[dir_name, '..', '..', file_name])
    the_model = model(name)
    print "Done."
    return the_model


#if __name__ == "__main__":
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
    #ruwiki_model_size = 392339
    #ruwiki_model_file_name = 'ruwikiruscorpora.model.bin'
    
    #dir_name = os.path.dirname(os.path.realpath(__file__))

    #pref_file_name = os.path.join(*[dir_name, '..', 'dicts', 'prefixes.txt'])
    #suff_file_name = os.path.join(*[dir_name, '..', 'dicts', 'suffixes.txt']) 

    #ruwiki_model = load_model(ruwiki_model_file_name)
    #print ruwiki_model.model.similar_by_vector(ruwiki_model.model[ruwiki_model.modelWord_from_word[u'машина']], topn=1, restrict_vocab=None)
    #my_new_model = ruwiki_model.get_new_morphemes_model()
    
    #print ruwiki_model.recalculate_vect(u"поросятина", pref_file_name, suff_file_name, 0.1)
