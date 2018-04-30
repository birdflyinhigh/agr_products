# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ProductPipeline(object):
    # 保存数据，创建文件
    def open_spider(self, spider):

        pass

    def process_item(self, item, spider):

        pass



    def close_spider(self, spider):

        pass




