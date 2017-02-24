# coding=utf-8

from collections import defaultdict
import codecs

class parser(object):
    """
    Load suffixes/prefixes from file and let to get info for every suffix.
    File should contains lines in following format:
    suffix_1/suffix_2/../suffix_n: meaning1 [example1_1, example1_2, ...]{spec1_1, spec1_2, ..}; meaning2 [..]{..};...
    It allows to group different suffixes with the same meaning into one line.
    """

    _MORPHEMES_ = defaultdict(lambda: list())
    _is_load_ = False
    _PATH_TO_MORPHEMES = "prefixies.txt"

    @classmethod
    def __load(cls):
        """
        Loads suffixes from files in specific format and push it to _SUFFIXIES_ dict
        in format: key - suffix, value - list of tuples, which contains three elements - meaning,
        list of examples, list of specs.
        """
        if cls._is_load_:
            return
        # if

        with codecs.open(cls._PATH_TO_MORPHEMES, "r", encoding='utf-8') as fin:
            line_num = 1

            for line in fin:
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
                            print value
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
                    cls._MORPHEMES_[key].append((meanings, examples, specs))
                # for

                line_num += 1
            # for
        # with

        cls._is_load_ = True
    # def

    @classmethod
    def get(cls, key):
        """
        :param key:
        :return: list, where each element is tuple contains three elements - meaning, list of examples, list of specs
        """
        cls.__load()

        return cls._MORPHEMES_[key]
    # def

    @classmethod
    def specify_file_(cls, path_to_dict):
        cls._PATH_TO_SUFFIXIES = path_to_dict
    # def
# class

if __name__ == '__main__':
    values = parser.get(u'об')
    for m, e, s in values:
        print e[0][0]
    # for
# if