# HupuNewsSearch
elastic search 6.2.4 --开源搜索引擎<br/>
scrapy 1.5.0 --爬虫工具<br/>
django 1.11.13 --页面展示<br/>

*Hupuspider<br/>
用于爬取虎扑网站上所需的内容并将爬取的内容存储在es中

*website<br/>
django向es发送post请求，将query传给es,并展示搜索结果

+attention<br/>
es分词：插件ik <br/>
es展示：elastic search head<br/>
去重:redis 

*使用<br/>
1.需要将es打开：brew services start elasticsearch or elasticsearch <br/>使用127.0.0.1:9200访问<br/>
2.打开es head:进入es head 安装目录： npm run start<br/> 使用127.0.0.1:9100访问 <br/>
3.打开redis:redis-server /usr/local/etc/redis.conf<br/>
4.打开爬虫:进入Hupuspider目录：scrapy crawl nba_news<br/>
5.打开网站:进入website目录：python manage.py runserver 9000><br/>
6.访问链接： http://127.0.0.1:9000/home




