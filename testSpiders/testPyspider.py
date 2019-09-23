#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-09-23 00:28:13
# Project: DoubanBooks

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.douban.com/doulist/45004834/?start=0&sort=time&playable=0&sub_type=', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')
        next = response.doc('.next > a').attr.href
        self.crawl(next, callback=self.index_page)
            
            
    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "author": response.doc('#info > a').text(),
            "intro": response.doc('#link-report .intro > p').text(),
            "image": response.doc('.nbg > image').attr.src
        }
