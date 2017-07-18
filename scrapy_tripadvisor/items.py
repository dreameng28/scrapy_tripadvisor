# -*- coding: utf-8 -*-

import scrapy


class AttractionItem(scrapy.Item):
    # define the field crawled from the website
    geo = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    count = scrapy.Field()
    tag = scrapy.Field()
    pic_des = scrapy.Field()
    pic_captionprovider = scrapy.Field()
