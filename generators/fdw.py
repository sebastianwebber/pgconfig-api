import tornado.web
import util

class FDWHandler(util.CustomRequestHandler):

	def _generate_connection(self):
		target_server = self.get_argument("server-name", "target_server", True)
		target_host = self.get_argument("host", "localhost", True)
		target_db = self.get_argument("db_type", "PostgreSQL", True)
		target_port = self.get_argument("port", 5432, True)

		target_fdw = "postgres_fdw"
		
		if target_db == "MySQL":
			target_fdw = "mysql_fdw"


		sql_output = ""
		sql_output += "CREATE SERVER {} ".format(target_server)
		sql_output += "FOREIGN DATA WRAPPER {} ".format(target_fdw)
		sql_output += "OPTIONS (host '{}', port '{}');".format(target_host, target_port)

		self.return_output(sql_output)

	def get(self, slug=None):		
		if slug == "generate-connection":
			self._generate_connection()
		else:
			raise tornado.web.HTTPError(404)