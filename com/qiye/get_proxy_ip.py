import threading
import time

import requests
import parsel
import json

proxy_list1 = []
def get_ip(page):
    print("获取第", page, '页')
    if page >= 0:
        url = 'https://www.kuaidaili.com/free/inha/' + str(page) + '/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54"
        }
        resp = requests.get(url=url, headers=headers)
        selector = parsel.Selector(resp.text)
        # css 提取器
        trs = selector.css("#list > table > tbody > tr")
        for tr in trs:
            ip = tr.css("td:nth-child(1)::text").get()
            port = tr.css("td:nth-child(2)::text").get()
            # adress = tr.xpath("td[4]/text()").get()
            # ip代理
            proxies_dict = {
                "http": "http://" + ip + ":" + port,
                # "https" : "https://" + ip + ":" + port,
            }
            try:
                resp_1 = requests.get(url='https://www.baidu.com/', proxies=proxies_dict, timeout=0.1)
                if resp_1.status_code == 200:
                    proxy_list1.append(proxies_dict)
            except:
                print(proxies_dict, "当前ip失效")


def success():
    print("开始获取ip，请稍等")
    for i in range(1, 20):
        threading.Thread(target=get_ip, args=(i,)).start()
        time.sleep(2)
    f = open('代理.txt', mode='w', encoding='utf-8')
    for proxy in proxy_list1:
        f.write(json.dumps(proxy))
        f.write('\n')


if __name__ == '__main__':
    success()
