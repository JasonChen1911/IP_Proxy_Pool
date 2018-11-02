#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2018/9/25 上午10:13
# @Author       : JasonChen
# @File         : settings.py
# @Software     : PyCharm
# @description  : 配置文件


# 请求参数
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

# 测试URL
# 拿目标网站做测试，如果通过，则是可用的，未通过的直接省去
TEST_URL = 'https://so.m.jd.com/webportal/channel/m_category'

# Redis 数据库配置
REDISNAME = "proxies"
USERDPROXIES = "used_proxies"
HOST = 'localhost'
PORT = 6379
MINNUM = 20
MAXNUM = 50


# 间隔时间
INTERVARLS = 120