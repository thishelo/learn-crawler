# -*- coding: utf-8 -*-

import os
import requests
import json
from lxml import html
import jsonpath
from time import sleep
import urllib2
import re
from bs4 import BeautifulSoup

class Zhihu_wallpapper(object):

    def __init__(self, questionID):
        
        self.questionID = questionID
        DIR = "img"
        if not os.path.exists(DIR):

            os.makedirs(DIR)

    
    def save(self, text, filename='temp', path='img'):
        #拼接文件路径名
        fpath = os.path.join(path, filename) 
        #epath = str(fpath)
         #用二进制写模式打开，否则爬下来的图片会花掉
        with open(fpath, 'wb') as  f:         
            #print 'output:', fpath
            f.write(text)


    def save_image(self, image_url):
        #获取图片响应体
        resp = requests.get(image_url)
        #content返回的是byte型数据
        page = resp.content
         
        #切割image_url后半部分为文件名
        filename = image_url.split('zhimg.co')[-1] 
        self.save(page, filename)
        #打印的中文转成unicode在windows平台就不会出现乱码了，win平台会自动把unicode转成gbk
        print u"正在保存:", filename
    

    """def save_image(self, image_url):  
    # 对图片进行存储  
        root = "D:\PY\CrawZhihuPic\pics"  # 这里注意一下转义符  
        path = root + image_url.split('/')[-1]  
        try:  
            if not os.path.exists(root):  
                os.mkdir(root)  
            if not os.path.exists(path):  
                r = requests.get(image_url)  
                with open(path, 'wb') as f:  
                    f.write(r.content)  
                    f.close()  
        except:  
            print u"文件保存出现错误"
    """


    def crawl(self):
        #此函数负责拿到图片url
        #构建请求头
        offset = 5
        l_offset = 10
        fir_url = "https://www.zhihu.com/api/v4/questions/" + self.questionID + "/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=" + str(offset) 
        sec_url = "https://www.zhihu.com/api/v4/questions/" + self.questionID + "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=" + str(l_offset) + "&sort_by=default"
        
        AUTHORIZATION ="oauth c3cef7c66a1843f8b3a9e6a1e3160e20"

        REFERER = "https://www.zhihu.com/question/" + self.questionID
        
        USER_AGENT ="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
        
        headers = {
            "User-Agent": USER_AGENT,

            "Referer": REFERER,

            "authorization": AUTHORIZATION

        }

        res = requests.get(fir_url, headers = headers)
        text = res.text
        #json转化为python对象
        js = json.loads(text)
        #print js
        answers_count = js['paging']['totals']
        print u"本问题下共有{}个回答".format(answers_count)
        sleep(1)

        request = urllib2.Request(fir_url, headers = headers)
        response = urllib2.urlopen(request)

        html = response.read()

        image_urls =[]

        for ans in js['data']:  
            soup = BeautifulSoup(ans['content'], 'html.parser')  
            for img in soup.find_all('img'):  
                match = re.match(r'https://.*?\.jpg', img.get('src'))  
                if match:  
                    image_urls.append(match.group(0)) 

        """py_html = json.loads(html)

        #print py_html

        fir_imgurl_list = jsonpath.jsonpath(py_html, "$..name")
        """
        #for item in urlList:
         #   print item


        

        
        #print page
        #得到对象根节点,HTML对象
        
        #用XPath得到图片url列表
        
        
        #print image_urls
        
        for image_url in image_urls:
            #将处理好的图片url传递给save_image方法
            self.save_image(image_url)
        
def main():
    questionID = raw_input("please input questionID:")

    img = Zhihu_wallpapper(questionID)
    #print "测试"
    #print u"测试unicode"
    img.crawl()

            


if __name__ == '__main__':
    """注意在运行之前，先确保该文件的同路径下存在一个download的文件夹, 用于存放爬虫下载的图片
       输入任意知乎问题url，例如：https://www.zhihu.com/question/263362761
    """
    main()
    