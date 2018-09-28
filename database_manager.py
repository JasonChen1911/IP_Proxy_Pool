#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 下午4:15
# @Author       : JasonChen
# @File         : database_manager.py
# @Software     : PyCharm
# @description  : 

import redis
from settings import HOST, PORT, REDISNAME

class redisClient(object):
    def __init__(self, host=HOST, port=PORT):
        self._db = redis.Redis(host, port, decode_responses=True)

    def get(self, count=1):
        proxies = self._db.lrange(REDISNAME, 0, count-1)
        self._db.ltrim(REDISNAME, count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush(REDISNAME, proxy)

    def puts(self, proxies):
        self._db.rpush(REDISNAME, *proxies)

    # 从右侧获取代理ip
    def pop(self):
        if self._db.llen(REDISNAME):
            return self._db.rpop(REDISNAME)
        else:
            return '代理IP池空了！！！'
    def count(self):
        return self._db.llen(REDISNAME)

    def del_key(self):
        self._db.delete(REDISNAME)

if __name__ == '__main__':
    rdb = redisClient()
    ips = ["http://192.168.0.1:8888", "http://192.168.0.1:8888", "http://192.168.0.1:8888", "http://192.168.0.1:8888", "http://192.168.0.1:8888"]
    for ip in ips:
        print(ip)
        rdb.put(ip)
    rdb.puts(ips)
    address = rdb.count()
    print(address)