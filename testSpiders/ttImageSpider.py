import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re

def get_page(offset):
    headers = {
        # you need to update cookie when you run this code
        'cookie': '__tasessionId=invmd00nc1568970224936; csrftoken=816ec0eb7fe12d8edd37c95fedbe8355; tt_webid=6738675946939926019; s_v_web_id=f04a10d6b28ef3a395ffbb972b869973; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',        
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    # print(url)
    try:
        resp = requests.get(url, headers=headers)
        if 200  == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('title') is None:
                continue
            title = re.sub('[\t]', '', item.get('title'))
            images = item.get('image_list')
            for image in images:
                # use regex to modify the url and then get original picture
                origin_image = re.sub("list.*?pgc-image", "large/pgc-image", image.get('url'))
                origin_image = re.sub("list", "large", origin_image)
                yield {
                    'image': origin_image,
                    'title': title
                }


def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image')) # binary data
        if codes.ok == resp.status_code:   # requests.codes.ok is 200;
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),  # use md5 to name the image
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f: # write as binary
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already Downloaded', file_path)
    except Exception as e:
        print(e)
                                

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        save_image(item)


GROUP_START = 0
GROUP_END = 9

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()

