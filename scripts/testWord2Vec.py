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
        good_mean = 0
        for word_inx in range(len(self.model.vocab)):
            # model_word is a word from w2v model (it contains part of speech for this word in format wordname_POSNAME)
            model_word = self.model.index2word[word_inx]

            # word - word from model after remove it's part of speech
            word = self.word_from_model_word[model_word]

            # old_vector - w2v vector of word
            old_vec = self.model[model_word]
            
            test_word = u"бездельник"


            # getMorphemes function returns the object with morphemes of a word
            word_morphemes = parse_word.getMorphemes(word)


            morphemes_count = len(word_morphemes.prefixes) + len(word_morphemes.roots) + len(word_morphemes.suffixes)

            morphemes_lists = [word_morphemes.prefixes, word_morphemes.suffixes]
            morphemes_vects = list()
            for i in range(len(morphemes_lists)):
                morphemes_list = morphemes_lists[i]
                for inx in range(len(morphemes_list)):
                    # methon suffixes_prefix_parser.parser.get return list of triples [[meaning1, examples, specs], [], [] ]
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

def load_model(file_name):
    # TODO: it's for current implementation
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
