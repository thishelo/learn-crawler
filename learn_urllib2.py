# -*- coding:utf-8 -*-

import urllib2

url = raw_input("please input url：")

# 构建User-Agent
headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
}

#调用Reques方法

request = urllib2.Request(url, headers = headers)

response = urllib2.urlopen(request)

html = response.read()

print html