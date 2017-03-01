# coding=utf-8
import codecs
from morphemes import WordMorphemes, WordMorphemeDicts

file_name = 'dicts//words_like_morhemes.txt'
root_array = []
pref_array = []
suff_array = []

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

def parse_by_morphemes(elem):
    word_morphems = WordMorphemes()
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
            word_morphems.prefixes.append(dict_pref)
            #root = dict_root
            word = word.replace(dict_pref, "")
            start_root_index -= len(dict_pref)
            #break

    for dict_suf in suff_array:
        if dict_suf in word:
            word_morphems.suffixes.append(dict_suf)
            if (word.find(dict_suf) > 0):
                word_morphems.suffixes.append(word[:word.find(dict_suf)])
                word = word.replace(word[:word.find(dict_suf)], "")
            word = word.replace(dict_suf, "")
    return word_morphems

def getMorphemes(word):
    if WordMorphemeDicts.contains(word):
        return WordMorphemeDicts.get(word)
    # if

    return parse_by_morphemes(word)
# def

if __name__ == "__main__":

    result = getMorphemes(u'поросятина')
    print len(result.roots)
    print result.roots[0]
    """
    parse_file_to_array("dicts//roots.txt", root_array)    
    parse_file_to_array("dicts//prefixes.txt", pref_array)    
    parse_file_to_array("dicts//suffixes.txt", suff_array)    
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
            if ((my_result.prefixes != right_result.prefixes) or (my_result.roots != right_result.roots) or (my_result.suffixes != right_result.suffixes) or (my_result.connecting_vowel != right_result.connecting_vowel)):
                problem_words.write("\n============== WORD: " + test_word + "=============")
                problem_words.write("\nMy prefix: " + ", ".join(my_result.prefixes))
                problem_words.write("\nRight prefix: " + ", ".join(right_result.prefixes))
                problem_words.write("\nMy roots: " + ", ".join(my_result.roots))
                problem_words.write("\nRight roots: " + ", ".join(right_result.roots))
                problem_words.write("\nMy suffixes: " + ", ".join(my_result.suffixes))
                problem_words.write("\nRight suffixes: " + ", ".join(right_result.suffixes))
                count += 1
                #problem_words.write("\nMy connecting_vowel: " + ", ".join(my_result.connecting_vowel))
                #problem_words.write("\nRight connecting_vowel: " + ", ".join(right_result.connecting_vowel)) + '\n'
                #if count > 5:
                #    break
                #break
            print '.',
    print count
    test = getMorphemes(dict, u'расщеплять')
    print test.roots[0]
    test = getMorphemes(dict, u'абиссинка')
    print test.roots[0]"""
