# coding=utf-8
import os
import codecs
from morphemes import WordMorphemes, WordMorphemeDicts
from utils.common import norm

root_array = []
pref_array = []
suff_array = []


def __parse_file_to_array(file_name):
    array = []
    count = 0

    with codecs.open(file_name, "r", encoding='utf-8') as fin:
        for line in fin:
            count += 1
            line = line.strip()

            if len(line) == 0:
                continue
            # if

            element_line = line.split(":")[0]
            for element_slash in element_line.split('/'):
                if '(' in element_slash:
                    start_list = element_slash.find("(")
                    end_list = element_slash.find(")")
                    main_element = norm(element_slash[:start_list])
                    array.append(main_element)

                    for end in element_slash[start_list+1:end_list].split(','):
                        array.append(main_element + norm(end))
                    # for
                else:
                    array += map(norm, element_slash.split(','))
                # if
            # for
        # for
    # with

    return sorted(array, key=len, reverse=True)
# def


def __load_standalone_morphemes():
    global suff_array, root_array, pref_array
    dir_name = os.path.dirname(os.path.realpath('__file__'))
    root_file = os.path.join(*[dir_name, 'dicts', 'morphemes_lists', 'roots.txt'])
    pref_file = os.path.join(*[dir_name, 'dicts', 'morphemes_lists', 'prefixes.txt'])
    suff_file = os.path.join(*[dir_name, 'dicts', 'morphemes_lists', 'suffixes.txt'])

    if len(root_array) == 0:
        root_array = __parse_file_to_array(root_file)
    # if

    if len(pref_array) == 0:
        pref_array = __parse_file_to_array(pref_file)
    # if

    if len(suff_array) == 0:
        suff_array = __parse_file_to_array(suff_file)
    # if
# if


def parse_by_morphemes(word):
    __load_standalone_morphemes()

    word = norm(word)
    word_morphems = WordMorphemes()
    start_root_index = -1

    for root in root_array:
        # only 0.12% of words have more than one root with
        # length < 7
        if len(word_morphems.roots) == 1:
            if len(word) <= 6:
                break
            # if
        else:
            if len(root) <= 4:
                break
            # if
        # if

        if root not in word:
            continue
        # if

        word_morphems.roots.append(root)
        if len(word_morphems.roots) == 1:
            start_root_index = word.find(root)
        # if

        if start_root_index != word.find(root):
            con_vowel = word[start_root_index:word.find(root)]

            if len(con_vowel):
                word_morphems.connecting_vowel.append(con_vowel)
                word = word[:start_root_index] + word[word.find(root):]
            # if
        # if

        word = word.replace(root, "|")
    # for

    for pref in pref_array:
        pos = word.find('|')

        if pref not in word[:pos]:
            continue
        # if

        word_morphems.prefixes.append(pref)
        word = word[:pos].replace(pref, "") + word[pos:]
    # for

    for suf in suff_array:
        pos = word.rfind('|')

        if suf not in word[pos:]:
            continue
        # if

        word_morphems.suffixes.append(suf)
        word = word[:pos] + word[pos:].replace(suf, "")
    # for

    return word_morphems
# def


def getMorphemes(word):
    """
    Check whether word in dictionary and if not then try to parse it
    """
    if WordMorphemeDicts.contains(word):
        return WordMorphemeDicts.get(word)
    # if

    return parse_by_morphemes(word)
# def

if __name__ == "__main__":

    all_count = 0
    test_count = 0
    false_negative = 0
    root_count = 0
    pref_count = 0
    suf_count = 0
    for word in WordMorphemeDicts.words():
        m_orig = WordMorphemeDicts.get(word)
        m_test = getMorphemes(word)
        all_count += 3

        count = 0
        n_count = 0
        for r in m_test.roots:
            if r in m_orig.roots:
                count += 1
            else:
                n_count += 1
            # if
        # for
        if len(m_orig.roots):
            test_count += (count + 0.0) / len(m_orig.roots)
            root_count += (count + 0.0) / len(m_orig.roots)

        if len(m_test.roots):
            false_negative += (n_count + 0.0) / len(m_test.roots)

        count = 0
        n_count = 0
        for r in m_test.suffixes:
            if r in m_orig.suffixes:
                count += 1
            else:
                n_count += 1
            # if
        # for
        if len(m_orig.suffixes):
            test_count += (count + 0.0) / len(m_orig.suffixes)
            suf_count += (count + 0.0) / len(m_orig.suffixes)
        else:
            test_count += 1
            suf_count += 1
        # if

        if len(m_test.suffixes):
            false_negative += (n_count + 0.0) / len(m_test.suffixes)

        count = 0
        n_count = 0
        for r in m_test.prefixes:
            if r in m_orig.prefixes:
                count += 1
            else:
                n_count += 1
            # if
        # for

        if len(m_orig.prefixes):
            test_count += (count + 0.0) / len(m_orig.prefixes)
            pref_count += (count + 0.0) / len(m_orig.prefixes)
        else:
            test_count += 1
            pref_count += 1
        # if

        if len(m_test.prefixes):
            false_negative += (n_count + 0.0) / len(m_test.prefixes)

        if all_count % 5000 == 0:
            print ((test_count + 0.0) / all_count) * 100, ((false_negative + 0.0) / all_count) * 100
        # if
    # for

    all_count /= 3
    print 'Roots :', (root_count / all_count) * 100
    print 'Pref :', (pref_count / all_count) * 100
    print 'Suf :', (suf_count / all_count) * 100
    """
    m = getMorphemes(u'предчувствие')

    print "ROOTS ------------- "
    for root in m.roots:
        print root
    # for

    print "PREFIXES ------------- "
    for pref in m.prefixes:
        print pref
    # for

    print "SUFFIXES ------------- "
    for suf in m.suffixes:
        print suf
    # for

    #result = getMorphemes(u'поросятина')
    #print len(result.roots)
    #print result.roots[0]

    __load_standalone_morphemes()
    """

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
