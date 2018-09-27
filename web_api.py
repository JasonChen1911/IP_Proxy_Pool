#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/26 下午1:27
# @Author       : JasonChen
# @File         : web_api.py
# @Software     : PyCharm
# @description  : 

from flask import Flask
import time
from IP_Proxy_Pool.database_manager import *


app = Flask(__name__)

@app.route('/')
def index():

    return 'Welcome the IP_Proxy_Pool!'

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

