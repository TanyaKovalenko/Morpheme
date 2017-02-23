# coding=utf-8
import scrapy
import csv
import codecs

urls_file_name = 'words.txt'
morphemes_file_name = 'words_like_morhemes.txt'

class MorphySpider(scrapy.Spider):
	name = "morpheme_spider"

	# Скачивалка разборов слов по url-ам из файла urls_file_name
	# Результаты будут записаны в файл morphemes_file_name

	def start_requests(self):
        	urls = set()
                with open(urls_file_name, 'r') as f_urls:
                        for line in f_urls:
                                url = line.strip()
                        	urls.add(url)

                for url in urls:
                        yield scrapy.Request(url=url, callback=self.parse)

        def parse(self, response):
                # вычленяем само слово из текста на страничке
                word = response.xpath('//div[contains(@class,"col-md-9")]').extract()[0]
                start_word = word.find('<h1>«'.decode('utf-8')) + len('<h1>«'.decode('utf-8'))
                end_word = word.find('»'.decode('utf-8'), start_word)
                word = word[start_word:end_word]
                        
                with codecs.open(morphemes_file_name, 'a', encoding='utf-8') as f:
                        f.write(word + ': ')

                # вычленяем морфемы слова  
                morphemes = [sel.extract() for sel in response.xpath('//div[contains(@class,"col-md-9")]/p')]

                if len(morphemes) != 0:
			morpheme = morphemes[0]
                	start_morpheme = morpheme.find('<span')
                        end_morpheme= len(morpheme) - 4
			morpheme = morpheme[start_morpheme:end_morpheme]
			morpheme = morpheme.replace('<span class="marker">', '')
			morpheme = morpheme.replace('</span>', '')
			morpheme = morpheme.replace('<br>', ';')
			morpheme = morpheme.replace('"', '')
                	morpheme = morpheme.replace(', ;', ';')
			morpheme = morpheme.replace('.;', ';')
			morpheme = morpheme.replace('&amp;plus;', '+')
		        with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
                        	f.write(morpheme + '\n')
                        
                else:
                        print ':-('
                        return
