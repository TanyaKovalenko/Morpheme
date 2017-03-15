# coding=utf-8
import scrapy
import csv
import codecs

roots_file_name = 'roots.txt'

class MorphySpider(scrapy.Spider):
        name = "roots_spider"
	
	#скачивалка корней
	
	def start_requests(self):
        	urls = set()	
		letters = ['a', 'b', 'v', 'g', 'd', 'je', 'zh', 'z', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'x', 'c', 'ch', 'sh', 'sc', 'ju', 'ja']
        	for letter in letters:
			# по url - у на каждую букву алфавита
			urls.add('http://www.slovorod.ru/slavic-roots/osl-' + letter + '.html')
        	
		for url in urls:
            		yield scrapy.Request(url=url, callback=self.parse)

    	def parse(self, response):

		roots = [sel.extract() for sel in response.xpath('//ol[contains(@class,"vocabulary")]/li')]           
	
                if len(roots) != 0:
			# Для каждого корня записываем в файл сам корень и его значения ( убираем при этом все лишние символы в каждой строке)
			for root in roots:
                		with codecs.open(roots_file_name, 'a', encoding='utf-8') as f:
					start_root = root.find('<b>') + len('<b>')
                        		end_root = root.find('</b>', start_root)
                        		the_root = root[start_root:end_root].strip()
					start_meaning = root.find('<i>') + len('<i>') 
                                        end_meaning = root.find('</i>', start_meaning)
                                        the_meaning = root[start_meaning:end_meaning].strip()
                			if the_root.find('-', 0, len(the_root)) != -1 and \
						the_root.find('>', 0, len(the_root)) == -1 and \
						the_root.find('<', 0, len(the_root)) == -1 and \
						the_meaning.find('<', 0, len(the_root)) == -1 and \
						the_meaning.find('>', 0, len(the_root)) == -1:	
		        			
						the_root = the_root.replace('-', '')
						the_root = the_root.replace('?', '')
						the_root = the_root.replace('//', '/')
						the_root = the_root.replace('"', '')

						the_meaning = the_meaning.replace('-', '')
                                                the_meaning = the_meaning.replace('?', '')
                                                the_meaning = the_meaning.replace('//', '/')
						the_meaning = the_meaning.replace('"', '')
						the_meaning = the_meaning.replace('//', '/')

						f.write(the_root + ': ' + the_meaning + '\n')
                else: 
			# В этой ветке можно оказаться только если на какой-то странице нет ни одного слова ( корня )
			print ':-('
                        return

