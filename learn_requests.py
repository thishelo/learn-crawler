# -*- coding:utf-8 -*-

import requests

#发送get请求 time表示最多等待时间
#response = requests.get("https://translate.google.cn/"， time=3)

#返回字节流数据来查看相应体内容，text返回的是unicoding内容
#print response.content

#print response.url

#打印出编码格式windows是gb2312
#print response.encoding

#print response.headers

#print response.text

#自定义headers

#headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
#}

#根据协议类型选择代理
proxies = {
	"http" : "http://115.218.120.157",
	"https" : "https://115.218.120.157",
}


response = requests.get("https://www.baidu.com", proxies = proxies)

print response.text

"""
proxies = {
  "http": "http://117.90.252.77",
  "https": "http://117.90.252.77",
}

response = requests.get("http://www.baidu.com", proxies = proxies)
print response.text"""