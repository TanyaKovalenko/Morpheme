# coding=utf-8
import scrapy
import csv
import codecs

class MorphySpider(scrapy.Spider):
        name = "morphy_spider"
	
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
                		with codecs.open('roots.txt', 'a', encoding='utf-8') as f:
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

	# Скачивалка url-ов со словами  для каждой буквы алфавита
	
        def start_requests(self):
                urls = set()
                letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
		for letter in letters:
			# по url - у на каждую букву алфавита
                        urls.add('http://morphemeonline.ru/' + letter)

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
                                        f.write(response.url + '/' + the_word + '\n')
                else:
			# В этой ветке можно оказаться только если на какой-то странице нет ни одного слова 
                        print ':-('
                        return
	
	# Скачивалка разборов слов по url-ам, полученных выше
	
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
		word = response.xpath('//div[contains(@class,"col-md-9")]').extract()[0]
		start_word = word.find('<h1>«'.decode('utf-8')) + len('<h1>«'.decode('utf-8'))
                end_word = word.find('»'.decode('utf-8'), start_word)
		word = word[start_word:end_word]
			
		with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
			f.write(word + ': ')

		# вычленяем морфемы слова  
		morphemes = [sel.extract() for sel in response.xpath('//div[contains(@class,"morpheme")]/span/span')]

                if len(morphemes) != 0:
                        for morpheme in morphemes:
				start_morpheme_name = morpheme.find('title="') + len('title="')
				end_morpheme_name = morpheme.find('"', start_morpheme_name)
				start_morpheme = morpheme.find('>', end_morpheme_name) + len('>')
                                end_morpheme = morpheme.find('<', start_morpheme)
                                with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
					name = morpheme[start_morpheme_name:end_morpheme_name].strip()
					mean = morpheme[start_morpheme:end_morpheme].strip()
					f.write(name + '-' + mean + ';')
			
			base_plus_ending = [sel.extract() for sel in response.xpath('//div[contains(@class,"morpheme")]/span')]
			for ending in base_plus_ending:
				if ending.find('"ending"') != -1:
					start_ending_name = ending.find('ending" title="') + len('ending" title="')
                        		end_ending_name = ending.find('"', start_ending_name)
                        		start_ending = ending.find('>', end_ending_name) + len('>')
                        		end_ending = ending.find('<', start_ending)
                        		with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
                        			name = ending[start_ending_name:end_ending_name].strip()
                                		mean = ending[start_ending:end_ending].strip()
						f.write(name + '-' + mean + ';')
			with codecs.open('words_like_morhemes.txt', 'a', encoding='utf-8') as f:
				f.write('\n')
                else:
                	print ':-('
                        return

