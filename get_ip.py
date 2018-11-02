#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 上午10:13
# @Author       : JasonChen
# @File         : get_ip.py
# @Software     : PyCharm
# @description  : 获取ip地址

import requests
from bs4 import BeautifulSoup
import time
from settings import *
from database_manager import *
from multiprocessing import Process


class webGetter():
    def __init__(self):
        self._xicidlIPLists = []
        self._kuaidlIPLists = []
        self._db = redisClient()


    # 获取网页信息
    def _get_web(self, url, host=None):
        headers = {
            'User-Agent' : USER_AGENT,
        }
        print(url, host)
        try:
            if host:
                try:
                    r = requests.get(url, headers=headers, timeout=30, proxies=host)
                except:
                    r = requests.get(url, headers=headers, timeout=30)
            else:
                r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print("Error")
    # 验证ip地址是否可用
    def is_validity(self, host):
        headers = {
            'User-Agent': USER_AGENT,
        }
        print(host)
        try:
            html = requests.get(TEST_URL, headers=headers, proxies=host, timeout=10)
            if html.status_code == 200:
                return True
            else:
                return False
        except:
            return 'error'

    # 获取西刺代理ip
    def _xicidl(self, index=1, host=None):
        url = 'http://www.xicidaili.com/nn/'+str(index)
        html = self._get_web(url,host)
        if html == None:
            #百分九十九 ip 被封
            return 0
        r_soup = BeautifulSoup(html, 'lxml')
        nav_num = r_soup.find_all("div", {"class": "pagination"})[0].find_all("a")[-2].text
        tr_soup = r_soup.find_all('table', {'id':'ip_list'})[0].find_all('tr')
        proxies=""
        for ip_item in tr_soup:
            items = ip_item.find_all('td')
            if len(items) > 0:
                ip = items[1].text
                port = items[2].text
                type = items[5].text
                address = ip + ":" + str(port)
                host = {
                    'http': 'http://' + address,
                    'https': 'https://' + address
                }
                value = self.is_validity(host)
                if value == True:
                    self._db.put(address)
                    proxies = host
                else:
                    pass
        index += 1
        time.sleep(2)
        if index > int(nav_num):
            return 0
        self._xicidl(index, proxies)

    def _kuaidl(self, index=1, host=None):
        url = 'https://www.kuaidaili.com/free/inha/'+str(index)
        html = self._get_web(url, host)
        if html == None:
            #百分九十九 ip 被封
            return 0
        r_soup = BeautifulSoup(html, 'lxml')
        nav_num = r_soup.body.contents[1].find_all("div", {"id": "listnav"})[0].find_all("a")[-1].text
        tr_text = r_soup.body.contents[1].find_all("tbody")[0].find_all("tr")  # .find_all("td")
        proxies = ""
        for item in tr_text:
            ip = item.find("td", {"data-title": "IP"}).text
            port = item.find("td", {"data-title": "PORT"}).text
            type = item.find("td", {"data-title": "类型"}).text
            address = ip + ":" + str(port)
            host = {
                'http': 'http://' + address,
                'https': 'https://' + address
            }
            value = self.is_validity(host)
            if value == True:
                self._db.put(address)
                proxies = host
            else:
                pass
        index += 1
        time.sleep(2)
        if index > 50:
            return 0
        self._kuaidl(index, proxies)

    def _89ip(self, index=1, host=None):
        url = 'http://www.89ip.cn/index_'+str(index)+'.html'
        html = self._get_web(url, host)
        if html == None:
            return 0
        r_soup = BeautifulSoup(html, 'lxml')
        tr_soups = r_soup.find_all('tbody')[0].find_all('tr')
        if len(tr_soups) < 1:
            return 0

        for tr_soup in tr_soups:
            td_soups = tr_soup.find_all('td')
            if len(td_soups) > 0:
                ip = td_soups[0].text.strip()
                port = td_soups[1].text.strip()
                address = ip + ":" + str(port)

                host={
                    'http' : 'http://'+address,
                    'https': 'https://'+address
                }
                value = self.is_validity(host)
                if value:
                    self._db.put(address)
                    proxies = host

        index = index + 1
        time.sleep(2)
        if(index > 10):
            return 0
        self._89ip(index, proxies)



    def IP_run(self):
        if True:
            p1 = Process(target=self._89ip)
            p1.start()
        if True:
            p2 = Process(target=self._kuaidl)
            p2.start()
        if True:
            p3 = Process(target=self._xicidl)
            p3.start()
        return 1

if __name__ == '__main__':
    getter = webGetter()
    getter.IP_run()
