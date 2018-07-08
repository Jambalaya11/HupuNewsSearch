# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuspiderItem(scrapy.Item):
	
    teamname = scrapy.Field()
    teamurl = scrapy.Field()
    newstitle = scrapy.Field()
    newsurl = scrapy.Field()
    content = scrapy.Field()
    imageurl = scrapy.Field()
