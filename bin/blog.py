#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import chardet
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

    def get_articlelist(self, page=1, num=0):
        '''
        默认page为1，num为0；
        后者特指不进行分页，将所有文章列在同一页上
        '''
        articlelist = []
        dirlist = os.listdir(config.article)
        log.debug('dirlist=%s'%(dirlist))
        for c in dirlist:
            if not os.path.isfile(os.path.join(config.article, c)):
                continue
            if c.startswith('.'):
                continue
            d = chardet.detect(c)
            e = c.decode(d['encoding'])
            try:
                tmp = e.split('_')
                tmpdict = {}
                tmpdict['time']  = u'%s年%s月%s日'%(tmp[0], tmp[1], tmp[2])
                tmpdict['name']  = tmp[3]
                tmpdict['title'] = tmp[4][:-5]
                tmpdict['a']     = '/article/%s/%s/%s/%s.html'%(tmp[0], tmp[1], tmp[2], tmp[3])
                print 'a = %s'%(tmpdict['a'])
                print 'e = %s'%(e)
                articlelist.append(tmpdict)
            except:
                pass
        
        result = {}
        tmplen = articlelist.__len__()
        if num == 0:
            result['page']          = 1
            result['pagenum']       = 1
            result['listnum']       = tmplen
            result['articlelist']   = articlelist
        else:
            result['page']          = page
            result['pagenum']       = tmplen / num + 1 if tmplen % num else 0
            if page < result['pagenum'] or page == result['pagenum'] and not tmplen % num:
                result['listnum']   = num
            else:
                result['listnum']   = tmplen % num
            if result['page'] == result['pagenum']:
                start = (result['page'] - 1) * num
                result['articlelist'] = articlelist[start :]
            else:
                start = (result['page'] - 1) * num
                end   = start + num
                result['articlelist'] = articlelist[start : end]

        return result
            
                

    def get_articlelist_withpage(self, page=1, num=12):
        '''
        配合get_articlelist完成分页；
        page代表第几页，num代表每页文章数量
        '''
        page = int(self.get_argument('page', '1'))
        result = self.get_articlelist(page, num)
        return result


    def get(self):
        result = self.get_articlelist_withpage()
        log.debug('result = %s'%(result))
        self.write(template('index.html', result=result))        # 这个地方不能传page=page，应该是被html里面的name="page"覆盖了



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

        log.debug('aarticlearticlearticlearticlearticlearticlerticle')
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












