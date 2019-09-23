# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from OrangeSpider.items import MingrenItem 

class MingrenSpider(scrapy.Spider):
    name = 'mingren'
    # allowed_domains = ['juzizhai.com/doc/mingyan/mingren']
    allowed_domains = ['juzizhai.com']
    start_urls = ['http://juzizhai.com/doc/mingyan/mingren/']
    def parse(self, response):
        # response.css('a[href="image1.html"] img::attr(src)').extract_first()
        articles = response.css('article[class="post format-standard"]')
        print('articles_len', len(articles))
        for article in articles:
            item = MingrenItem()
            item['title'] = article.css('.entry-title a::text').extract_first()
            item['type'] = article.css('.entry-meta a::text').extract()[1]
            item['text'] = article.css('p::text').extract_first() # why None
            item['link'] = article.css('a[class="more-link dt-btn"]::attr(href)').extract_first()
            yield item

        next = response.css('a[class="pageNumber next"]::attr(href)').extract_first()
        url = response.urljoin(next)
        print("*********************** New Page ******************************")
        yield scrapy.Request(url=url, callback=self.parse)


