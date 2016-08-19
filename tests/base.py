import main
import tornado.testing
import tornado.ioloop
import tornado.web
import difflib


class DefaultTestCase(tornado.testing.AsyncHTTPTestCase):
    def unidiff_output(self, expected, actual):
        """
        Helper function. Returns a string containing the unified diff of two multiline strings.
        """
        expected = expected.splitlines(1)
        actual = actual.splitlines(1)

        diff = difflib.unified_diff(expected, actual)

        return ''.join(diff)

    def get_app(self):
        app = main.MainAPI()
        return app.get_app()
