# coding=utf-8
import codecs

with codecs.open('diff_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        new_line = line.replace(line, 'http://sostavslova.ru/' + line[0].upper() + '/' + line)
        with codecs.open('diff_words_urls.txt', 'a', encoding='utf-8') as f1: 
            f1.write(new_line)

