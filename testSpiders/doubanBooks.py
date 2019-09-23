"""
爬虫功能：
    抓取豆瓣top100书单；
    分别使用正则表达式 和 beautifulsoup进行解析；
    并保存为.txt文件；
"""

import requests
from requests.exceptions import RequestException
import re
import json
import time
from bs4 import BeautifulSoup


"""
函数说明：通过url抓取页面信息
Param: url
Return: html(text)
"""
def get_one_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None    
    except RequestException:
        return None


"""
函数说明：使用beautifulsoup解析页面信息
Param: html
Returns: item
"""
def parse_one_page(html):
    """正则表达式解析"""
    # pattern = re.compile('<div class="bd doulist-subject">.*?class="post">.*?<a href="(.*?)".*?src="(.*?)">.*?class=title">.*?"_blank">(.*?)</a>.*?rating_nums">(.*?)</span>.*?"abstract">(.*?)</div>',
    #     re.S)
    # items = re.findall(pattern, html)
    # print(len(items))
    # for item in items:
    #     yield {'url': item[0],
    #         'image': item[1],
    #         'title': item[2].strip(), 
    #         'score': item[3].strip(),
    #         'abstract': item[4].strip()
    #     }

    soup = BeautifulSoup(html, 'lxml')
    for item in soup.find_all(attrs={'class':'bd doulist-subject'}):
        yield {
            'url': item.find(class_='post').a['href'],
            'image': item.find(class_='post').a.img['src'],
            'title': item.find(class_='title').a.string.strip(),
            'score': item.find(class_='rating_nums').string.strip(),
            'abstract': item.find(class_='abstract').text.strip()
        }

"""
函数说明：数据写入文件
"""
def write_to_file(content): 
    with open('./data/doubanBoooksTop100.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(nums):
    url = 'https://www.douban.com/doulist/45004834/?start='+str(nums)+'&sort=time&playable=0&sub_type='
    html = get_one_page(url)
    print(type(html))
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(4):  # get 4 pages info
        main(nums=i*25)  # nums of books
        time.sleep(1)  # 防止爬取过快





