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

		:param server_name: FDW Server Name
		:param host: Remote server address (IP or DNS name)
		:param db_type: Database Type Name (PostgreSQL, MySQL, etc)
		:param port: Remote server port address

		"""

		target_server = self.get_argument("server_name", "target_server", True)
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


	def generate_user_mapping(self):
		"""
		**Generate the FDW user mapping**


		Returns
			SQL command with the ``CREATE USER MAPPING`` statement
		Sample URL
			::

				/fdw/generate-user-mapping?pg_user=dev_user&server_name=dev_server&remote_user=root&remote_password=install123&format=sql
		::

		Sample output
			::

				CREATE USER MAPPING FOR dev_user FOREIGN DATA WRAPPER target_server OPTIONS (username 'root', password 'install123');
			::

		:param pg_user: PostgreSQL User to map remote FDW connection
		:param server_name: FDW server same
		:param remote_user: Remote server user
		:param remote_password: Remote server password

		"""
		pg_user = self.get_argument("pg_user", "postgres", True)
		server_name = self.get_argument("server_name", "target_server", True)
		remote_user = self.get_argument("remote_user", "postgres", True)
		remote_password = self.get_argument("remote_password", "postgres123", True)

		sql_output = ""
		sql_output += "CREATE USER MAPPING FOR {} ".format(pg_user)
		sql_output += "FOREIGN DATA WRAPPER {} ".format(server_name)
		sql_output += "OPTIONS (username '{}', password '{}');".format(remote_user, remote_password)

		self.return_output(sql_output)

	def get(self, slug=None):		
		if slug == "generate-connection":
			self.generate_connection()
		elif slug == "generate-user-mapping":
			self.generate_user_mapping()
		else:
			raise tornado.web.HTTPError(404)