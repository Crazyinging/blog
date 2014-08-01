#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
HOME = os.path.dirname(os.path.abspath(__file__))
from common.base import loader
loader.loadconf(HOME)
import config

import tornado
import tornado.web



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('jiong~~~')

application = tornado.web.Application([
    # 主页
    (r'/', IndexHandler)
])

def main():
    try:
        application.listen(config.port)
        instance = tornado.ioloop.IOLoop.instance()
        instance.start()
    except:
        print "wrong......"

if __name__ == '__main__':
    print "start"
    main()
