import imp
import tornado.testing


class DefaultTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = imp.load_source('application', 'main.py')
        return app
