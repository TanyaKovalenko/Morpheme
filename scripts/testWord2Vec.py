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
			

			pref_meanings = list()
                        for inx in range(len(word_morphemes.prefixes)):
                                # methon suffixes_prefix_parser.parser.get return list of triples [[meaning1, examples, specs], [], [] ]
                                if word == u"поросятина":
                                        print "pref: "
                                        print word_morphemes.prefixes[inx].strip()
                                meanings, _, _ = pref_parser.get(word_morphemes.prefixes[inx].strip())
                                if word == u"поросятина":
                                        print ' ,'.join(meanings)
                                sim_to_word = list()
                                if (len(meanings) > 0):
                                        for mean in meanings:
                                                if self.model_word_from_word.get(pref_mean):
                                                        sim_to_word.append((mean, abs(self.model.similarity(self.model_word_from_word[mean], self.model_word_from_word[word]))))
                                        if len(sim_to_word) > 0:
                                                max_sim = max(sim_to_word, key = lambda item:item[0])[1]
                                                max_sim_mean = max(sim_to_word, key = lambda item:item[0])[0]
                                                if word == u"поросятина":
                                                        print "Max sim = " + max_sim
                                                        print "Max mean = " + max_sim_mean
                                        pref_meanings.append((max_sim_mean, max_sim))

                        pref_vects = list()
                        pref_mean_sim = 0
                        if len(pref_meanings) > 0:
                                sim_to_word = list()
                                for pref_mean in pref_meanings:
                                        sim, mean = pref_mean
                                        if word == u"поросятина":
                                                print "MEANING_PREF = " + mean
                                        pref_vects.append((self.model[self.model_word_from_word[mean]], sim))

			suff_meanings = list()
                	for inx in range(len(word_morphemes.suffixes)):
				# methon suffixes_prefix_parser.parser.get return list of triples [[meaning1, examples, specs], [], [] ]
				if word == u"поросятина":
                                        print "suff: "
                                        print word_morphemes.suffixes[inx].strip()
				meanings, _, _ = suff_parser.get(word_morphemes.suffixes[inx].strip())
				if word == u"поросятина":
					print ' ,'.join(meanings)
				sim_to_word = list()
				if (len(meanings) > 0):
					for mean in meanings:
						if self.model_word_from_word.get(mean):
                                                	sim_to_word.append((mean, abs(self.model.similarity(self.model_word_from_word[mean], self.model_word_from_word[word]))))
                                	if len(sim_to_word) > 0:
                                        	max_sim = max(sim_to_word, key = lambda item:item[0])[1]
                                        	max_sim_mean = max(sim_to_word, key = lambda item:item[0])[0]
                                        	if word == u"поросятина":
                                                	print "Max sim = " + max_sim
                                                	print "Max mean = " + max_sim_mean
                        		suff_meanings.append((max_sim_mean, max_sim))

                	suff_vects = list()
                        suff_mean_sim = 0
			if len(suff_meanings) > 0:
				sim_to_word = list()
				for suff_mean in suff_meanings:
					sim, mean = suff_mean
					if word == u"поросятина":
                                                print "MEANING_SUFF = " + mean
					if self.model_word_from_word.get(mean)
					suff_vects.append((self.model[self.model_word_from_word[mean]], sim))

			new_model = {}
			new_model[model_word] = old_vec

#			if pref_mean_sim != 0 and suff_mean_sim != 0:
#				new_model[model_word] = 0.5 * np.add(old_vec, 0.5 * np.add(pref_mean_sim * pref_vect, suff_vect_sim * suff_vect))

#			else:
#				if pref_mean_sim != 0 and suff_mean_sim == 0:
#					new_model[model_word] = 0.5 * np.add(old_vec, pref_mean_sim * pref_vect)
#				else:
#					if pref_mean_sim == 0 and suff_mean_sim != 0: 
#						new_model[model_word] = 0.5 * np.add(old_vec, suff_mean_sim * suff_vect)
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
	
