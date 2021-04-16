# -*- coding: utf-8 -*-

import random
import time
import tornado.ioloop
import tornado.web
import tornado.gen


class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('ok')


class AsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.sleep(10)
        self.finish('ok')


class SyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        time.sleep(10)
        self.finish('ok')


class KeepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        count = 1
        while True:
            yield tornado.gen.sleep(5)
            self.write('CURRENT:' + str(count))
            count += 1
            self.flush()
            if count == 5:
                break
        self.finish()


class HutHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        hut = '''
= COMPONENT -> Series ~ data: ^data
= DATA -> csv #data
日期 | 值'''

        data = []
        count = 0
        while True:
            yield tornado.gen.sleep(0.2)
            count += 1
            data.append('%s | %s' % (count, random.randint(100, 1000)))

            pre = 'window.DATA = `%s`' % (hut + '\n' + '\n'.join(data[-50:]))
            s = 'parent.postMessage(window.DATA, "*");'
            s = '<script>%s;%s</script>' % (pre, s)
            self.write(s)
            self.flush()
        self.finish()



MAP = [
    ('/', DemoHandler),
    ('/async', AsyncHandler),
    ('/sync', SyncHandler),
    ('/keep', KeepHandler),
    ('/hut', HutHandler),
]

if __name__ == '__main__':
    app = tornado.web.Application(MAP)
    app.listen(8888)
    print('server is starting on 8888 ...')
    tornado.ioloop.IOLoop.current().start()

