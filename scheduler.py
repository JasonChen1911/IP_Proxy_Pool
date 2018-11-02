#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 下午3:28
# @Author       : JasonChen
# @File         : scheduler.py
# @Software     : PyCharm
# @description  : 调度器


from get_ip import *
from database_manager import *
from settings import *
from web_api import *
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
        # 获取代理ip列表
        webGetter().IP_run()

    def used_ip_checker(self):
        print("检测已用IP的可用性")
        rdb = redisClient()
        used_len = rdb.count(USERDPROXIES)
        IP_Lists = rdb.get(USERDPROXIES, used_len)
        for ip in IP_Lists:
            value = webGetter().is_validity(ip)
            if value:
                rdb.put(REDISNAME, ip)

    def unused_ip_checker(self):
        print("未用IP可用性检测")
        #rdb = redisClient()
        pass

    def schedul_checker(self):
        print("IP池检测器启动")
        rdb = redisClient()
        while True:
            count = rdb.count(REDISNAME)
            print("IP池当前代理数量为%s！" %(count))
            if count < MINNUM:
                self.ip_generater()
            if count < MAXNUM:
                self.used_ip_checker()
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