#!/usr/bin/env python

import tornado.ioloop
import tornado.web

from generators import fdw

settings = {
    # "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    # "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "debug" : True
    # ,"autoreload" : True
}

application = tornado.web.Application([
    (r"/fdw/([^/]+)", fdw.FDWHandler),
], **settings)

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.current().start()