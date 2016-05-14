import tornado.web
import util

class FDWHandler(util.CustomRequestHandler):
	"""Foreign Data Wrapper Generator"""

	def generate_connection(self):
		"""
		**Generate the FDW connection**


		Returns
			SQL command with the ``CREATE SERVER`` statement
		Sample URL
			::

				/fdw/generate-connection?server-name=dev_server&host=128.3.0.100&db_type=MySQL&port=3306&format=sql
		::

		Sample output
			::

				CREATE SERVER dev_server FOREIGN DATA WRAPPER mysql_fdw OPTIONS (host '128.3.0.100', port '3306');
			::

		:param server-name: FDW Server Name
		:param host: Remote server address (IP or DNS name)
		:param db_type: Database Type Name (eg. PostgreSQL, MySQL, etc)
		:param port: Remote server port address

		"""

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