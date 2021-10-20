#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
httpx是一个爬虫库
对比常用的 requests, 除了支持 requests 的所有操作之外，还具有以下特点：
1.同时支持同步和异步请求
2.支持 HTTP1.0/HTTP2.0
3.可直接向 WSGI 程序或 ASGI 程序发出请求
4.类型注释
从以上可以看出在 requests 的所有功能之上，增加了更多新的功能，相当于一个功能更强大的 requests !!

安装:
pip insatll httpx

ps: 如果使用支持http2的功能,请选择这种安装方式: pip install httpx[http2]
"""
import httpx

url = 'https://www.baidu.com'
headers = {
        "cookie": 'your cookie',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
data = {
    "key": "value"
    }

"""基本操作, 等同于requests库"""
resp_get = httpx.get(url, headers=headers)                  # get方法
print(resp_get.text)
print(resp_get.status_code)
print(resp_get.content)

resp_post = httpx.post(url, data=data, headers=headers)     # post方法
print(resp_post.text)
print(resp_post.status_code)
print(resp_post.content)


"""
会话保持, client等同于requests.Session()
使用 Client 具有更高的性能, 因为Client实例使用HTTP 连接池！在向同一主机发出多个请求时, Client 将重用底层 TCP 连接，而不是为每个请求重新创建一个。
"""
with httpx.Client() as client:
    resp = client.get(url)
    print(resp.status_code)


"""
事件监听
如在请求完全准备好之后，但还未被发送到网络之前会调用 log_request 函数
在网络获取响应返回之后，但还未发送到调用着之前会调用 log_response 函数
通过下面两个函数，可以实现日志记录，请求监控等等功能
"""


def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")


client = httpx.Client(event_hooks={'request': [log_request], 'response': [log_response]})


"""异步请求"""
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(response)

asyncio.run(main())


"""
支持HTTP/2
使用 httpx 客户端时，默认情况下不启用 HTTP/2 , 在安装 HTTP/2 依赖后可使用
设置参数 http2=True
"""
async with httpx.AsyncClient(http2=True) as client_a:
    r = client_a.get(url)

"""
有些网站不支持HTTP/2
判断网站是否支持HTTP/2
"""
client_b = httpx.AsyncClient(http2=True)
response = await client_b.get(url)
print(response.http_version)
# "HTTP/1.0", "HTTP/1.1", "HTTP/2"
