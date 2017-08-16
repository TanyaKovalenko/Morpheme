# coding=utf-8
import gensim
import os
from collections import defaultdict

def load_model(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path_to_model = os.path.join(*[dir_path, '..', '..', file_name])
    model = gensim.models.Word2Vec.load_word2vec_format(path_to_model, binary=True)
    return model

if __name__ == "__main__":
    # ---------- ruwikiruscorpora -------------
    ruwiki_model_size = 392339
    ruwiki_model_file_name = 'ruwikiruscorpora.model.bin'
    model = load_model(ruwiki_model_file_name)

    word_from_model_word = defaultdict(lambda: list())
    model_word_from_word = defaultdict(lambda: list())

    for inx in range(len(model.vocab)):
        word_from_model_word[model.index2word[inx]] = model.index2word[inx].split('_')[0]
        model_word_from_word[model.index2word[inx].split('_')[0]] = model.index2word[inx]
    
    print model.wv.similarity(model_word_from_word[u"ученый"], model_word_from_word[u"наука"])
    print model.wv.similarity(model_word_from_word[u"пододеяльник"], model_word_from_word[u"простыня"])
    print model.wv.similarity(model_word_from_word[u"ручка"], model_word_from_word[u"карандаш"])
    print model.wv.similarity(model_word_from_word[u"огурец"], model_word_from_word[u"помидор"])
