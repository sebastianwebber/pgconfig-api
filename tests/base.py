import main
import tornado.testing
import tornado.ioloop
import tornado.web


class DefaultTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = main.MainAPI()
        return app.get_app()
