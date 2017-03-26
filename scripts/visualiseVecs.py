# coding=utf-8
import os
import re
import codecs
import gensim
import logging
import numpy as np
import matplotlib.pyplot as plt

from testWord2Vec import model
from operator import itemgetter
from suffixes_prefix_parser import SuffixPrefixParser
from collections import defaultdict
from sklearn.manifold import TSNE

def getWordVecs(words):
    vecs = []
    for word in words:
        word = word.replace('\n', '')
        try:
            if ruwiki_model.model_word_from_word.get(word) != None:
                vecs.append(ruwiki_model.model[ruwiki_model.model_word_from_word[word]].reshape((1,300)))
        except KeyError:
            continue
    vecs = np.concatenate(vecs)
    return np.array(vecs, dtype='float') #TSNE expects float type values

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
    ruwiki_model = load_model(ruwiki_model_file_name)

    dir_name = os.path.dirname(os.path.realpath(__file__))
    pref_file_path = os.path.join(*[dir_name, '..', 'dicts', 'prefixes.txt'])
    suff_file_path = os.path.join(*[dir_name, '..', 'dicts', 'suffixes.txt'])
    finTerms_file_path = os.path.join(*[dir_name, '..', 'dicts', 'finTerms.txt'])

    with codecs.open(finTerms_file_path, 'r', encoding='utf-8') as infile:
        fin_words = infile.readlines()
    
    fin_vecs = getWordVecs(fin_words)
    for vec in fin_vecs:
        with codecs.open('fin_vects.txt', 'a', encoding='utf-8') as outfile:
                outfile.write(str(vec).decode('utf-8'))
                outfile.write('\n')
    
    fin_vecs = np.nan_to_num(fin_vecs)

    ts = TSNE(2)
    reduced_vecs = ts.fit_transform(fin_vecs)

    #color points by word group to see if Word2Vec can separate them
    for i in range(len(reduced_vecs)):
        color = 'b'
        plt.plot(reduced_vecs[i,0], reduced_vecs[i,1], marker='o', color=color, markersize=8)
