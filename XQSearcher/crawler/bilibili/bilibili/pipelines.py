# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import glob

class BilibiliPipeline(object):
    num = len(glob.glob(os.path.join('./json/bili_*.json')))
    def process_item(self, item, spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        if item['content'] == '':
        	return
        file_name = os.path.join('./json/bili_'+str(self.num)+'.json')
        self.num += 1
        print(os.path.abspath(file_name))
        with codecs.open(file_name, 'wb+', encoding='utf-8') as f:
            f.write(json.dumps(dict(item), ensure_ascii=False, sort_keys=False)+'\n')
        return item
