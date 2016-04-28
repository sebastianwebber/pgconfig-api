#!/usr/bin/env python

from flask import Flask

from flask_ripozo import FlaskDispatcher

from ripozo.decorators import apimethod
from ripozo.adapters import SirenAdapter, HalAdapter
from ripozo.resources import ResourceBase

import logging


class FDWGeneratorViewSet(ResourceBase):
	resource_name = 'FDW'

	@apimethod(methods=['GET'],route='/generate_connection')
	def generate_connection(cls, request, *args, **kwargs):


		if "db_type" in request.query_args:
			target_db = request.query_args['db_type'][0]
		else:
			raise Exception("Mandatory field db_type")


		### DEFAULTS:
		target_host = "localhost"
		target_server = "remote_server"


		target_fdw="postgres_fdw"
		target_port=5432
		if target_db == "MySQL":
			target_fdw = "mysql_fdw"
			target_port = 3306

		#### END OF

		if "host" in request.query_args:
			target_host   = request.query_args['host'][0]

		if "port" in request.query_args:
			target_port   = request.query_args['port'][0]

		if "server_name" in request.query_args:
			target_server   = request.query_args['server_name'][0]

		sql_output  = """CREATE SERVER {}
FOREIGN DATA WRAPPER {}
OPTIONS (host '{}', port '{}');""".format(
				target_server, 
				target_fdw, 
				target_host,
				target_port
			)



		return cls(properties={'output': sql_output, 'args': request.query_args})


# Create the flask application
app = Flask(__name__)

app.debug = True


# Create the dispatcher
dispatcher = FlaskDispatcher(app, url_prefix='/v1')
dispatcher.register_adapters(SirenAdapter, HalAdapter)

dispatcher.register_resources(FDWGeneratorViewSet)

if __name__ == '__main__':
    app.run() # Run the app