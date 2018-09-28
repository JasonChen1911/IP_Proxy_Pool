# IP_Proxy_Pool
一个比较简单的初级IP代理池。  
整个工程一共有四个模块分别是：控制器模块、IP爬取模块、数据存储模块、api接口模块。  

## 运行环境
Python3.6  

## 控制器模块：
scheduler.py  
控制器管理整个工程的运行，使用`multiprocessing`模块的 `Process` 函数，启动IP池监测函数与接口函数  

## IP爬取模块：
get_ip.py  
爬取快代理的免费IP  

## 数据库模块：
database_manager.py  
封装redis数据库的相关操作方法
## api接口模块：
web_api.py  
使用Flask模块封装接口服务  
## 配置文件：
settings.py  
整个工程的配置信息

## 运行
    python scheduler.py
运行以上命令启动ip代理池，然后在本地浏览器输入http://127.0.0.1:5000/ 回车，获取整个服务的功能说明。





