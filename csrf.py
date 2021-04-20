# -*- coding: utf-8 -*-

import random
import time
import tornado.ioloop
import tornado.web
import tornado.gen

import hashlib
import time


ACCOUNT = {
    'yszou': {
        'username': 'yszou', # 4b6c764cd04ad2ebf0a32e4655192f65
        'password': 'ccb93a5c372ece11bbdb4f391fafa7fe', #  md5(4b6c764cd04ad2ebf0a32e4655192f65+123)
        'key': '123!@#$%^',
        'value': '1',
    }
}



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        value = self.get_cookie('APP')
        v, sign = value.split('-')
        username = v.split('|')[0]
        account = ACCOUNT.get(username)
        if not account:
            return None
        key = account['key']
        p = hashlib.md5((key + v).encode('utf-8')).hexdigest()
        if p == sign:
            obj = account.copy()
            del obj['key']
            return obj
        return None


class LoginHandler(BaseHandler):
    def get(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        salt = self.get_argument('salt', '')

        account = ACCOUNT.get(username, None)
        if not account:
            self.finish({'code': 1, 'msg': 'username错误'})
            return

        pa = hashlib.md5((salt + account['password']).encode('utf-8')).hexdigest()
        if pa != password:
            self.finish({'code': 2, 'msg': '密码错误'})
            return

        now = str(int(time.time()))
        seed = hashlib.md5(now.encode('utf-8')).hexdigest()[:8]
        cookie = '%s|%s|%s' % (username, now, seed)
        sign = hashlib.md5((account['key'] + cookie).encode('utf-8')).hexdigest()
        cookie += ('-' + sign)
        self.set_cookie('APP', cookie, httponly=True)
        self.finish({'code': 0})


class IndexHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            self.finish({'code': 1, 'msg': 'login require'})
            return

        self.finish({'code': 0, 'data': user})
        return


class UpdateHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            self.finish({'code': 1, 'msg': 'login require'})
            return

        value = self.get_argument('value', '')
        if value:
            ACCOUNT[user['username']]['value'] = value

        user = self.get_current_user()
        self.finish({'code': 0, 'data': user})



MAP = [
    ('/login', LoginHandler),
    ('/', IndexHandler),
    ('/update', UpdateHandler),
]

if __name__ == '__main__':
    app = tornado.web.Application(MAP)
    app.listen(8888)
    print('server is starting on 8888 ...')
    tornado.ioloop.IOLoop.current().start()

