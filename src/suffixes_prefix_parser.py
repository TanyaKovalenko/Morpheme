# coding=utf-8

from collections import defaultdict
import codecs

class SuffixPrefixParser(object):
    """
    Load suffixes/prefixes from file and let to get info for every suffix.
    File should contains lines in following format:
    suffix_1/suffix_2/../suffix_n: meaning1 [example1_1, example1_2, ...]{spec1_1, spec1_2, ..}; meaning2 [..]{..};...
    It allows to group different suffixes with the same meaning into one line.
    """

    _MORPHEMES_ = defaultdict(lambda: ([], [], []))
    _is_load_ = False
    _PATH_TO_MORPHEMES = "prefixes.txt"

    def __init__(self, path_to_file=None):
        if path_to_file:
            self.specify_file(path_to_file)
        # if
    # def

    def __load(self):
        """
        Loads suffixes from files in specific format and push it to _SUFFIXIES_ dict
        in format: key - suffix, value - tuple of three list-values the same size:
        list of meanings,list of examples, list of specs.
        """
        if self._is_load_:
            return
        # if

        with codecs.open(self._PATH_TO_MORPHEMES, "r", encoding='utf-8') as fin:
            line_num = 0

            for line in fin:
                line_num += 1
                line = line.strip()

                # check whether there comments
                pos = line.find("#")
                if pos >= 0:
                    line = line[:pos].strip()
                # if

                if len(line) == 0:
                    continue
                # if

                # check whether there separator between key and values
                pos = line.find(":")
                if pos == -1:
                    raise Exception("Line [%s] is wrong, because there is no ':' symbol-separator" % line_num)
                # if

                # map every key to values
                keys = filter(lambda x: len(x), map(lambda x: x.strip().replace(u'ё', u'е'), line[:pos].split("/")))

                examples = []
                meanings = []
                specs = []

                for value in line[pos + 1:].split(";"):
                    min_pos = len(value)

                    # ----------- #
                    # try to find marker of examples
                    pos = value.find('[')
                    if pos == -1:
                        examples.append([])
                    else:
                        close_pos = value.find(']')
                        if close_pos == -1 or close_pos < pos:
                            print(value)
                            raise Exception("Line [%s] is wrong, because examples are formed wrong" % line_num)
                        # if

                        if min_pos > pos:
                            min_pos = pos
                        # if

                        token = value[pos + 1:close_pos]
                        examples.append(filter(lambda x: len(x) != 0,
                                               map(lambda x: x.strip().replace(u'ё', u'е'), token.split(","))))
                    # if

                    # ----------- #
                    # try to find marker of specification
                    pos = value.find('{')
                    if pos == -1:
                        specs.append({})
                    else:
                        close_pos = value.find('}')
                        if close_pos == -1 or close_pos < pos:
                            raise Exception("Line [%s] is wrong, because specifications are formed wrong" % line_num)
                        # if

                        if min_pos > pos:
                            min_pos = pos
                        # if

                        token = value[pos + 1: close_pos]
                        specs.append(filter(lambda x: len(x) != 0,
                                            map(lambda x: x.strip().replace(u'ё', u'е'), token.split(","))))
                    # if

                    # ----------- #
                    # push meaning
                    meanings.append(value[:min_pos].strip())
                # for

                for key in keys:
                    self._MORPHEMES_[key] = (meanings, examples, specs)
                # for
            # for
        # with

        self._is_load_ = True
    # def

    def get(self, key):
        """
        :param key:
        :return: list, where each element is tuple contains three elements - meaning, list of examples, list of specs
        """
        self.__load()

        return self._MORPHEMES_[key]
    # def

    def len(self):
        return len(self._MORPHEMES_)
    # def

    def keys(self):
        return self._MORPHEMES_.keys()
    # def

    def specify_file(self, path_to_dict):
        self._PATH_TO_MORPHEMES = path_to_dict
        self.__load()
    # def
# class

def open_other_suffixes():
    l = []

    with codecs.open('../dicts/morphemes_lists/suffixes.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            if line.find('(') != -1 or \
                line.find(')') != -1 or \
                line.find('{') != -1 or \
                line.find('}') != -1:
                continue
            # if

            l.append(line.strip())
        # for
    # with

    return l
# def

if __name__ == '__main__':
    #parser.specify_file("../dicts/suffixes.txt")

    parser = SuffixPrefixParser("../dicts/suffixes.txt")
    parser2 = SuffixPrefixParser("../dicts/prefixes.txt")

    meanings, _, _ = parser.get(u'ят')
    meanings2, _, _ = parser2.get(u'пре')

    print(len(meanings), meanings[0])
    print(len(meanings2), meanings2[0])
