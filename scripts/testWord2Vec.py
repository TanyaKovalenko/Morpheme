# coding=utf-8
import os
import codecs
import gensim
import logging
import re
import numpy as np
from utils import load_word2vec_format

# ------------ web --------------------
#model_size = 353608
#model_file_name = 'web.model.bin'

# ------------ news ------------------
#model_size = 124590
#model_file_name = 'news.model.bin'

# ---------- ruscorpora -------------
#model_size = 184973
#model_file_name = 'ruscorpora.model.bin'

# ---------- ruwikiruscorpora -------------
model_size = 392339
model_file_name = 'ruwikiruscorpora.model.bin'

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
russianDictDir = '/Users/ruslan/Tanya/ArticleMorphems/dicts'
russian_dict_set = set()
for fname in os.listdir(russianDictDir):
        for line in codecs.open(os.path.join(russianDictDir, fname), 'r', encoding='utf-8'):
                if '"' in line:
			word=line.split('"')[1]
			if len(word) > 2: 
                		russian_dict_set.add(word.lower())
# --------------------------------------------------------- Form dict of russian words ( end ) ---------------------------------------------------------------------------
#
#
#
#
# --------------------------------------------------------- Get model ( start ) --------------------------------------------------------------------------------------------
model = gensim.models.Word2Vec.load_word2vec_format(model_file_name, binary=True)  # C binary format
print model

dict_word_from_model = {}
dict_model_from_word = {}
for i in range(model_size):
	dict_word_from_model[model.index2word[i]] = model.index2word[i].split('_')[0]
	dict_model_from_word[model.index2word[i].split('_')[0]] = model.index2word[i]
# --------------------------------------------------------- Get model ( end ) --------------------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------Get the html with usal morphems -----------------------------------------------------------------------------------
#import requests
#response = requests.get('https://grammatika-rus.ru/znachenie-latinskih-morfem/')
#response = requests.get('http://spelling.siteedit.ru/page51/')
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(response.text, 'html.parser')

#morphy_file = codecs.open('usual_morphies.txt', 'w+', encoding='utf-8')

#for morphy_inx in range(2, len(soup('strong')) - 5):
#	print soup('tr')[morphy_inx]('td')[0]
#	morphy =  soup('tr')[morphy_inx]('td')[0]('strong').string.lower()
#	meaning =  soup('tr')[morphy_inx]('td')[1]('strong').string.lower()
#	morphy_file.write(morphy + ":" + meaning + "\n")

#morphy_file.close()	
#------------------------------------------------------Get the html with usal morphems ( end )-----------------------------------------------------------------------------------
#
#
#
#
# -----------------------------------------------------------------Create a dict of morphems (start) ------------------------------------------------------------------------
morpy_dict = {}

morphy_file = codecs.open('morphies_latin.txt', 'r', encoding='utf-8')
for line in morphy_file:
	morphy = line.split(":")[0]
	meaning = line.split(":")[1]
	meaning = re.sub("^\s+|\n|\r|\s+$", '', meaning)
	morpy_dict[morphy] = meaning

morphy_file.close()
# -----------------------------------------------------------------Create a dict of morphems (end) ------------------------------------------------------------------------
#
#
#
#
#
#------------------------------------------------------- Form new model ---------------------------------------------------------------------------------------------------
word_like_morphies_dict = {}
new_model = {}
count = 0
for i in range(model_size):
	model_word = model.index2word[i]
	old_vec = model[model_word]
	new_model[model_word] = old_vec 
	word = dict_word_from_model[model_word]
	word_like_morphies_dict[word] = word
        for inx in range(1, len(word)):
		if (morpy_dict.get(word[0:inx])) and (word[inx:len(word)] in russian_dict_set):
			morphy_list = [word[0:inx], word[inx:len(word)]]
                	word_like_morphies_dict[word] = morphy_list
	if (word_like_morphies_dict[word] != word):
		morphy_meaning = morpy_dict[word_like_morphies_dict[word][0]].split(',')[0]
		print "Word = " + word
		print morphy_meaning
                print word_like_morphies_dict[word][1]
		if (dict_model_from_word.get(morphy_meaning) and dict_model_from_word.get(word_like_morphies_dict[word][1])):
			count += 1
			morphy_vec = model[dict_model_from_word[morphy_meaning]]
        		word_vec = model[dict_model_from_word[word_like_morphies_dict[word][1]]]
			new_model[model_word] = old_vec + 0.5 * (morphy_vec + word_vec)

print "Count of word like morphy-list = " + str(count)
#------------------------------------------------------ Form new model -----------------------------------------------------------------------------------
