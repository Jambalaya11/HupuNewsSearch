# -*- coding: utf-8 -*-
import scrapy
import os
import json
from HupuSpider.items import HupuspiderItem
item = HupuspiderItem()


class NbaNewsSpider(scrapy.Spider):
    name = 'nba_news'
    allowed_domains = ['hupu.com']
    start_urls=['https://voice.hupu.com/nba/']

    def parse(self, response):
        items=[]

	result=response.xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/ul')

	# 球队队名
	team=result.xpath('.//li/a/text()').extract()
	allteam=team[:-1]
	team=result.xpath('.//li[last()]/div/a/text()').extract()
	allteam.extend(team)

	# 球队url
	teamurl = result.xpath('.//li/a/@href').extract()
	allteamurl = teamurl[:-1]
	teamurl = result.xpath('.//li[last()]/div/a/@href').extract()
	allteamurl.extend(teamurl)

	# 爬取所有的球队
	for i in range(0,len(allteam)):
	    item = HupuspiderItem()

	    # 指定存储目录+球队名字
	    teamFilename="./hupunews/"+allteam[i]

	    # 如果目录不存在，则创建目录
	    if (not os.path.exists(teamFilename)):
		os.makedirs(teamFilename)

	    item['teamname']=allteam[i]
	    item['teamurl']=allteamurl[i]

	    items.append(item)

	#发送每个球队url的Request请求，得到Response连同包含meta数据
	# 一同交给回调函数 second_parse 方法处理
	for item in items:
	    for i in range(1,2):
		tempurl = item['teamurl'].replace('.html','')
		teamurl = tempurl + '-' + str(i) + '.html'
		yield scrapy.Request( url = teamurl, meta={'meta_1': item}, callback=self.second_parse)
     
    # 对每支球队的url进行爬取
    def second_parse(self,response):
        items=[]
 
        # 提取每次Response的meta数据
        meta_1 = response.meta['meta_1']
 
        # 提取每支球队的所有新闻url
        allurl = response.xpath('//html/body/div[3]/div[1]/div/div[@class="list"]/div/div/span/a/@href').extract()
        # 提取每支球队的所有新闻标题
        alltitle = response.xpath('//html/body/div[3]/div[1]/div/div[@class="list"]/div/div/span/a/text()').extract()
 
        for i in range(0, len(alltitle)):
            item=HupuspiderItem()
            item['teamname'] = meta_1['teamname']
            item['teamurl'] = meta_1['teamurl']
            item['newstitle'] = alltitle[i]
            item['newsurl'] = allurl[i]
 
            items.append(item)
 
            # 指定存储目录+球队名字+新闻标题文件夹
            newsFilename =  "./hupunews/"+item['teamname']+'/' + alltitle[i]
 
             # 如果目录不存在，则创建目录
            if (not os.path.exists(newsFilename)):
                os.makedirs(newsFilename)
 
        # 发送每个新闻链接url的Request请求，得到Response后连同包含meta数据
        # 一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['newsurl'], meta={'meta_2': item}, callback=self.detail_parse)
 
    def detail_parse(self,response):
        item = response.meta['meta_2']
        content = ""
        # 提取所有p标签里的文本内容
        content_list = response.xpath('//html/body/div[4]/div[1]/div[2]/div/div[2]/p/text()').extract()
        # 提取配图url
        imageurl = response.xpath('/html/body/div[4]/div[1]/div[2]/div/div[1]/img/@src').extract()
 
        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
            content +="\n"
 
        item['content'] = content
        item['imageurl'] = imageurl
        # 将获取的数据交给pipelines
        yield item
 
