# -*- coding: utf-8 -*-

import os
import requests
from lxml import html

class Zhihu_wallpapper(object):

    def __init__(self, url):
        
        self.url = url

    
    def save(self, text, filename='temp', path='download'):
        #拼接文件路径名
        fpath = os.path.join(path, filename) 
         #用二进制写模式打开，否则爬下来的图片会花掉
        with open(fpath, 'wb') as  f:         
            #print 'output:', fpath
            f.write(text)


    def save_image(self, image_url):
        
        resp = requests.get(image_url)
        page = resp.content
         
        #切割image_url后半部分为文件名
        filename = image_url.split('zhimg.com/')[-1] 
        self.save(page, filename)
        print "saving:", filename



    def crawl(self):

        #构建请求头 
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

        resp = requests.get(self.url, headers=headers)
        page = resp.content
        #print page
        #得到对象根节点,HTML对象
        root = html.fromstring(page)
        #用XPath得到图片url列表
        image_urls = root.xpath('//img[@data-original]/@data-original')
        
        #print image_urls
        
        for image_url in image_urls:
            #将处理好的图片url传递给save_image方法
            self.save_image(image_url)
            


if __name__ == '__main__':
    """注意在运行之前，先确保该文件的同路径下存在一个download的文件夹, 用于存放爬虫下载的图片
       输入任意知乎问题url，例如：https://www.zhihu.com/question/263362761
    """
    url = raw_input("please input url:") 
    img = Zhihu_wallpapper(url)
    img.crawl()