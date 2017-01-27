#!/usr/bin/env python

import tornado.wsgi
import tornado.web

import wsgiref.simple_server
from main import MainAPI


if __name__ == "__main__":
    apiApp = MainAPI()
    wsgi_app = tornado.wsgi.WSGIAdapter(apiApp.application)
    server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
    server.serve_forever()
