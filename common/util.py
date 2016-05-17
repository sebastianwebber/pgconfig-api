import tornado.web
import parameter
import json

class DefaultRequestHandler(tornado.web.RequestHandler):	
	
	def initialize(self):
		self.default_format = self.get_argument("format", "json", True)
		self.pg_version = self.get_argument("pg_version", 9.5, True)
	
	def write_plain(self, message=list()):
		if len(message) == 1:
			self.write(message[0])
		else:
			for line in message:
				self.write(line + '\n')
	
	def write_bash(self, message=list()):
		bash_script = """
#!/bin/bash

"""
		self.write(bash_script)

		if len(message) == 1:
			self.write('SQL_QUERY="{}"\n'.format(message[0]))
			self.write('psql -c "${SQL_QUERY}"\n')
		else:
			for line in message:
				self.write('SQL_QUERY="{}"\n'.format(line))
				self.write('psql -c "${SQL_QUERY}"\n\n')


	def write_json_api(self, message):
		self.set_header('Content-Type', 'application/vnd.api+json')
		
		_document = {}
		
		_document["data"] = message
		
		_meta = {}
		_meta["copyright"] = "PGConfig API"
		# _meta["authors"] = ("Sebastian Webber",)
		_document["meta"] = _meta
		
		_document["jsonapi"] = { "version" : "1.0"}
		
		full_url = self.request.protocol + "://" + self.request.host + self.request.uri 
		_document["links"] = { "self" : full_url}
		
		self.write( json.dumps(_document, sort_keys = True,separators=(',', ': ')))

	def write_json(self, message=list()):
		self.set_header('Content-Type', 'application/json')
		
		if len(message) == 1:
			self.write("{ \"output\": \"" + message[0] + "\"}")
		else:
			new_output = "{ \"output\": ["

			first_line = True

			for line in message:
				if not first_line:
					new_output += ","
				else: 
					first_line = False

				new_output += "\"{}\"".format(line)

			new_output += "] } "

			self.write(new_output)

	def return_output(self, message=list()):
		# default_format=self.get_argument("format", "json", True)

		# converting string input into a list (for solve issue with multiline strings)
		process_data = []
		if not isinstance(message, list):
			process_data.insert(0, message)
		else:
			process_data = message

		if self.default_format == "json":
			self.write_json_api(message)	
		elif self.default_format == "bash":
			self.write_bash(message)
		else:
			self.write_plain(message)
	

class GeneratorRequestHandler(DefaultRequestHandler):
	pass
	