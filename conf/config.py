# coding: utf-8
import os, sys
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print "当前使用配置文件%s"%(os.path.abspath(__file__))

# 日志文件
logfile = os.path.join(HOME, 'log/myblog.log')

# 端口
port = 8888

# 模板路径
template = os.path.join(HOME, 'bin/template')

settings = {'debug':True}
