#! /usr/bin/python3
# _*_ coding:utf-8 _*_

"""

@ File   :网易歌单爬取.py
@ Author :ShenggengLin
@ Mail   :liuhedong135@163.com
@ Date   :2020-08-25

"""

from urllib import parse
from lxml import etree
from urllib3 import disable_warnings
import requests
import csv
import re
import urllib.request
import urllib.error
import urllib.parse
import cloudmusic


def get_Lables(url, name):  # 获得歌单的标签，传入参数为网易云的歌单url和歌单的名字

    header = {  # 请求头部
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=header)
    html = urllib.request.urlopen(request).read().decode('utf-8')  # 打开url

    html = str(html)  # 转换成str

    # print(url)
    pat = r'<meta name="description" content="([\d\D]*?)" />'

    # pat = r'<meta name="keywords" content="(.*?)" />\n<meta name="description"'
    result_label = re.compile(pat).findall(html)  # 用正则表达式进行筛选
    # print(result_label)
    ss = ''.join(result_label)  # '歌单名，创作者，标签1，标签2···'
    all = []

    all = ss.split('，')  # 切分字符串 ['歌单名','创作者','标签1','标签2',```]
    # print(all)

    ns = name.count('，', 0, len(name))  # 歌单名中拥有的逗号的数量
    # print(ns)
    x = 0
    while x < ns + 1:  # 清除all里面的歌单名
        t = all.pop(0)
        # print(all.pop(0))
        x += 1
    # t = all.pop(0)  # 清除all里面的创作者
    biaoqian = all[0]
    biaoqian1 = biaoqian.split('：')
    biaoqian2 = biaoqian1[-1]
    # print(biaoqian2)

    return biaoqian2


class Wangyiyun(object):

    def __init__(self, **kwargs):
        # 歌单的歌曲风格
        self.types = kwargs['types']
        # 歌单的发布类型
        self.years = kwargs['years']
        # 这是当前爬取的页数
        self.pages = pages
        # 这是请求的url参数（页数）
        self.limit = 35
        self.offset = 35 * self.pages - self.limit
        # 这是请求的url
        self.url = "https://music.163.com/discover/playlist/?"

    # 设置请求头部信息(可扩展：不同的User - Agent)
    def set_header(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1',
        }
        return self.header

    # 设置请求表格信息
    def set_froms(self):
        self.key = parse.quote(self.types)
        self.froms = {
            "cat": self.key,
            "order": self.years,
            "limit": self.limit,
            "offset": self.offset,
        }
        return self.froms

    # 解析代码，获取有用的数据
    def parsing_codes(self):
        page = etree.HTML(self.code)

        # 标题
        self.title = page.xpath('//div[@class="u-cover u-cover-1"]/a[@title]/@title')
        # 作者
        self.author = page.xpath('//p/a[@class="nm nm-icn f-thide s-fc3"]/text()')
        # 阅读量
        self.listen = page.xpath('//span[@class="nb"]/text()')
        # 歌单链接
        self.link = page.xpath('//div[@class="u-cover u-cover-1"]/a[@href]/@href')
        # 歌单标签


        #gedanlabel = get_Lables("https://music.163.com/" + self.link, self.title)
        '''
        for i in zip(self.title, self.link, self.author, self.listen):
            print("[歌单名称]：{}\n[发布作者]：{}\n[总播放量]：{}\n[歌单链接]：{}\n".format(i[0], i[2], i[3], "https://music.163.com/" + i[1]))

            gedanlabel = get_Lables("https://music.163.com/" + i[1], i[0])
            print(gedanlabel)
        '''
    # print('第{}页'.format(self.pages).center(50,'='))

    # 写入文件
        for i in zip(self.title, self.link, self.author, self.listen,self.code):
            id = i[1].split("=")[-1]
            gedanlabel = get_Lables("https://music.163.com/" + i[1], i[0])
            writer.writerow([id,i[0], i[2], i[3],"https://music.163.com/" + i[1], gedanlabel])
        csv_file.close()


# 获取网页源代码
    def get_code(self):
        disable_warnings()
        self.froms['cat'] = self.types
        disable_warnings()
        self.new_url = self.url + parse.urlencode(self.froms)
        self.code = requests.get(
            url=self.new_url,
            headers=self.header,
            data=self.froms,
            verify=False,
        ).text


# 爬取多页时刷新offset
    def multi(self, page):
        self.offset = self.limit * page - self.limit


if __name__ == '__main__':
    # =======================================
    # 指定一些参数
    # 歌单的歌曲风格
    csv_file = open("playlist.csv", "a", encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['playlist_id', 'playlist_name', 'author', 'Amount_of_play', 'Playlist_link', 'Playlist_label'])
    types = "说唱"
    # 歌单的发布类型:最热=hot，最新=new
    years = "hot"
    # 指定爬取的页数
    pages = 20
    # =======================================

    # =======================================
    # 例子：通过pages变量爬取指定页面（多页）
    music = Wangyiyun(
        types=types,
        years=years,
    )

    for i in range(pages):
        page = i + 1  # 因为没有第0页
        music.multi(page)  # 爬取多页时指定，传入当前页数，刷新offset
        music.set_header()  # 调用头部方法，构造请求头信息
        music.set_froms()  # 调用froms方法，构造froms信息
        music.get_code()  # 获取当前页面的源码
        music.parsing_codes()  # 处理源码，获取指定数据

'''
import cloudmusic
musiclist = cloudmusic.getPlaylist(5101056870)
# 通过歌单id来定位歌单
for music in musiclist:
    print("歌曲名称：{}".format(music.name))

'''

'''
def get_Lables(url,name):    #获得歌单的标签，传入参数为网易云的歌单url和歌单的名字
    header = {  # 请求头部
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=header)
    html = urllib.request.urlopen(request).read().decode('utf-8')  # 打开url
    html = str(html)  # 转换成str

    #print(url)
    pat=r'<meta name="description" content="([\d\D]*?)" />'

    #pat = r'<meta name="keywords" content="(.*?)" />\n<meta name="description"'
    result_label = re.compile(pat).findall(html)  # 用正则表达式进行筛选
    #print(result_label)
    ss = ''.join(result_label)  # '歌单名，创作者，标签1，标签2···'
    all = []

    all = ss.split('，')  # 切分字符串 ['歌单名','创作者','标签1','标签2',```]
    #print(all)
    
    ns = name.count('，', 0, len(name))  # 歌单名中拥有的逗号的数量
    #print(ns)
    x = 0
    while x < ns + 1:  # 清除all里面的歌单名
        t = all.pop(0)
        # print(all.pop(0))
        x += 1
    #t = all.pop(0)  # 清除all里面的创作者
    biaoqian=all[0]
    biaoqian1=biaoqian.split('：')
    biaoqian2=biaoqian1[-1]
    #print(biaoqian2)

    return biaoqian2

label=get_Lables('https://music.163.com//playlist?id=5101056870')
'''
