import json
import random
import threading

import requests
import parsel

url_all = input("url:")
list_all = []  # 储存章节
list_books = {}  # 章节：内容
list_list = {}  # 编号：内容
thread_list = []  # 守护进程
proxy_ip = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54"
}


# 获取代理ip
def get_ip():
    file = open("代理.txt", 'r', encoding='utf-8')
    papers = []
    for line in file.readlines():
        c = json.loads(line)
        papers.append(c)
    file.close()
    return papers


# 获取小说名字
def get_name():
    url = url_all
    resp = requests.get(url=url, headers=headers)
    resp.encoding = "gbk"
    selector = parsel.Selector(resp.text)
    name = selector.css("#info>h1::text").get()
    print(name)
    return name


# 获取小说章节列表数量
def get_list_num():
    url = url_all
    resp = requests.get(url=url, headers=headers)
    resp.encoding = "gbk"
    selector = parsel.Selector(resp.text)
    all_list = selector.css(".form-control>option").extract()  # 获取一共多少页
    all_list_num = len(all_list)  # 页数
    return all_list_num


#  获取章节数量和连接
def get_list(list_num):
    url = url_all
    n = 1
    for i in range(2, list_num + 2):
        resp = requests.get(url=url, headers=headers)
        resp.encoding = "gbk"
        selector = parsel.Selector(resp.text)
        list = selector.css(".zjlist>dd>a::attr(href)").extract()  # 获取链接地址
        # list_name = selector.css(".zjlist>dd>a::text").extract()  # 获取章节名字
        # next_list = selector.css(".btn-default::attr(href)").extract()[1] #下一页的地址
        url = url_all + "index_" + str(i) + ".html"  # 拼接目录
        print("获取第", n, "页目录")
        for i in list:
            list_url = url_all + i  # 拼接小说章节地址
            list_all.append(list_url)
        n += 1
    print("一共获取{}章".format(len(list_all)))


#  多线程工具
def threading_test(url, num):
    t = threading.Thread(target=visit, args=(url, num))
    thread_list.append(t)


# 编写 标题：内容， 编号：内容
# 参数为 章节地址， 编号
def visit(url, num):
    ip_num = random.randint(1, len(proxy_ip) - 2)
    while True:
        try:
            prox = {'http': proxy_ip[ip_num]["http"]}
            resp = requests.get(url=url, headers=headers, proxies=prox, timeout=1)
            resp.encoding = "gbk"
            selector = parsel.Selector(resp.text)
            print("success")
            str = selector.css("#content *::text").extract()  # 获取内容
            title = selector.css("#main > h1::text").get()  # 获取标题
            books = ""
            for i in range(3, len(str)):
                books = books + str[i]
            list_books[title] = books  # 标题 ： 内容
            list_list[num] = title  # 编号：标题
            return
        except:
            ip_num = random.randint(1, len(proxy_ip) - 2)
            print("异常")


def run(name):
    x = 1
    for i in list_all:
        threading_test(i, x)
        x += 1
    for t in thread_list:
        t.setDaemon(True)  # 设置为守护线程，不会因主线程结束而中断
        t.start()
    for t in thread_list:
        t.join()  # 子线程全部加入，主线程等所有子线程运行完毕
    a = sorted(list_list)
    f = open(name + ".txt", 'w', encoding='utf-8')
    for i in a:
        f.write(list_list[i] + '\n')
        f.write(list_books[list_list[i]] + '\n')


if __name__ == '__main__':
    name = get_name()
    get_list(get_list_num())
    proxy_ip = get_ip()
    run(name)
