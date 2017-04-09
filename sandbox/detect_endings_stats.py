# coding=utf-8
from scripts.morphemes import WordMorphemeDicts
from collections import defaultdict
import codecs
import time
from multiprocessing import Pool

def get(word, pos):
    if pos < 0:
        pos += len(word)
    # if

    if pos >= len(word) or pos < 0:
        return None
    # if

    return word[pos]
# def


def get_morph(x, w, fs, d, filter_key):
    it = iter(WordMorphemeDicts.get(w).all_in_order)
    l = len(x)
    tag, morph = it.next()
    morph_len = len(morph)

    w = w.replace(u'-', '')

    try:
        for inx in range(len(w) - l + 1):
            sub = w[inx: inx + l]

            if morph_len == 0:
                tag, morph = it.next()
                morph_len = len(morph)
            # if

            if sub == x:
                # Match, then build key from features
                key = tuple(map(lambda f: f(l, w, inx), fs))

                if key == filter_key:
                    if sub == morph:
                        d[key][tag] += 1
                    # if

                    d[key]['ALL'] += 1
                # if
            # if

            morph_len -= 1
        # for
    except Exception as e:
        print w
    # try
# def

def get_morph_by_pos(x, w, fs, d, filter_key, pos):
    tag_for_letter = WordMorphemeDicts.get(w).tag_for_letter
    all_in_order = WordMorphemeDicts.get(w).all_in_order
    pos = len(w) + pos

    sub = w[pos: pos + len(x)]

    l = len(x)
    tags = set(tag_for_letter[pos: pos + len(x)])

    if x == sub:
        key = tuple(map(lambda f: f(l, w, pos), fs))

        if key == filter_key:
            tag = next(iter(tags))
            if len(tags) == 1 and (tag, sub) in all_in_order:
                d[key][tag] += 1
            # if

            d[key]["ALL"] += 1
        # if
    # if
# def

D = defaultdict(lambda: defaultdict(lambda: 0))
matches = 0

def parse_word(word, start_from):
    global D
    global matches

    features_f = [ lambda _, w, pos: len(w) - pos
                   #, lambda _, w, pos: get(w, pos - 3)
                   #, lambda _, w, pos: get(w, pos - 2)
                   #, lambda _, w, pos: get(w, pos - 1)
                   , lambda l, w, pos: w[pos: pos + l]
                   , lambda l, w, pos: get(w, pos + l) ]
                   # , lambda l, w, pos: get(w, pos + l + 1)]

    small_feature = False
    if start_from > 4:
        features_f = features_f[1:]
        small_feature = True
    # if

    result = []
    for inx in range(1, len(word) - start_from + 1):
        # get statistic for concrete substring
        #D = defaultdict(lambda: defaultdict(lambda: 0))

        if start_from != 0:
            sub = word[-(inx + start_from):-start_from]
        else:
            sub = word[-(inx + start_from):]
        # if
        sub_key = tuple(map(lambda f: f(len(sub), word, len(word) - (inx + start_from)), features_f))

        if sub_key not in D:
            for w in WordMorphemeDicts.words():
                if small_feature:
                    get_morph(sub, w, features_f, D, sub_key)
                else:
                    get_morph_by_pos(sub, w, features_f, D, sub_key, -(inx + start_from))
            # for
        else:
            matches += 1
        # if

        # apply statistic to determine max probability
        max_prob, max_key = 0.0, None

        for key, value in D[sub_key].iteritems():
            if key == 'ALL':

                continue
            # if

            p = (value + 0.0) / D[sub_key]['ALL']

            if p > max_prob:
                max_prob, max_key = p, key
            # if
        # for

        result.append([max_prob, max_key, sub])
    # for

    return result
# def

def find_max(A, inx, length):
    max_p, max_key, max_sub = -0.1, [], []

    for value in A[inx]:
        p, key, sub = value

        if len(sub) > length:
            break
        # if

        if key is None:
            continue
        # if

        if length - len(sub) > 0:
            rec_p, rec_key, rec_sub = find_max(A, inx + len(sub), length - len(sub))

            if rec_p < 0:
                continue
            # if

            if p * rec_p > max_p:
                max_p, max_key, max_sub = p * rec_p, [key] + rec_key, [sub] + rec_sub
            # if
        else:
            if p > max_p:
                max_p, max_key, max_sub = p, [key], [sub]
            # if
        # if
    # for

    return max_p, max_key, max_sub
# def

def parse(word):
    start = 0
    result = []

    while True:
        result.append(parse_word(word, start))
        
        start += 1

        if start == len(word):
            break
        # if
    # while

    p, key, sub = find_max(result, 0, len(word))
    return p, key, sub
# def


p, k, s = parse(u'образовав')
print k
print s
raise

#orig_word = u'заделать'
#orig_word = u'бледно-голубой'
#orig_word = u'стеснительно' #!!!
#orig_word = u'тамга'

#orig_word = u'заречься'
#orig_word = u'истребитель'
orig_word = u'поросенок'
#orig_word = u'сопеть'
#start = 0

with open('result.csv', 'w') as fout:
    for w in WordMorphemeDicts.words():
        print w
        start_time = time.time()
        p, res_key, res_sub = parse(w)
        #print key, '|'.join(sub)
        
        orig_split = ''
        for t, sub in WordMorphemeDicts.get(w).all_in_order:
            orig_split += sub + '(' + t + ') '
        # for
        print orig_split

        result_split = ''
        for t, sub in zip(res_key, res_sub):
            result_split + sub + '(' + t + ') '
        # for

        dif_time = time.time() - start_time
        print "------------", dif_time, matches

        fout.write(str(dif_time) + ',' + str(matches) + '\n') 
        matches = 0
    # for
# with


#result = []

#while True:
#    result.append(parse_word(orig_word, start))

#   start += 1

#    if start == len(orig_word):
#        break
#    # if
# while

#for w in WordMorphemeDicts.words():
#    p, key, sub = find_max(result, 0, len(orig_word))
# for

#for k, s in zip(key, sub):
#    print k, s
# for

# стеснительно
# обворожительно
# предположительно

# несостоятельно
