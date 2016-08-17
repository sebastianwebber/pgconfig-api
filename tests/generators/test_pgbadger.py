import unittest
import tornado.testing
import tests.base
from generators import pgbadger


class PGBadgerTestCase(tests.base.DefaultTestCase):
    def initialize(self):
        super(PGBadgerTestCase, self).initialize()
        self.target_url = '/v1/generators/pgbadger/get-config'

    def test_getconfig_conf(self):

        response = self.fetch('/v1')

        # self.http_client.fetch(
        #     self.get_url('/v1/generators/pgbadger/get-config'), self.stop)
        # response = self.wait()

        self.assertEqual(response.code, 200)

# self.client.fetch('/v1/generators/pgbadger/get-config?format=conf',
#                   self.stop)
# response = self.wait()
# self.assertEqual(response.code, 200)
# self.assertTrue(
#     response.headers['Location'].endswith('/tutorial'),
#     "response.headers['Location'] did not ends with /tutorial")
