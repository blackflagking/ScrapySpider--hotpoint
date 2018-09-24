# -*- coding: utf-8 -*-
import scrapy
import sys
import re
import urllib
from spider.items import SpiderItem
reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=25017023_10_pg&wd=%E7%83%AD%E7%82%B9&oq=%25E7%2583%25AD%25E6%25AD%25BB%25E5%25AE%2589&rsv_pq=83529cd8000127f4&rsv_t=240bkzyqroYixb%2FU3ugOquSY%2FtwKG3xBAw1Hqw44iCGeaiE6G98Vw9z89Ml6KCthadOQ1J0&rqlang=cn&rsv_enter=1&rsv_sug3=6&rsv_sug1=5&rsv_sug7=100&bs=%E7%83%AD%E6%AD%BB%E5%AE%89']

    def parse(self, response):

        item = SpiderItem()

        pro_char = 'http://www.baidu.com/'
        for num in range(1, 11):
            pro_hot = response.xpath("//div[@class='FYB_RD']/table/tbody[1]/tr[%d]" % num)
            hotname = pro_hot.xpath('td/span/a/text()').extract()[0]
            hoturl  = pro_hot.xpath('td/span/a/@href').extract()[0]
            theurl  =  pro_char + hoturl

            item['bdname'] = hotname
            item['bdurl'] = theurl
            print hotname, theurl
        yield scrapy.Request(url='https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q=%E7%83%AD%E7%82%B9', meta={'item':item}, callback=self.get360, dont_filter=True)

    def get360(self, response):
        item = response.meta['item']

        for num in range(1,3):
            pro = response.xpath("//ul[@class='mh-wrap js-mh-wrap mh-active']/li[@class='mh-item'][%d]/ul[@class='mh-col']" % num)
            for num in range(1, 11):
                name = pro.xpath("li[@class='g-ellipsis'][%d]/a/text()" % num).extract()[0]
                url  = pro.xpath("li[@class='g-ellipsis'][%d]/a/@href" % num).extract()[0]

                item['name360'] = name
                item['url360'] = url
                print name, url
        yield scrapy.Request(url="http://s.weibo.com/ajax/jsonp/gettopsug?uid=&ref=PC_topsug&url=http%3A%2F%2Fs.weibo.com%2Ftop%2Fsummary&Mozilla=Mozilla%2F5.0%20",encoding='utf-8', meta={"item": item}, callback=self.weibo, dont_filter=True)

    def weibo(self, response):
        item = response.meta["item"]
        responsebody = response.body
        namelist = re.findall(',"word":"(.*?)",', responsebody)
        pro_url = "http://s.weibo.com/weibo/"
        for i in namelist:
            name = i.encode('ascii').decode('unicode_escape')
            wbname = urllib.quote(name.encode('utf-8'))
            url = pro_url + wbname

            item['weiboname'] = name
            item['weibourl'] = url
            print name, url
            yield item
