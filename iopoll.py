# -*- coding: utf-8 -*-

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


MAP = [
    ('/', DemoHandler),
    ('/async', AsyncHandler),
    ('/sync', SyncHandler),
    ('/keep', KeepHandler),
]

if __name__ == '__main__':
    app = tornado.web.Application(MAP)
    app.listen(8888)
    print('server is starting on 8888 ...')
    tornado.ioloop.IOLoop.current().start()

