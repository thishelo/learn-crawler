# -*- coding:utf-8 -*-

import requests
from lxml import etree
from Queue import Queue
import threading
import time
import json




class ThreadCrawl(threading.Thread):
    """爬取页面的类"""
    def __init__(self, threadName, pageQueue, dataQueue ):
        #调用父类__init__方法
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
} 
    
    #把要运行的代码写在run方法里，线程创建后会直接运行run方法
    def run(self):
        #print "go" + self.threadName
        while not CRAWL_EXIT:
            try:
                #block默认是True,会阻塞，所以设为False
                page = self.pageQueue.get(False) * 25
                print page
                url = "https://www.douban.com/doulist/2602718/?start=" + str(page)
                #print url
                
                res = requests.get(url, headers = self.headers).text
                time.sleep(1)
                self.dataQueue.put(res)
            except:
                pass
            
        #print "exit" + self.threadName

class Threadparse(threading.Thread):
    """创建解析类,解析并获得想要的页面内容"""
    def __init__(self, threadName, dataQueue, filename, lock):
        super(Threadparse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.filename = filename
        self.lock = lock 
    def run(self):
        #print "go" + self.threadName
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                self.parse(html)
            except:
                pass
        #print "exit" + self.threadName
    def parse(self, html):
        #解析为 HTML DOM
        html = etree.HTML(html)

        #用xpath强大的模糊查询获取根节点,注意单双引号
        node_list = html.xpath('//div[contains(@class, "doulist-item")]')

        for node in node_list:
            num = node.xpath('.//span[@class="pos"]')[0].text
            name = node.xpath('.//div/div[2]/div[3]/a')[0].text
            star = node.xpath('./div/div[2]/div[4]/span[2]')[0].text
            info = node.xpath('./div/div[2]/div[5]')[1].text

        


            items = {
                "name" : name,
                "info" : info,
                "star" : star,
                "num" : num
            }   
                
            with self.lock:
                #用dumps()把python对象转化为json字符串并保存
                self.filename.write(json.dumps(items,ensure_ascii = False).encode("utf-8") + "\n")
                    


            

CRAWL_EXIT = False
PARSE_EXIT = False

def main():
    #创建一个页面队列，表示40个页面
    print "haha" + threading.active_count()
    pageQueue = Queue(40)

    for i in range(0, 40):
        pageQueue.put(i)

    #创建数据队列
    dataQueue = Queue()

    lock = threading.Lock()


    #采集页面的线程名字
    crawlList = ["collection1", "collection2", "collection3"]
    #创建列表储存采集线程
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue )
        thread.start()
        threadcrawl.append(thread)

    filename = open("doulist.json", "a")
    #用来保存解析线程
    threadparse = ["parse1", "parse2", "parse3"]
    for threadName in threadparse:
        thread = Threadparse(threadName, dataQueue, filename, lock )
        thread.start()
        threadparse.append(thread)

        

    #等待页面队列为空然后采集线程退出
    while not pageQueue.empty():
        pass

    global CRAWL_EXIT
    CRAWL_EXIT = True
    print "pageQueue is empty now"

    for thread in threadcrawl:
        thread.join()
        print "1"

    global PARSE_EXIT
    PARSE_EXIT = True
    #由于线程是非守护线程要等待线程运行
    for thread in threadparse:
        thread.join()
        print "2"
    with lock:
        filename.close()
    print "thanks use！"







if __name__ == '__main__':
    main()