# coding=utf-8
import codecs
file_name = '../dicts/words_like_morhemes.txt'


def form_morphemes_lists():
	prefixies_list = list()
	roots_list = list()
	suffixies_list = list()
	ending_list = list()
	main_part_list = list()
	connecting_vowel_list = list()
	with codecs.open(file_name, 'r', encoding='utf-8') as f:
        	for line in f:
                	start_inx = line.find(': ') + len(': ')
			line = line[start_inx:len(line)]
			morphemes = line.split(';')
                        for item in morphemes:
                                morpheme = item.split(u'—')[0].strip()
                                if (len(item.split(u'—')) > 1):
                                        morpheme_name = item.split(u'—')[1].strip()
                                        if (morpheme_name == u'корень') or (morpheme_name == u'корни'):
                                                roots = morpheme.split(',')
						roots_list += roots
                                        if (morpheme_name == u'приставка') or (morpheme_name == u'приставки'):
                                                prefixies = morpheme.split(',')
                                        	prefixies_list += prefixies
					if (morpheme_name == u'суффикс') or (morpheme_name == u'суффиксы'):
                                                suffixies = morpheme.split(',')
                                                suffixies_list += suffixies
                                        if (morpheme_name == u'основа слова'):
                                                main_part = morpheme.split(',')
                                                main_part_list += main_part
                                        if (morpheme_name == u'соединительная гласная'):
                                                connecting_vowel = morpheme.split(',')
                                                connecting_vowel_list += connecting_vowel
                                        if (morpheme_name == u'окончание'):
                                                ending = morpheme.split(',')
                                                ending_list += ending
	# Записываем все префиксы, корни, суффиксы и окончания в соответствующие файлы 
	# prefixies
	for inx in range(len(prefixies_list) - 1):
		prefixies_list[inx] = prefixies_list[inx].strip()
		if prefixies_list[inx].find(':') != -1:
			with codecs.open('BAD_prefixies.txt', 'a', encoding='utf-8') as f:
                		f.write(prefixies_list[inx] + '\n')
	with codecs.open('prefixies.txt', 'a', encoding='utf-8') as f:
                f.write('\n'.join(set(prefixies_list)))
	
	# roots
        for inx in range(len(roots_list) - 1):
                roots_list[inx] = roots_list[inx].strip()
		if roots_list[inx].find(':') != -1 or \
                        roots_list[inx].find('{') != -1 or \
                        roots_list[inx].find('}') != -1 or \
                        roots_list[inx].find('(') != -1 or \
                        roots_list[inx].find(')') != -1 or \
                        roots_list[inx].find('[') != -1 or \
                        roots_list[inx].find(']') != -1:
			with codecs.open('BAD_roots.txt', 'a', encoding='utf-8') as f:
                                f.write(roots_list[inx] + '\n')
	with codecs.open('roots.txt', 'a', encoding='utf-8') as f:
        	f.write('\n'.join(set(roots_list)))
	
	#suffixies
	for inx in range(len(suffixies_list) - 1):
                suffixies_list[inx] = suffixies_list[inx].strip()
		if suffixies_list[inx].find(':') != -1 or \
			suffixies_list[inx].find('{') != -1 or \
			suffixies_list[inx].find('}') != -1 or \
			suffixies_list[inx].find('(') != -1 or \
			suffixies_list[inx].find(')') != -1 or \
			suffixies_list[inx].find('[') != -1 or \
			suffixies_list[inx].find(']') != -1: 
                        with codecs.open('BAD_suffixies.txt', 'a', encoding='utf-8') as f:
                                f.write(suffixies_list[inx] + '\n')
        with codecs.open('suffixies.txt', 'a', encoding='utf-8') as f:
                f.write('\n'.join(set(suffixies_list)))
	
	#endings
	for inx in range(len(ending_list) - 1):
                ending_list[inx] = ending_list[inx].strip()
		if ending_list[inx].find(':') != -1 or \
                        ending_list[inx].find('{') != -1 or \
                        ending_list[inx].find('}') != -1 or \
                        ending_list[inx].find('(') != -1 or \
                        ending_list[inx].find(')') != -1 or \
                        ending_list[inx].find('[') != -1 or \
                        ending_list[inx].find(']') != -1:
                        with codecs.open('BAD_ending.txt', 'a', encoding='utf-8') as f:
                                f.write(ending_list[inx] + '\n')
        with codecs.open('ending.txt', 'a', encoding='utf-8') as f:
                f.write('\n'.join(set(ending_list)))

	#main_part
	for inx in range(len(main_part_list) - 1):
                main_part_list[inx] = main_part_list[inx].strip()
		if main_part_list[inx].find(':') != -1 or \
                        main_part_list[inx].find('{') != -1 or \
                        main_part_list[inx].find('}') != -1 or \
                        main_part_list[inx].find('(') != -1 or \
                        main_part_list[inx].find(')') != -1 or \
                        main_part_list[inx].find('[') != -1 or \
                        main_part_list[inx].find(']') != -1:
                        with codecs.open('BAD_main_part.txt', 'a', encoding='utf-8') as f:
                                f.write(main_part_list[inx] + '\n')
        with codecs.open('main_part.txt', 'a', encoding='utf-8') as f:
                f.write('\n'.join(set(main_part_list)))

	#connecting_vowel
	for inx in range(len(connecting_vowel_list) - 1):
                connecting_vowel_list[inx] = connecting_vowel_list[inx].strip()
                if connecting_vowel_list[inx].find(':') != -1 or \
                        connecting_vowel_list[inx].find('{') != -1 or \
                        connecting_vowel_list[inx].find('}') != -1 or \
                        connecting_vowel_list[inx].find('(') != -1 or \
                        connecting_vowel_list[inx].find(')') != -1 or \
                        connecting_vowel_list[inx].find('[') != -1 or \
                        connecting_vowel_list[inx].find(']') != -1:        
			with codecs.open('BAD_connecting_vowel.txt', 'a', encoding='utf-8') as f:
                                f.write(connecting_vowel_list[inx] + '\n')
	with codecs.open('connecting_vowel.txt', 'a', encoding='utf-8') as f:
                f.write('\n'.join(set(connecting_vowel_list)))

if __name__ == "__main__":
	form_morphemes_lists()
