#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web

from generators import fdw, native_replication, pgbadger
from advisors import tuning

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True
    ,"autoreload" : True
}

API_VERSION=1.0
API_PREFIX="/v1/"

application = tornado.web.Application([
    (r"/", tornado.web.RedirectHandler, {"url": "/v1"}),
	(r"/v1", IndexHandler),
    (r"/v1/generators/fdw/([^/]+)", fdw.FDWHandler),
    (r"/v1/generators/pgbadger/([^/]+)", pgbadger.PGBadgerConfigurationHandler),
    (r"/v1/generators/native-replication/([^/]+)", native_replication.NativeReplicationHandler),
    (r"/v1/tuning/([^/]+)", tuning.TuningHandler),
], **settings)

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.current().start()