from urllib.parse import urlencode  
import requests  
from pyquery import PyQuery as pq
from pymongo import MongoClient

# Ajax分析! 爬取某一位用户的微博！


base_url = 'https://m.weibo.cn/api/container/getIndex?'  

"""
 根据request Header构造
"""
headers = {  
    'Host': 'm.weibo.cn',  
    'Referer': 'https://m.weibo.cn/u/1353112775',  # +uid
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  
    'X-Requested-With': 'XMLHttpRequest',  
}  

"""
函数说明：构造URL，获取一个XHR请求的页面，以json格式返回
Param：page(页码)
Returns: json格式的页面数据
"""
def get_page(page):
    params = {  
        'type': 'uid',  
        'value':'1353112775', # uid
        'containerid': '1076031353112775',  # 107603+uid
        'page': page  
    }  
    url = base_url + urlencode(params)  # urlencode()可以直接生成url格式字符串
    try:  
        response = requests.get(url, headers=headers)  
        if response.status_code == 200:  # ok
            return response.json()  # 以json格式返回
    except requests.ConnectionError as e:  
        print('ConnectionError', e.args)

"""
函数说明：PyQuery解析页面，转发链接、图片等还没有处理；
Param: json
Returns: Item
"""
def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['time'] = item.get('created_at')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo

"""
MongoDB 保存
"""
client = MongoClient()
db = client['weibo']
collection = db['weibo']
def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')


if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            save_to_mongo(result)
            # print(result)
