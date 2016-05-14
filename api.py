#!/usr/bin/env python

import tornado.ioloop
import tornado.web

from generators import fdw


application = tornado.web.Application([
    (r"/fdw/([^/]+)", fdw.FDWHandler),
], 
debug = True, 
autoreload = True)

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.current().start()