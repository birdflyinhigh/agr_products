# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 大类名，小类名，小类下子类名，商品名称，地址，联系电话，产品介绍

    # 大类名
    big_category = scrapy.Field()
    # 小类名
    small_category = scrapy.Field()
    # 小类下子类名
    child_category = scrapy.Field()
    # 商品名称
    name = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 联系电话
    contact = scrapy.Field()
    # 产品介绍
    desc = scrapy.Field()
    # 产品链接
    url = scrapy.Field()


