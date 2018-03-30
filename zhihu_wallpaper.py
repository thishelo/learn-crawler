# -*- coding: utf-8 -*-

import os
import requests
from lxml import html

headers = {
    'Host': 'www.zhihu.com',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}


def save(text, filename='temp', path='download1'):
    fpath = os.path.join(path, filename) 
    with open(fpath, 'wb') as  f:          #用"wb"方不会出现图片花掉
        print('output:', fpath)
        f.write(text)


def save_image(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    save(page, filename)
    print "saving" + filename


def crawl(url):
    resp = requests.get(url, headers=headers)
    page = resp.content
    root = html.fromstring(page)
    image_urls = root.xpath('//img[@data-original]/@data-original')
    for image_url in image_urls:
        save_image(image_url)


if __name__ == '__main__':
    """注意在运行之前，先确保该文件的同路径下存在一个download1的文件夹, 用于存放爬虫下载的图片
       输入任意知乎问题url，例如：https://www.zhihu.com/question/263362761
    """
    url = raw_input("please input url:")  
    crawl(url)