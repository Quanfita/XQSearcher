#-*- coding:utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from crawler.bilibili.bilibili.spiders.videos import VideosSpider
from search import Searcher
import json
import glob
import time
from termcolor import *
from colorama import init
import codecs

class Main(object):

	def __init__(self):
		init()
		self.__searcher = Searcher()
		self.__json_list = []
		self.__self_list = glob.glob('./json/bili_*.json')

	def runCrawler(self):
		# 创建一个CrawlerProcess对象
		process = CrawlerProcess({"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)","ITEM_PIPELINES":{'crawler.bilibili.bilibili.pipelines.BilibiliPipeline': 300}}) # 括号中可以添加参数

		process.crawl(VideosSpider)
		process.start()

	def runSearch(self,content):
		t = time.time()
		res = self.__searcher.searchItems(content)
		ts = time.time()
		#res = self.__searcher.getResList(content)
		'''
		new_res = []
		for id_ in res:
			if id_ not in new_res:
				new_res.append(id_)'''
		self.__sprint(res)
		print(colored('Total Search Results: '+str(len(res)),'grey'), flush=True)
		print(colored('Total Time: '+str(time.time()-t)+'\tSearch Time:'+str(ts-t), 'blue'), flush=True)
		with codecs.open('./res.json', 'wb+', encoding='utf-8') as f:
			f.write('{"results":['+''.join([json.dumps(dict(x), ensure_ascii=False, sort_keys=False)+',' for x in res])[:-1]+']}\n')
		return res

	def __sprint(self,dic):
		print(colored('Search Results:','magenta'))
		for d in dic:
			title = d['title']
			content = d['content']
			target = d['target']
			site = d['site']
			url = d['url']
			msg = title+'-'+target+'-'+site
			print(colored(msg, 'red'), flush=True)
			print(colored(content, 'cyan'), flush=True)
			print(colored(url, 'green'), flush=True)
			print()

	def bulidSearcher(self):
		self.__json_list = []
		for file in glob.glob('./json/bili_*.json'):
			with open(file,'r',encoding='utf-8') as f:
				s = json.load(f)
				if s['content'] == '':
					continue
				self.__json_list.append(s)
		self.__searcher.buildIndex(self.__json_list)

	def updateSearcher(self):
		self.__json_list = []
		for file in [x for x in glob.glob('./json/bili_*.json') if x not in self.__self_list]:
			with open(file,'r',encoding='utf-8') as f:
				s = json.load(f)
				if s['content'] == '':
					continue
				self.__json_list.append(s)
		self.__searcher.updateIndex(self.__json_list)

	def startSearcher(self):
		self.__searcher.searchSetting()

if __name__ == "__main__":
	main = Main()
	main.startSearcher()
	#main.runCrawler()
	#main.bulidSearcher()
	#main.updateSearcher()
	s = input("Search:")
	main.runSearch(s)
	'''
	while True:
		s = input("Search:")
		main.runSearch(s)
'''
	'''
	#runCrawler()
	l = []
	for file in glob.glob('./json/bili_*.json'):
		with open(file,'r',encoding='utf-8') as f:
			s = json.load(f)
			if s['content'] == '':
				continue
			l.append(s)
	searcher = Searcher()
	searcher.buildCommit(l)
	t = time.time()
	res = searcher.getResList('魔法禁书目录')
	new_res = []
	for id_ in res:
		if id_ not in new_res:
			new_res.append(id_)
	print(new_res)
	print(time.time() - t)
	with codecs.open('./res.json', 'wb+', encoding='utf-8') as f:
		f.write('{"results":['+''.join([json.dumps(x, ensure_ascii=False, sort_keys=False)+',' for x in new_res])[:-1]+']}\n')'''