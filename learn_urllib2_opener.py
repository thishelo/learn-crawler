# coding=utf-8

import urllib2

#构建处理器对象来支持处理HTTP请求,debuglevel=1参数可以打开debug模式
http_handler = urllib2.HTTPHandler(debuglevel=1)

#调用build_opener()方法构建自定义opener对象，参数是构建的处理器对象

opener = urllib2.build_opener(http_handler)

request = urllib2.Request("http://www.baidu.com/")

#不用调用urllib2.urlopen了
response = opener.open(request)

print response.read()