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
from IP_Proxy_Pool.settings import *



class webGetter():
    def __init__(self):
        self._xicidlIPLists = []
        self._kuaidlIPLists = []
    # 获取网页信息
    def _get_web(self, url, host=None):
        headers = {
            'User-Agent' : USER_AGENT,
        }
        try:
            if host:
                r = requests.get(url, headers=headers, timeout=30, proxies=host)
            else:
                r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print("Error:status is ", r.raise_for_status)
    # 验证ip地址是否可用
    def _is_validity(self, host):
        headers = {
            'User-Agent': USER_AGENT,
        }

        try:
            html = requests.get(TEST_URL, headers=headers, proxies=host, timeout=10)
            if html.status_code == 200:
                return True
            else:
                return False
        except:
            return 'error'

    # 获取西刺代理ip
    def _xicidl(self, index, num, host=None):
        url = 'http://www.xicidaili.com/nn/'+str(index)
        html = self._get_web(url,host)
        if html == None:
            #百分九十九 ip 被封
            return 0
        r_soup = BeautifulSoup(html, 'lxml')
        nav_num = r_soup.find_all("div", {"class": "pagination"})[0].find_all("a")[-2].text
        tr_soup = r_soup.find_all('table', {'id':'ip_list'})[0].find_all('tr')
        for ip_item in tr_soup:
            items = ip_item.find_all('td')
            if len(items) > 0:
                ip = items[1].text
                port = items[2].text
                type = items[5].text
                host = {
                    type.lower() : type.lower() + "://" + ip + ":" + str(port)
                }
                value = self._is_validity(host)

                if value == True:
                    self._xicidlIPLists.append(host)
                    num += 1
                else:
                    pass
                if num > MAXNUM:
                    return self._xicidlIPLists
        index += 1
        time.sleep(2)
        if index > int(nav_num):
            return 0
        self._xicidl(index, num, host)

    def _kuaidl(self, index, num, host=None):
        url = 'https://www.kuaidaili.com/free/inha/'+str(index)
        html = self._get_web(url, host)
        if html == None:
            #百分九十九 ip 被封
            return 0
        r_soup = BeautifulSoup(html, 'lxml')
        nav_num = r_soup.body.contents[1].find_all("div", {"id": "listnav"})[0].find_all("a")[-1].text
        tr_text = r_soup.body.contents[1].find_all("tbody")[0].find_all("tr")  # .find_all("td")
        for item in tr_text:
            ip = item.find("td", {"data-title": "IP"}).text
            port = item.find("td", {"data-title": "PORT"}).text
            type = item.find("td", {"data-title": "类型"}).text
            host = {type.lower(): type.lower() + "://" + ip + ":" + str(port)}
            value = self._is_validity(host)
            if value == True:
                self._kuaidlIPLists.append(host)

            else:
                pass
            num += 1
            if num > MAXNUM:
                return self._kuaidlIPLists
        index += 1

        time.sleep(2)
        if index == int(nav_num) + 1:
            return 0
        self._kuaidl(index, num, host)

    def IPLists(self):
        if self._kuaidlIPLists:
            self._kuaidlIPLists = []
        if self._xicidlIPLists:
            self._xicidlIPLists = []
        #self._xicidl(1, 1)
        self._kuaidl(1, 1)
        if self._kuaidlIPLists and self._xicidlIPLists:
            return (self._xicidlIPLists + self._kuaidlIPLists)
        elif self._kuaidlIPLists:
            return self._kuaidlIPLists
        elif self._xicidlIPLists:
            return self._xicidlIPLists
        else:
            return []

if __name__ == '__main__':
    getter = webGetter()
    ip_lists = getter.IPLists()
    print(ip_lists)
