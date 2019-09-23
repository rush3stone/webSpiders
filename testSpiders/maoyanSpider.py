import requests
from requests.exceptions import RequestException
import re
import json
import time

"""
regex + requests;
"""

"""
Get html info of one page using url
"""
def get_one_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        # set encoding?
        if response.status_code == 200:
            return response.text
        return None    
    except RequestException:
        return None


"""
Get ranking, name, actor, releasetime, score of one movie
"""
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', 
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'index': item[0],
            'image': item[1],
            'title': item[2].strip(), 
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }


"""
Write to file
    Param: content: the info of one movie, dict
"""
def write_to_file(content): 
    with open('./data/maoyanTop100.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):  # get 10 pages info
        main(offset=i*10)  # offset of url
        time.sleep(1)





