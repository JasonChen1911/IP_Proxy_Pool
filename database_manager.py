#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 下午4:15
# @Author       : JasonChen
# @File         : database_manager.py
# @Software     : PyCharm
# @description  : 

import redis
from settings import *

class redisClient(object):
    def __init__(self, host=HOST, port=PORT):
        self._db = redis.Redis(host, port, decode_responses=True)
    # 获取一定数量的代理IP
    def get(self, database, count=1):
        proxies = self._db.lrange(database, 0, count-1)
        self._db.ltrim(database, count, -1)
        return proxies


    def put(self, database, proxy):
        self._db.rpush(database, proxy)

    def puts(self, database, proxies):
        self._db.rpush(database, *proxies)

    # 从右侧获取代理IP
    def pop(self, database):
        if self._db.llen(database):
            ip = self._db.rpop(database)
            return ip
        else:
            return 0
    def count(self, database):
        return self._db.llen(database)

    def del_key(self, database):
        self._db.delete(database)

if __name__ == '__main__':
    rdb = redisClient()
    proxies = rdb.get(REDISNAME, 12)
    print(proxies)