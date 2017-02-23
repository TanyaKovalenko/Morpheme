# coding=utf-8
import scrapy
import csv
import codecs

class MorphySpider(scrapy.Spider):
        name = "urls_spider"

	def start_requests(self):
                urls = set()
                letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
		for letter in letters:
			# url - ы на каждую букву алфавита
			for inx in range(150):
                        	urls.add('http://morphemeonline.ru/' + letter + '?page=' + str(inx))

                for url in urls:
                        yield scrapy.Request(url=url, callback=self.parse)

        def parse(self, response):

                words = [sel.extract() for sel in response.xpath('//ul[contains(@class,"list-unstyled")]/li')]
		
                if len(words) != 0:
			# Так как для того, чтобы просмотреть разбор слов на какую-то букву алфавита, надо далее перейти по ссылке на это слово, то сначала сохраним в файлик все url - ы всех слов 
                        for word in words:
                                with codecs.open('words.txt', 'a', encoding='utf-8') as f:
                                        start_word = word.find('">') + len('">')
                                        end_word = word.find('<', start_word)
                                        the_word = word[start_word:end_word].strip()
                                        letter = the_word[0].upper()
					f.write('http://morphemeonline.ru/' + letter + '/' + the_word + '\n')
                else:
			# В этой ветке можно оказаться только если на какой-то странице нет ни одного слова 
                        print ':-('
                        return
