#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web
from generators import fdw, pgbadger
from guides import native_replication
from advisors import tuning


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MainAPI():

    def __init__(self):
        self.settings = {
            "template_path":
            os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "debug": True,
            "autoreload": True
        }

        API_VERSION = 1.0
        API_PREFIX = "/v1/"

        self.application = tornado.web.Application([
            (r"/", tornado.web.RedirectHandler, {"url": "/v1"}),
            (r"/v1", IndexHandler),

            ## Generators
            (r"/v1/generators/fdw/([^/]+)", fdw.FDWHandler),
            (r"/v1/generators/pgbadger/([^/]+)", pgbadger.PGBadgerConfigurationHandler),

            ## Guides
            (r"/v1/guides/native-replication/([^/]+)", native_replication.NativeReplicationHandler),

            ## Tuning
            (r"/v1/tuning/([^/]+)", tuning.TuningHandler),
        ], **self.settings)

    def get_app(self):
        return self.application


if __name__ == "__main__":
    apiApp = MainAPI()
    apiApp.application.listen(5000)
    tornado.ioloop.IOLoop.current().start()
