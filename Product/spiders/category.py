# -*- coding: utf-8 -*-
import scrapy
import scrapy
import re
import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from Product.items import ProductItem


from Product.mysql_writer import insert_item




categories = []


class CategorySpider(Spider):
    name = 'category'
    allowed_domains = ['zgny.com.cn']
    start_urls = ['http://zgny.com.cn/']

    # redis_key = 'product'

    def parse(self, response):

        big_categories = response.xpath('//div[@class="FenLei_01"]')

        for big in big_categories:
            big_category = big.xpath('div[1]/text()|div[1]/a/text()').extract_first()
            # print(big_category)
            small_categories = big.xpath('div[3]/div')
            for small in small_categories:
                small_category = small.xpath('span/a/text()').extract_first()
                child_categories = small.xpath('a')
                for child in child_categories:
                    temp = {}
                    child_catagory = child.xpath('text()').extract_first()
                    child_catagory_url = child.xpath('@href').extract_first()
                    temp = {
                        'big_category': big_category,
                        'small_category': small_category,
                        'child_category': child_catagory,
                        'child_catagory_url': child_catagory_url
                    }
                    categories.append(temp)





class ProductSpider(CrawlSpider):
    name = 'product'
    allowed_domains = ['zgny.com.cn']
    start_urls = ['http://www.zgny.com.cn/']
    # redis_key = 'product'

    rules = (
        # http://sc.zgny.com.cn/Products
        Rule(LinkExtractor(allow=r'/Products/Page_[\d]+_NodeId_.*_.*_.*\.shtml'), follow=True),
        # /Product_31160502.shtml
        Rule(LinkExtractor(allow=r'/Product_[\d]+\.shtml$'), callback='parse_detail', follow=False),

    )


    def __init__(self, temp=None, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self.start_urls = [temp['child_catagory_url']]
        # print(self.start_urls)
        self.temp = temp
        # print(temp)
        self._compile_rules()
        # self.f = open('data.json', 'w')

    def parse_detail(self, response):
        temp = self.temp
        item = ProductItem()

        item['big_category'] = temp['big_category']
        item['small_category'] = temp['small_category']
        item['child_category'] = temp['child_category']
        name = response.xpath('//div[@class="gqGongSi"]/text()').extract_first()
        address = self.parse_address(response)
        contact = self.parse_contact(response)

        desc = self.parse_desc(response)

        item['name'] = name
        item['address'] = address
        item['url'] = response.url
        item['contact'] = contact
        item['desc'] = desc

        # str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        # self.f.write(str_data)

        insert_item(item)

        yield item

    def parse_contact(self, resp):
        """解析联系方式"""
        paras = resp.xpath('//p').extract()
        additional_paras = resp.xpath('//div[@class="wenZi_02"]/text()').extract()
        paras = paras + additional_paras
        contact = ''
        mobiles = None
        tel = None
        for para in paras:
            if not para:
                continue
            regex = '(1[35789][\d]{9})'
            result1  = re.findall(regex, para)
            regex = '(0[1-9]+[-]{0,1}[\d]{7,8})'
            result2 = re.findall(regex, para)
            if result1:
                mobiles = list(set(result1))
                for i ,mobile in enumerate(mobiles):
                    if i == 2:
                        break
                    contact += mobile + ' '

            if result2:
                tel = list(set(result2))[0]
                contact += tel + ' '

        return contact

    def parse_address(self, resp):
        """解析地址"""
        address = resp.xpath('//div[@class="proCon"]/div[2]/text()').extract_first()
        if address:
            address = address.replace('地址：', '')
            return address
        else:
            content = resp.text
            result = re.findall('地址：(.*)</div>\r', content)
            if result:
                address = result[0]
                print(resp.url, '*' * 50)
        return address

    def parse_desc(self, resp):
        """解析产品介绍"""
        headers = resp.xpath('//span[@class="wenZi_04"]')
        desc = ''
        for header in headers:
            content = header.xpath('text()').extract_first()
            if '产品' in content:
                siblings = header.xpath('following-sibling::*')
                for sibling in siblings:
                    paragraph = sibling.xpath('text()').extract_first()
                    if paragraph:
                        paragraph = paragraph.strip()
                        desc += paragraph + '\n'
                        # print(paragraph)

        additional_paras = resp.xpath('//div[@class="wenZi_02"]/text()').extract()
        desc = desc.strip()

        for para in additional_paras:
            if para:
                para = para.strip()
                desc += para + '\n'

        desc = desc.strip()

        return desc












configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(CategorySpider)
    for temp in categories:
        yield runner.crawl(ProductSpider, temp=temp)
    reactor.stop()

crawl()
reactor.run()