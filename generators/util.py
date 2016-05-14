import tornado.web

class CustomRequestHandler(tornado.web.RequestHandler):
	def return_output(self, message=None):
		default_format=self.get_argument("format", "json", True)

		if default_format == "json":
			self.set_header('Content-Type', 'application/json')
			self.write("{ \"output\": \"" + message + "\"}")
		else:
			self.write(message)