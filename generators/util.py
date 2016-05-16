import tornado.web

class CustomRequestHandler(tornado.web.RequestHandler):
	def return_output(self, message=list()):
		default_format=self.get_argument("format", "json", True)

		# print message
		# converting string input into a list (for solve issue with multiline strings)
		process_data = []
		if not isinstance(message, list):
			process_data.insert(0, message)
		else:
			process_data = message

		if default_format == "json":
			self.set_header('Content-Type', 'application/json')

			if len(process_data) == 1:
				self.write("{ \"output\": \"" + process_data[0] + "\"}")
			else:
				new_output = "{ \"output\": ["

				first_line = True

				for line in process_data:
					if not first_line:
						new_output += ","
					else: 
						first_line = False

					new_output += "\"{}\"".format(line)

				new_output += "] } "

				self.write(new_output)
			
		if default_format == "bash":

			bash_script = """
#!/bin/bash

"""
			self.write(bash_script)

			if len(process_data) == 1:
				self.write('SQL_QUERY="{}"\n'.format(process_data[0]))
				self.write('psql -c "${SQL_QUERY}"\n')
			else:
				for line in process_data:
					self.write('SQL_QUERY="{}"\n'.format(line))
					self.write('psql -c "${SQL_QUERY}"\n\n')

		else:
			if len(process_data) == 1:
				self.write(process_data[0])
			else:
				for line in process_data:
					self.write(line + '\n')