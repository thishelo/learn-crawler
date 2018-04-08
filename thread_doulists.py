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
		print "start" + self.threadName
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
			
		print "exit" + self.threadName	


			

CRAWL_EXIT = False
PARSE_EXIT = False

def main():
	#创建一个页面队列，表示40个页面
	pageQueue = Queue(40)

	for i in range(0, 40):
		pageQueue.put(i)

	#创建数据队列
	dataQueue = Queue()


	#采集页面的线程名字
	crawlList = ["collection1", "collection2", "collection3"]
	#创建列表储存采集线程
	threadcrawl = []
	for threadName in crawlList:
		thread = ThreadCrawl(threadName, pageQueue, dataQueue )
		thread.start()
		threadcrawl.append(thread)


	#等待页面队列为空然后采集线程退出
	while not pageQueue.empty():
		pass

	global CRAWL_EXIT
	CRAWL_EXIT = True
	print "pageQueue is empty now"

	for thread in threadcrawl:
		thread.join()
		print "1"






if __name__ == '__main__':
	main()