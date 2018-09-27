#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 下午3:28
# @Author       : JasonChen
# @File         : scheduler.py
# @Software     : PyCharm
# @description  : 调度器


from IP_Proxy_Pool.get_ip import *
from IP_Proxy_Pool.database_manager import *
from IP_Proxy_Pool.settings import *
from IP_Proxy_Pool.web_api import *
from multiprocessing import Process
import time



'''
    1、ip池的定期检测
    2、ip池第一次启动时注入ip
    3、ip池补入

'''
# 插入ip
class IPProxyPoolGenerater(object):
    def __init__(self):
        self._circle = INTERVARLS

    def ip_generater(self):
        # 判断proxies是否存在，存在的话清空
        print("IP池生成器启动")
        rdb = redisClient()
        print(rdb)
        rdb.del_key()
        # 获取代理ip列表
        ip_lists = webGetter().IPLists()
        print("获取到的IP：")
        print(ip_lists)
        if not ip_lists:
            print("获取代理ip 失败")
        rdb.puts(ip_lists)

    def schedul_checker(self):
        print("IP池检测器启动")
        rdb = redisClient()
        while True:
            count = rdb.count()
            print("IP池当前代理数量为%s！" %(count))
            if count < MINNUM:
                self.ip_generater()
            time.sleep(self._circle)


    def schedul_api(self):
        app.run()

    def run(self):
        if True:
            p1 = Process(target=self.schedul_checker)
            p1.start()
        if True:
            p2 = Process(target=self.schedul_api)
            p2.start()

if __name__ == '__main__':
    IPProxyPoolGenerater().run()