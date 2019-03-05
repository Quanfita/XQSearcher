# -*- coding: utf-8 -*-
from whoosh.qparser import QueryParser  
from whoosh.index import create_in  
from whoosh.index import open_dir  
from whoosh.fields import *  
from jieba.analyse import ChineseAnalyzer   
from whoosh.sorting import FieldFacet
from whoosh.scoring import TF_IDF
import time

class Searcher(object):

	def __init__(self):
		self.__analyser = ChineseAnalyzer()    #导入中文分词工具  
		self.__schema = Schema(title=TEXT(stored=True,analyzer=analysis.StandardAnalyzer()), 
							target=TEXT(stored=True,analyzer=analysis.StandardAnalyzer()),
							site=TEXT(stored=True,analyzer=analysis.StandardAnalyzer()),
							content=TEXT(stored=True,analyzer=analysis.StandardAnalyzer()),  
		                    url=TEXT(stored=True),uid=ID(stored=True))# 创建索引结构 
		self.__schema_zh = Schema(title=TEXT(stored=True, analyzer=self.__analyser), 
							target=TEXT(stored=True, analyzer=self.__analyser),
							site=TEXT(stored=True, analyzer=self.__analyser),
							content=TEXT(stored=True, analyzer=self.__analyser),  
		                    url=TEXT(stored=True),uid=ID(stored=True))# 创建索引结构

	def __createIndex(self):
		self.__ix_zh = create_in("path_zh", schema=self.__schema_zh, indexname='indexname_zh') #path 为索引创建的地址，indexname为索引名称  
		self.__writer_zh = self.__ix_zh.writer()
		self.__ix = create_in("path", schema=self.__schema, indexname='indexname') #path 为索引创建的地址，indexname为索引名称  
		self.__writer = self.__ix.writer()

	def __addItem_zh(self,title,target,site,content,url,uid):
		self.__writer_zh.add_document(title=title,target=target,site=site,content=content,url=url,uid=uid) #  此处为添加的内容
		#print("Add Item to ZH: " + title + '-' + target + '-' + site)

	def __addItem(self,title,target,site,content,url,uid):
		self.__writer.add_document(title=title,target=target,site=site,content=content,url=url,uid=uid) #  此处为添加的内容
		#print("Add Item: " + title + '-' + target + '-' + site)
	
	def searchSetting(self):
		index_zh = open_dir("path_zh", indexname='indexname_zh')
		index = open_dir("path", indexname='indexname')
		self.__search_zh = index_zh.searcher(weighting=TF_IDF()) 
		self.__search = index.searcher(weighting=TF_IDF())
		self.__parser_title_zh = QueryParser('title', self.__search_zh.schema)
		self.__parser_content_zh = QueryParser('content', self.__search_zh.schema)
		self.__parser_url_zh = QueryParser('url', self.__search_zh.schema)
		self.__parser_title = QueryParser('title', self.__search.schema)
		self.__parser_content = QueryParser('content', self.__search.schema)
		self.__parser_url = QueryParser('url', self.__search.schema)

	def searchItems(self,content,limit=None,stored=None,reverse=False):
		myquery = self.__parser_title_zh.parse(content)
		if stored != None:
			facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
			results = self.__search_zh.search(myquery, limit=limit, sortedby=facet)
		else:
			results = self.__search_zh.search(myquery, limit=limit)
		myquery = self.__parser_content_zh.parse(content)
		if stored != None:
			facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
			res = self.__search_zh.search(myquery, limit=limit, sortedby=facet)
		else:
			res = self.__search_zh.search(myquery, limit=limit)
		results.upgrade_and_extend(res)
		myquery = self.__parser_url_zh.parse(content)
		if stored != None:
			facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
			res = self.__search_zh.search(myquery, limit=limit, sortedby=facet)
		else:
			res = self.__search_zh.search(myquery, limit=limit)
		results.upgrade_and_extend(res)
		if len(results) == 0:
			myquery = self.__parser_title.parse(content)
			if stored != None:
				facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
				results = self.__search.search(myquery, limit=limit, sortedby=facet)
			else:
				results = self.__search.search(myquery, limit=limit)
			myquery = self.__parser_content.parse(content)
			if stored != None:
				facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
				res = self.__search.search(myquery, limit=limit, sortedby=facet)
			else:
				res = self.__search.search(myquery, limit=limit)
			results.upgrade_and_extend(res)
			myquery = self.__parser_url.parse(content)
			if stored != None:
				facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
				res = self.__search.search(myquery, limit=limit, sortedby=facet)
			else:
				res = self.__search.search(myquery, limit=limit)
			results.upgrade_and_extend(res)
		return results
		'''
		new_list = []
		for res in results:
			#print(dict(res))  
			new_list.append(dict(res))
		return new_list'''
	'''
	def __searchItemsFromParser_zh(self,parser,content,limit=None,stored=None,reverse=False):
		new_list = []
		self.__parser_zh = QueryParser(parser, self.__search_zh.schema)
		myquery = self.__parser_zh.parse(content)
		if stored != None:
			facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果  
			results = self.__search_zh.search(myquery, limit=limit, sortedby=facet)  #limit为搜索结果的限制，默认为10，详见博客开头的官方文档  
		else:
			results = self.__search_zh.search(myquery, limit=limit)
		for res in results:  
			#print(dict(res))
			new_list.append(dict(res))
		return new_list

	def __searchItemsFromParser(self,parser,content,limit=None,stored=None,reverse=False):
		new_list = []
		self.__parser = QueryParser(parser, self.__search.schema)
		myquery = self.__parser.parse(content)
		if stored != None:
			facet = FieldFacet(stored, reverse=reverse)  #按序排列搜索结果
			results = self.__search.search_page(myquery, pagenum=limit, sortedby=facet)
			#results = self.__search.search(myquery, limit=limit, sortedby=facet)  #limit为搜索结果的限制，默认为10，详见博客开头的官方文档  
		else:
			#results = self.__search.search(myquery, limit=limit)
			pass
		for res in results:
			#print(dict(res))  
			new_list.append(dict(res))
		return new_list
	'''
	def buildIndex(self,reslist):
		self.__createIndex()
		for item in reslist:
			self.__addItem_zh(item['title'],item['target'],item['site'],item['content'],item['url'],item['uid'])
		for item in reslist:
			self.__addItem(item['title'],item['target'],item['site'],item['content'],item['url'],item['uid'])
		
		self.__writer_zh.commit()
		self.__writer.commit()
		print("Successfully to build indexs.")
		pass
	'''
	def getResList(self,content,limit=None,stored=None,reverse=False):
		l = []
		for item in ['title','target','content','site','url']:
			tmp = self.__searchItemsFromParser_zh(parser=item,content=content,limit=limit,stored=stored,reverse=reverse)
			#print(tmp)
			l.extend(tmp)
		if l == []:pass
		for item in ['title','target','content','site','url']:
			tmp = self.__searchItemsFromParser(parser=item,content=content,limit=limit,stored=stored,reverse=reverse)
			l.extend(tmp)
		return l
	'''
	def updateIndex(self,reslist):
		self.__ix_zh = open_dir("path_zh", indexname='indexname_zh')
		self.__writer_zh = self.__ix_zh.writer()
		self.__ix = open_dir("path", indexname='indexname')
		self.__writer = self.__ix.writer()

		for item in reslist:
			self.__addItem_zh(item['title'],item['target'],item['site'],item['content'],item['url'],item['uid'])
		for item in reslist:
			self.__addItem(item['title'],item['target'],item['site'],item['content'],item['url'],item['uid'])
		
		self.__writer_zh.commit()
		self.__writer.commit()
		print("Successfully to update indexs.")
		pass

if __name__ == '__main__':
	searcher = Searcher()
	s = [{"url": "https://www.bilibili.com/video/av109900", "title": "央视名嘴阿丘点评口才帝蓝志", "target": "哔哩哔哩 (゜-゜)つロ 干杯~", "site": "bilibili", "uid": "/0", "content": " 蓝志加了个油"}]
	'''
	s = [{'title':'first','target':'math','site':'CSDN','content':'This is math item.','url':'www.csdn.net','uid':'/1'},
			{'title':'second','target':'chinese','site':'Baidu','content':'This is chinese item.','url':'www.baidu.com','uid':'/2'},
			{'title':'third','target':'english','site':'Bing','content':'This is english item.','url':'www.github.com','uid':'/3'}]
	'''
	#s = [{"title":'这是一个测试列表','target':'测试',"content":"央视名嘴阿丘点评口才帝蓝志",'url':'www.bilibili.com','site':'bilibili','uid':'/0'}]
	searcher.buildIndex(s)
	s = time.time()
	res = searcher.getResList('蓝志')
	new_res = []
	for id in res:
		if id not in new_res:
			new_res.append(id)
	print(time.time() - s)
	print(new_res)