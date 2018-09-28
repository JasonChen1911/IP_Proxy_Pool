#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/26 下午1:27
# @Author       : JasonChen
# @File         : web_api.py
# @Software     : PyCharm
# @description  : 

from flask import Flask
import time
from database_manager import *


app = Flask(__name__)

@app.route('/')
def index():

    return "Welcome the IP_Proxy_Pool!  /get 获取一个代理IP  /count 获取代理池中的IP数量"

@app.route('/get')
def get_proxy():
    rdb = redisClient()
    ip = rdb.pop()
    return ip

@app.route('/count')
def get_count():
    rdb = redisClient()
    count = rdb.count()
    return str(count)

if __name__ == '__main__':
    app.run(threaded = True)

