import unittest
import tornado.testing
import tests.base


class TuningGetConfigTestCase(tests.base.DefaultTestCase):
    def test_WEB_91_json(self):
        self.run_test('json', 'WEB', '9.1')

    def test_WEB_92_json(self):
        self.run_test('json', 'WEB', '9.2')

    def test_WEB_93_json(self):
        self.run_test('json', 'WEB', '9.3')

    def test_WEB_94_json(self):
        self.run_test('json', 'WEB', '9.4')

    def test_WEB_95_json(self):
        self.run_test('json', 'WEB', '9.5')

    def test_OLTP_91_json(self):
        self.run_test('json', 'OLTP', '9.1')

    def test_OLTP_92_json(self):
        self.run_test('json', 'OLTP', '9.2')

    def test_OLTP_93_json(self):
        self.run_test('json', 'OLTP', '9.3')

    def test_OLTP_94_json(self):
        self.run_test('json', 'OLTP', '9.4')

    def test_OLTP_95_json(self):
        self.run_test('json', 'OLTP', '9.5')

    def test_DW_91_json(self):
        self.run_test('json', 'DW', '9.1')

    def test_DW_92_json(self):
        self.run_test('json', 'DW', '9.2')

    def test_DW_93_json(self):
        self.run_test('json', 'DW', '9.3')

    def test_DW_94_json(self):
        self.run_test('json', 'DW', '9.4')

    def test_DW_95_json(self):
        self.run_test('json', 'DW', '9.5')

    def test_Mixed_91_json(self):
        self.run_test('json', 'Mixed', '9.1')

    def test_Mixed_92_json(self):
        self.run_test('json', 'Mixed', '9.2')

    def test_Mixed_93_json(self):
        self.run_test('json', 'Mixed', '9.3')

    def test_Mixed_94_json(self):
        self.run_test('json', 'Mixed', '9.4')

    def test_Mixed_95_json(self):
        self.run_test('json', 'Mixed', '9.5')

    def test_Desktop_91_json(self):
        self.run_test('json', 'Desktop', '9.1')

    def test_Desktop_92_json(self):
        self.run_test('json', 'Desktop', '9.2')

    def test_Desktop_93_json(self):
        self.run_test('json', 'Desktop', '9.3')

    def test_Desktop_94_json(self):
        self.run_test('json', 'Desktop', '9.4')

    def test_Desktop_95_json(self):
        self.run_test('json', 'Desktop', '9.5')

    def test_WEB_91_conf(self):
        self.run_test('conf', 'WEB', '9.1')

    def test_WEB_92_conf(self):
        self.run_test('conf', 'WEB', '9.2')

    def test_WEB_93_conf(self):
        self.run_test('conf', 'WEB', '9.3')

    def test_WEB_94_conf(self):
        self.run_test('conf', 'WEB', '9.4')

    def test_WEB_95_conf(self):
        self.run_test('conf', 'WEB', '9.5')

    def test_OLTP_91_conf(self):
        self.run_test('conf', 'OLTP', '9.1')

    def test_OLTP_92_conf(self):
        self.run_test('conf', 'OLTP', '9.2')

    def test_OLTP_93_conf(self):
        self.run_test('conf', 'OLTP', '9.3')

    def test_OLTP_94_conf(self):
        self.run_test('conf', 'OLTP', '9.4')

    def test_OLTP_95_conf(self):
        self.run_test('conf', 'OLTP', '9.5')

    def test_DW_91_conf(self):
        self.run_test('conf', 'DW', '9.1')

    def test_DW_92_conf(self):
        self.run_test('conf', 'DW', '9.2')

    def test_DW_93_conf(self):
        self.run_test('conf', 'DW', '9.3')

    def test_DW_94_conf(self):
        self.run_test('conf', 'DW', '9.4')

    def test_DW_95_conf(self):
        self.run_test('conf', 'DW', '9.5')

    def test_Mixed_91_conf(self):
        self.run_test('conf', 'Mixed', '9.1')

    def test_Mixed_92_conf(self):
        self.run_test('conf', 'Mixed', '9.2')

    def test_Mixed_93_conf(self):
        self.run_test('conf', 'Mixed', '9.3')

    def test_Mixed_94_conf(self):
        self.run_test('conf', 'Mixed', '9.4')

    def test_Mixed_95_conf(self):
        self.run_test('conf', 'Mixed', '9.5')

    def test_Desktop_91_conf(self):
        self.run_test('conf', 'Desktop', '9.1')

    def test_Desktop_92_conf(self):
        self.run_test('conf', 'Desktop', '9.2')

    def test_Desktop_93_conf(self):
        self.run_test('conf', 'Desktop', '9.3')

    def test_Desktop_94_conf(self):
        self.run_test('conf', 'Desktop', '9.4')

    def test_Desktop_95_conf(self):
        self.run_test('conf', 'Desktop', '9.5')

    def test_WEB_91_alter_system(self):
        self.run_test('alter_system', 'WEB', '9.1')

    def test_WEB_92_alter_system(self):
        self.run_test('alter_system', 'WEB', '9.2')

    def test_WEB_93_alter_system(self):
        self.run_test('alter_system', 'WEB', '9.3')

    def test_WEB_94_alter_system(self):
        self.run_test('alter_system', 'WEB', '9.4')

    def test_WEB_95_alter_system(self):
        self.run_test('alter_system', 'WEB', '9.5')

    def test_OLTP_91_alter_system(self):
        self.run_test('alter_system', 'OLTP', '9.1')

    def test_OLTP_92_alter_system(self):
        self.run_test('alter_system', 'OLTP', '9.2')

    def test_OLTP_93_alter_system(self):
        self.run_test('alter_system', 'OLTP', '9.3')

    def test_OLTP_94_alter_system(self):
        self.run_test('alter_system', 'OLTP', '9.4')

    def test_OLTP_95_alter_system(self):
        self.run_test('alter_system', 'OLTP', '9.5')

    def test_DW_91_alter_system(self):
        self.run_test('alter_system', 'DW', '9.1')

    def test_DW_92_alter_system(self):
        self.run_test('alter_system', 'DW', '9.2')

    def test_DW_93_alter_system(self):
        self.run_test('alter_system', 'DW', '9.3')

    def test_DW_94_alter_system(self):
        self.run_test('alter_system', 'DW', '9.4')

    def test_DW_95_alter_system(self):
        self.run_test('alter_system', 'DW', '9.5')

    def test_Mixed_91_alter_system(self):
        self.run_test('alter_system', 'Mixed', '9.1')

    def test_Mixed_92_alter_system(self):
        self.run_test('alter_system', 'Mixed', '9.2')

    def test_Mixed_93_alter_system(self):
        self.run_test('alter_system', 'Mixed', '9.3')

    def test_Mixed_94_alter_system(self):
        self.run_test('alter_system', 'Mixed', '9.4')

    def test_Mixed_95_alter_system(self):
        self.run_test('alter_system', 'Mixed', '9.5')

    def test_Desktop_91_alter_system(self):
        self.run_test('alter_system', 'Desktop', '9.1')

    def test_Desktop_92_alter_system(self):
        self.run_test('alter_system', 'Desktop', '9.2')

    def test_Desktop_93_alter_system(self):
        self.run_test('alter_system', 'Desktop', '9.3')

    def test_Desktop_94_alter_system(self):
        self.run_test('alter_system', 'Desktop', '9.4')

    def test_Desktop_95_alter_system(self):
        self.run_test('alter_system', 'Desktop', '9.5')

    def run_test(self, format_name, enviroment_name, pg_version):
        test_url = "/v1/tuning/get-config?env_name={}&format={}&max_connections=150&pg_version={}&total_ram=10GB".format(
            enviroment_name, format_name, pg_version)

        test_filename = "tests/advisors/espected/{}_{}.{}".format(
            enviroment_name, pg_version, format_name)

        test_file = open(test_filename, 'r')
        expected_test_result = ''

        for line in test_file.readlines():
            expected_test_result += line

        test_file.close()

        response = self.fetch(test_url)
        self.assertEqual(response.code, 200)

        diff = '\n'
        diff += self.unidiff_output(response.body.strip(),
                                    expected_test_result.strip())
        self.assertEqual(response.body.strip(), expected_test_result.strip(),
                         diff)
