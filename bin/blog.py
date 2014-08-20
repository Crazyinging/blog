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

article = template.install(config.article)
template = template.install(config.template)
#import traceback                   #看一下这个东西



class IndexHandler(tornado.web.RequestHandler):

    def get_articlelist(self):
        articlelist = []
        dirlist = os.listdir(config.article)
        log.debug('dirlist=%s'%(dirlist))
        for c in dirlist:
            if not os.path.isfile(os.path.join(config.article, c)):
                continue
            log.debug('c=%s'%(c))
            try:
                tmp = c.split('_')
                tmpdict = {}
                log.debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                tmpdict['time']  = u'%s年%s月%s日'%(tmp[0], tmp[1], tmp[2])
                log.debug('tmpdict["time"]=%s'%(tmpdict['time']))
                tmpdict['name']  = tmp[3]
                log.debug('tmpdict["name"]=%s'%(tmpdict['name']))
                tmpdict['title'] = tmp[4]
                log.debug('tmpdict["title"]=%s'%(tmpdict['title']))
                articlelist.append(tmpdict)
                log.debug('tmpdict=%s'%(tmpdict))
            except:
                pass

        return articlelist
                

    def get(self):
        articlelist = self.get_articlelist()
        log.debug('articlelist = %s'%(articlelist))
        self.write(template('index.html', articlelist=articlelist))



class BooksHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(template('books.html'))



class ArticleHandler(tornado.web.RequestHandler):

    def get_namepart(self):
        '''
        从url读取文章的时间和英文name
        '''
        queryurl = self.request.full_url()
        tmppart  = queryurl.split('/')
        if 'article' not in tmppart:
            log.debug('url error')
            raise

        tmpid = tmppart.index('article')
        if tmppart.__len__() - tmpid - 1 < 4:
            log.debug('url error')
            raise

        namepart = {}
        namepart['year']    = tmppart[tmpid + 1]
        namepart['month']   = tmppart[tmpid + 2]
        namepart['day']     = tmppart[tmpid + 3]
        namepart['name']    = tmppart[tmpid + 4][:-5]
        return namepart

    def get(self, tmp):

        try:
            namepart = self.get_namepart()
            tmpname  = '%s_%s_%s_%s'%(namepart['year'], namepart['month'], namepart['day'], namepart['name'])
            articlelist = os.listdir(config.article)
            for c in articlelist:
                if c.startswith(tmpname):
                    articleid = articlelist.index(c)
                    break
            self.write(article(articlelist[articleid]))
            log.debug('articlename = %s'%(articlelist[articleid]))

        except:
            log.debug('article not found')
            raise


application = tornado.web.Application([
    # 主页
    (r'/', IndexHandler),

    # 文章
    (r'/article/(.*)', ArticleHandler, {}),

    # 页首的6个选项
    (r'/books', BooksHandler),

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












