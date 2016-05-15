#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web

from generators import fdw

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True
    ,"autoreload" : True
}

application = tornado.web.Application([
	(r"/", IndexHandler),
    (r"/fdw/([^/]+)", fdw.FDWHandler),
], **settings)

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.current().start()