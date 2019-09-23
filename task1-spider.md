**Task**：搜寻“不同标准的”
请自定义“最好用”，请记录搜索过程，以及搜索结果，以及你自己的分析结论

---
## 作业总结

**必做**：关于爬虫库和框架的报告如下；知乎回答已详细阅读，但是鉴于自己水平有限，大部分复现都有难度，先实现几个可以快速上手的爬虫，希望之后能尝试；

**Challenge**： 总共实现了四个小爬虫，后有介绍


这一周，阅读了大量博客和知乎问答(后有链接)，同时分别尝试了用正则表达式、beautifulsoup、pyquery解析网页，之后尝试了scrapy和pyspider爬虫框架，精力有限，Nutch留到之后来了解；

# “最好用”的开源框架
个人认为，没有绝对意义上的”最好用“的框架，针对不同的需求，每种框架有各自的优势，而决定一个爬虫框架/软件优劣的大概有以下几个方面：

1、易用性
框架和软件实现网页抓取和调试的难度；相比于scrapy的命令行调试，pyspider的图形化界面个人感觉就很“省力”（当然也是自己命令行功夫不到家）

2、反爬能力：
对接代理池、cookie池是否方便；Ajax动态页面抓取是否方便；对于加载算法太复杂的网站，实现浏览器模拟登录、渲染是否方便；

3、数据对接问题
是否支持与各种数据库和消息队列的对接；目前大部分爬虫框架都支持蛮好的。

4、是否支持分布处理：
如果是大型项目，有大量的爬取需求，单机显然是不现实的，分布式部署就显得很关键；分布式部署的环境配置也比较麻烦，如果能支持Docker部署就很赞了。

5、扩展问题
比如pyspider相比于scrapy，虽然可以快速实现网页爬虫，但是可扩展程度不足；scrapy对接Middleware、Pipeline可以应对各种反爬能力较强的网站；


# 解析库

0、正则表达式

1、beautifulsoup

2、pyquery 

3、Xpath （未尝试）
自己只尝试了前三种，beautifulsoup和pyquery功能都很强大，至于孰优孰劣，觉得还是看个人的熟练程度；

# 框架对比
## 一、scrapy:
[Scrapy-官方文档](https://docs.scrapy.org/en/latest/) - Python爬虫

架构非常清晰，大家都说功能十分强大；

然只实现了简单的网页爬取，但是
内置了Xpath和css选择器，好像没有beautifulsoup？不过css选择器失恋了之后还是很方便的；

### 不足
相比于pysipder，需要命令行调试；


## 二、pyspider 
[PySpider-官方文档](http://docs.pyspider.org/en/latest/) - python爬虫
### 优点
图形化的操作界面简直太惊艳了，用WebUI实现网页的抓取和分析（是内置了PyQuery解析库的，但是图形化操作真的方便）；可以实时监控爬取进度，不同颜色表示不同的返回情况；爬取结果可以直接以json、csv等各种格式导出；对于各种数据库的后端支持也很好，目前值尝试了mongodb，其他还没有操作；
其他高阶功能：
分布式部署；Docker部署；
对接PhantomJS，可实现动态渲染的抓取；
支持各种消息队列；

### 不足
可扩展性较差

## 三、Nutch

Nutch是一个基于Lucene，类似Google的完整网络搜索引擎解决方案，基于Hadoop的分布式处理模型保证了系统的性能，类似Eclipse的插件机制保证了系统的可客户化，而且很容易集成到自己的应用之中。

### 不足
Nutch依赖hadoop运行，hadoop本身会消耗很多的时间。如果集群机器数量较少，爬取速度反而不如单机爬虫快。

具体本周实在精力有限，之后再细细了解！


【参考文档】
[Python有哪些常见的、好用的爬虫框架？](https://www.zhihu.com/question/60280580/answer/617068010)

[知乎回答: 开源爬虫框架各有什么优缺点？](https://www.zhihu.com/question/27042168/answer/70821088)

[开源爬虫Labin，Nutch，Neritrix介绍和对比](https://www.open-open.com/bbs/view/1325332257061)

[知乎：50种最棒的开源爬虫框架/项目](https://zhuanlan.zhihu.com/p/64305013)

【待看优秀项目】

[GitHub 上有哪些优秀的 Python 爬虫项目？](https://www.zhihu.com/question/58151047/answer/640461600)

一个爬虫排名，不知道是否客观，待研究……
[Top 50 open source web crawlers for data mining](https://bigdata-madesimple.com/top-50-open-source-web-crawlers-for-data-mining/)

## 爬虫的正当性
[爬虫的合法性问题](https://www.zhihu.com/question/291554395/answer/476074383)

[友情提示：爬虫违法](https://zhuanlan.zhihu.com/p/54013381)

---

# Challenge： 总共实现了四个小爬虫

之前没有是编写过，重在体会过程！

## 1. 无框架爬取（静态、动态）

### 1.1、实现豆瓣读书（分别使用正则表达式 和 beautifulsoup）
**页面类型**：豆瓣读书排行属于静态页面，十分易于爬取；

**URL构造**：针对多个页面，点击不同页面观察其url的变化，发现只有start部分变为一个新数字，通过推算，应该表示当前的项目序号！这样就可以构造url了

**页面解析**：分别使用正则表达式和beautifulsoup进行解析；具体逻辑请移步代码；


### 1.2 爬取微博内容（Ajax动态加载）
**页面类型**： 结论：Ajax动态加载；
浏览微博时，随着你不断向下滚动，新的内容会不断出现。如果我们以上一爬虫的抓取方法，抓取结果只有初始加载的几十行html代码，没有任何有用信息，显然有问题； 

进入微博主页，选择开发者选项的network，限定只看XHR类型的URL，接着向下滑动，会发现不断有请求和返回产生，点击getindex?type……的项，就是最新的Ajax请求，点击Preview，就能看到返回的内容，点击Response能看到数据是以json格式组织的；

**动态加载分析：**

点击某一个XHR类URL，在Header中可以看到Request Header的各项内容，这样就很方便我们构造请求；通过观察不同请求的Header，可以发现随着下拉动态加载页面的Request URL中只有page选项在发生变化，其他都是固定的；这样就可以构造url了；

**页面解析**

这次解析尝试用pyquery，只要获得了response，用pyquery语法操作；

**数据存储**

数据保存到MongoDB中；
	

# 2、pyspider + phantomjs 抓取豆瓣图书排行

### **环境配置**

Ubuntu 18.04 +
PhantomJS-2.2.1 + MongoDB + PyMongo 库

可能出现的问题：
1、 PhantomJS已在后台启动，会报错；

**解决**：杀死进程，重新启动；

（selenium提示它已经不支持phantom了啊，让用Chrome或Firefox……）
2、WebUI出现窗口很小的问题

**解决：** 需要修改debug.min.css 和debug.min.js两个文件，具体参考此github讨论: - [链接](https://github.com/binux/pyspider/issues/740)

### 操作流程
1、create新建项目，输入起始页url和项目名；

2、点击run单步调试进行首页爬取，右侧是调试界面；

3、点击web按钮，点击css功能，可以进行链接图形话界面选取；之后加入后侧代码；

4、定义翻页逻辑，找到next项url，使用callback()回调，实现下一页页面处理；

5、代码只需修改Handler类，逻辑和1.1相同；

### PS：
这个图形化操作方式真的很难用语言描述，还是建议大家上手尝试一下，真的很爽！


# 3、scrapy 
目标网站：http://www.juzizhai.com/doc/mingyan/mingren/
### 环境配置
Ubuntu 18.04 + MongoDB + PyMongo 库

### 目的
重在走一遍基本过程，之后再尝试动态加载和浏览器模拟的内容；

1、创建项目；

2、创建Spider：

定义想要爬取的属性信息，

3、解析网页：

scrapy内嵌了css选择器，具体爬取规则可查看文档；主要点是后续request的衔接：找到”下一页”标签，callback构造循环；

4、对接数据结构：新建item实时保存
  -可以抓取查看效果，再进行数据库保存

5、数据存储：scrapy可以在抓取时直接输出为各种格式数据：csv, json, pickle等或者可以直接ftp传输

6、数据库链接：使用Item Pipeline
Item Pipeline的主要作用清洗 HTML 数据，验证爬取数据，检查爬取字段，查重并丢弃重复内容，将爬取结果储存到数据库；

在setting.py 中配置数据库信息；

7、执行抓取！
	
# 后记

一周的精力实在有限，各种东西只是初步感受了一下；

因为网站结构的时效性很强，所以网上很多爬虫教程即使很新，不少也会爆出各种Bug，心累……；

爬虫还是蛮有意思的(除了密密麻麻的前端代码)，想要好好研究一下。



