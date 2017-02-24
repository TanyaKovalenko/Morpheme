# coding=utf-8
import codecs
file_name = 'dicts//words_like_morhemes.txt'
root_array = []
pref_array = []
suff_array = []

class Word_Morpheme:
    def __init__(self):    
        self.prefixies = []
        self.roots = []
        self.suffixies = []
        self.main_part = []
        self.connecting_vowel = []
        self.ending = []

def parse_file_to_array(file, array):
    with codecs.open(file, "r", encoding='utf-8') as dict_file:    
        for line in dict_file.read().split("\n"):
            if line != "":
                element_line = line.split(":")[0]
                for element_slash in element_line.split('/'):
                    if ('(' in element_slash):
                        start_list = element_slash.find("(")
                        end_list = element_slash.find(")")
                        main_element = element_slash[:start_list].strip().lower()
                        array.append(main_element)
                        for end in element_slash[start_list+1:end_list].split(','):
                            array.append(main_element + end.strip().lower())
                    else:
                        array.append(element_slash.strip().lower())

def form_dict():
    word_morhemes_dict = {}
    
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
    return word_morhemes_dict

def parse_by_morphemes(elem):
    word_morphems = Word_Morpheme()
    word = elem
    start_root_index = -1
    for dict_root in root_array:
        if dict_root in word:
            word_morphems.roots.append(dict_root)
            if len(word_morphems.roots) == 1:
                start_root_index = word.find(dict_root)

            if start_root_index != word.find(dict_root):
                word_morphems.connecting_vowel.append(word[start_root_index:word.find(dict_root)])
                word = word[:start_root_index] + word[word.find(dict_root):]
            word = word.replace(dict_root, "")
        if len(dict_root) < 3:
            break
    for dict_pref in pref_array:
        if dict_pref in word[:start_root_index]:
            word_morphems.prefixies.append(dict_pref)
            #root = dict_root
            word = word.replace(dict_pref, "")
            start_root_index -= len(dict_pref)
            #break

    for dict_suf in suff_array:
        if dict_suf in word:
            word_morphems.suffixies.append(dict_suf)
            if (word.find(dict_suf) > 0):
                word_morphems.suffixies.append(word[:word.find(dict_suf)])
                word = word.replace(word[:word.find(dict_suf)], "")
            word = word.replace(dict_suf, "")
    return word_morphems

def getMorphemes(main_dict, word):
    dict_result = main_dict[word]
    if len(dict_result.roots) == 0:
       dict_result = parse_by_morphemes(word)
    #dict_result = parse_by_morphemes(word)
    return dict_result

if __name__ == "__main__":
    parse_file_to_array("dicts//roots.txt", root_array)    
    parse_file_to_array("dicts//prefixies.txt", pref_array)    
    parse_file_to_array("dicts//suffixies.txt", suff_array)    
    root_array = sorted(root_array, key=len, reverse=True)
    pref_array = sorted(pref_array, key=len, reverse=True)
    suff_array = sorted(suff_array, key=len, reverse=True)
    main_dict = form_dict()
    test_keys = main_dict.keys()
    count = 0
    with codecs.open("problem.txt", 'w+', encoding='utf-8') as problem_words:
        for test_word in test_keys:
            my_result = getMorphemes(main_dict, test_word)
            right_result = main_dict[test_word]
            if ((my_result.prefixies != right_result.prefixies) or (my_result.roots != right_result.roots) or (my_result.suffixies != right_result.suffixies) or (my_result.connecting_vowel != right_result.connecting_vowel)):
                problem_words.write("\n============== WORD: " + test_word + "=============")
                problem_words.write("\nMy prefix: " + ", ".join(my_result.prefixies))
                problem_words.write("\nRight prefix: " + ", ".join(right_result.prefixies))
                problem_words.write("\nMy roots: " + ", ".join(my_result.roots))
                problem_words.write("\nRight roots: " + ", ".join(right_result.roots))
                problem_words.write("\nMy suffixies: " + ", ".join(my_result.suffixies))
                problem_words.write("\nRight suffixies: " + ", ".join(right_result.suffixies))
                count += 1
                #problem_words.write("\nMy connecting_vowel: " + ", ".join(my_result.connecting_vowel))
                #problem_words.write("\nRight connecting_vowel: " + ", ".join(right_result.connecting_vowel)) + '\n'
                #if count > 5:
                #    break
                #break
            print '.',
    print count
    """test = getMorphemes(dict, u'расщеплять')
    print test.roots[0]
    test = getMorphemes(dict, u'абиссинка')
    print test.roots[0]"""
