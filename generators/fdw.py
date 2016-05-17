import tornado.web
from common import util

class FDWHandler(util.GeneratorRequestHandler):
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

	def import_foreign_schema(self):
		"""
		**Import foreign schema**

		.. warning:: ``IMPORT FOREIGN SCHEMA`` it's only supported on the 9.5 or greater


		Returns
			SQL command with the ``IMPORT FOREIGN SCHEMA`` statement
		Sample URL
			::

				/fdw/import-foreign-schema?remote_schema=sales_schema&server_name=dev_server&schema_name=dev_sales_remote&only_tables=customer,sales&create_schema=true
		::

		Sample output
			::

				CREATE SCHEMA IF NOT EXISTS dev_sales_remote; 
				IMPORT FOREIGN SCHEMA sales_schema LIMIT TO (customer, sales) FROM SERVER dev_server INTO dev_sales_remote; 
			::
			
		:param remote_schema: Remote schema name
		:param server_name: FDW Server name
		:param schema_name: Local schema name
		:param only_tables: list of tables to import (comma separated - no spaces)
		:param except_tables: list of tables to EXCLUDE from import (comma separated - no spaces)
		:param create_schema: Generates de statement from ``CREATE SCHEMA``

		"""

		pg_version = float(self.get_argument("pg_version", 9.5, True))
		remote_schema = self.get_argument("remote_schema", "remote_schema", True)
		server_name = self.get_argument("server_name", "target_server", True)
		schema_name = self.get_argument("schema_name", "remote_db", True)
		only_tables = self.get_argument("only_tables", "table1,table2", True)
		except_tables = self.get_argument("except_tables", "table1,table2", True)
		create_schema = self.get_argument("create_schema", False, True)

		sql_output = []

		if pg_version >= 9.5:

			if pg_version >= 9.3 and create_schema:
				sql_output.append("CREATE SCHEMA IF NOT EXISTS {};".format(schema_name))


			sql_line = ""
			sql_line += "IMPORT FOREIGN SCHEMA {} ".format(remote_schema)

			if only_tables != "table1,table2":
				sql_line += "LIMIT TO ({}) ".format(', '.join(only_tables.split(',')))

			if except_tables != "table1,table2":
				sql_line += "EXCEPT ({}) ".format(', '.join(only_tables.split(',')))

			sql_line += "FROM SERVER {} ".format(server_name)
			sql_line += "INTO {};".format(schema_name)
			sql_output.append(sql_line)
		else:
			sql_output.append("-- IMPORT FOREIGN SCHEMA it's only supported on the 9.5 or greater")

		self.return_output(sql_output)


	def get(self, slug=None):		
		if slug == "generate-connection":
			self.generate_connection()
		elif slug == "generate-user-mapping":
			self.generate_user_mapping()
		elif slug == "import-foreign-schema":
			self.import_foreign_schema()
		else:
			raise tornado.web.HTTPError(404)