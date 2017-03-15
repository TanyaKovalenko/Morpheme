# coding=utf-8
import codecs
"""
with codecs.open('urls.txt', 'r', encoding='utf-8') as f:
    letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
    for line in f:
        for letter in letters:
            if line.find('http://sostavslova.ru/' + letter.decode('utf-8') + '/') != -1:
                new_line = line.replace('http://sostavslova.ru/' + letter.decode('utf-8') + '/', '')
                with codecs.open('sostavslova_words.txt', 'a', encoding='utf-8') as f1: 
                    f1.write(new_line)
"""
sostavslova_list = list()
with codecs.open('sostavslova_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        sostavslova_list.append(line.lower())

morphemeonline_list = list()
with codecs.open('morphemeonline_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
                morphemeonline_list.append(line.lower())

for inx_1 in range(len(sostavslova_list)):
    flag = False
    for inx_2 in range(len(morphemeonline_list)):
        if sostavslova_list[inx_1] == morphemeonline_list[inx_2]:
            flag = True
    if flag == False:
        with codecs.open('same_words.txt', 'a', encoding='utf-8') as f1: 
            f1.write(sostavslova_list[inx_1])
