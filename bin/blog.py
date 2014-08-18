#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
HOME = os.path.dirname(os.path.abspath(__file__))
from common.base import loader, logger
from common.web import template
loader.loadconf(HOME)
import config
log = logger.install('stdout')#(config.logfile)

import tornado, tornado.web#, tornado.autoreload
from common.web import template
log.debug('template:%s', config.template)
template.install(config.template)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        a = 1
#        self.write('jiong~')#template.render('jiong~~${a}', a))
        self.write(template.render('base.html'))

application = tornado.web.Application([
    # 主页
    (r'/', IndexHandler),


    # 其它
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path':config.static}),

], **config.settings)

def main():
    try:
        application.listen(config.port)
        log.debug('myblog start at:%d', config.port)
        instance = tornado.ioloop.IOLoop.instance()
        instance.start()
        log.info('tornado start at port:%d'%(config.port))
    except Exception, e:
        log.debug('wrong......')

if __name__ == '__main__':
    main()












