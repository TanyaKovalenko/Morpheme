# coding=utf-8
import codecs
file_name = 'words_like_morhemes.txt'

class Word_Morpheme:
	prefixies = list()
    	roots = list()
    	suffixies = list()
	main_part = list()
	connecting_vowel = list()
     	ending = list()

word_morhemes_dict = {}

def form_dict():
	with codecs.open(file_name, 'r', encoding='utf-8') as f:
		for line in f:
			word_morphems = Word_Morpheme()
			word = line.split(':')[0]	
			start_inx = line.find(': ') + len(': ')
			line = line[start_inx:len(line)]
			morphemes = line.split(';')
			for item in morphemes:
				morpheme = item.split(u'—')[0].strip()
				if (len(item.split(u'—')) > 1):
					morpheme_name = item.split(u'—')[1].strip()
					if (morpheme_name == u'корень') or (morpheme_name == u'корни'):
						roots = morpheme.split(',')
						word_morphems.roots = roots
					if (morpheme_name == u'приставка') or (morpheme_name == u'приставки'):
                                        	prefixies = morpheme.split(',')
						word_morphems.prefixies = prefixies
					if (morpheme_name == u'суффикс') or (morpheme_name == u'суффиксы'):
                                        	suffixies = morpheme.split(',')
                                        	word_morphems.suffixies = suffixies
					if (morpheme_name == u'основа слова'):
                                        	main_part = morpheme.split(',')
                                        	word_morphems.main_part = main_part
					if (morpheme_name == u'соединительная гласная'):
                                        	connecting_vowel = morpheme.split(',')
                                        	word_morphems.connecting_vowel = connecting_vowel
					if (morpheme_name == u'окончание'):
						ending = morpheme.split(',')
                                        	word_morphems.ending = ending
			word_morhemes_dict[word] = word_morphems

def getMorphemes(word):
	form_dict()
	return word_morhemes_dict[word]

if __name__ == "__main__":
	print getMorphemes(u'абиссинка').roots[0]
