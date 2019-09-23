from bs4 import BeautifulSoup
import sys, requests


"""
类说明：下载《笔趣看》网络小说《一念永恒》
Parameters: None
Returns: None
Modify: 2019-9-19
"""
class downLoader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []  # 存放章节名字
        self.urls = []   # 存放章节链接
        self.nums = 0    # 记录章节数目

    """
    函数说明： 获取下载链接
    Parameters: None
    Returns: None
    Modify: 2019-9-19
    """
    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = 'gbk'
        htmlText = req.text
        bf = BeautifulSoup(htmlText)
        texts = bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(texts[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a:
            self.names.append(each.string)
            self.urls.append((self.server + each.get('href')))

    """
    函数说明：获取章节内容
    Modify: 2019-9-19
    """            
    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = 'gbk'
        htmlText = req.text
        bf = BeautifulSoup(htmlText)
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    """
    函数说明：将爬取的内容写入文件
    Modify: 2019-9-19
    """
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = downLoader()
    dl.get_download_url()
    print('《一念永恒》开始下载>>>')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '一年永恒.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载：%.3f%%" % float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print('《一念永恒》下载完成')














