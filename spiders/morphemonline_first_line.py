# coding=utf-8
import scrapy
import csv
import codecs

class MorphySpider(scrapy.Spider):
    name = "morphy_spider"

    def start_requests(self):
        urls = set()
        with open('words.txt', 'r') as f_urls:
            for line in f_urls:
                url = line.strip()
                urls.add(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # вычленяем само слов из текста на страничке
        div = response.xpath('//div[contains(@class,"col-md-9")]').extract()[0]

        start_word = div.find('<h1>«'.decode('utf-8')) + len('<h1>«'.decode('utf-8'))
        end_word = div.find('»'.decode('utf-8'), start_word)
        word = div[start_word:end_word]

        pos = div.find('class="morpheme"')
        end_pos = div.find('</div>', pos)
        end2_pos = div.find(u'программа института', pos)
        if end2_pos != -1 and end2_pos < end_pos:
            end_pos = end2_pos
        # if

        morph_names = [u'корень', u'окончание', u'приставка',
                   u'суффикс', u'нулевой суффикс', u'соединительная гласная',
                   u'формообразующий суффикс']

        with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
            f.write(word + ': ')

            while True:
                min_pos = pos * pos
                min_name = None

                for name in morph_names:
                    t_pos = div.find(name, pos)

                    if t_pos != -1 and t_pos < min_pos:
                        min_name = name
                        min_pos = t_pos
                    # if
                # for

                if min_name is None or min_pos > end_pos:
                    break
                # if

                pos = div.find('<', min_pos)
                morph_base = div[min_pos + len(min_name) + 2: pos]
                f.write(min_name + "-" + morph_base + ";")
            # while

            f.write("\n")
        # with
    # def
# clsss