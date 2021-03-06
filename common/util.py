import tornado.web
import json
from tornado_cors import CorsMixin
from common import ParameterFormat, EnumEncoder


class DefaultRequestHandler(CorsMixin, tornado.web.RequestHandler):

    CORS_ORIGIN = '*'

    def initialize(self):
        self.default_format = self.get_argument("format", "json", True)
        self.show_about = self.get_argument("show_about", True, True)
        self.pg_version = self.get_argument("pg_version", 9.6, True)
        self.version = "2.0 beta"

    def write_about_stuff(self, format_type="alter_system"):
        default_comment = "--"

        if format_type == "conf":
            default_comment = "#"

        self.write("{} Generated by PGConfig {}\n".format(default_comment,
                                                          self.version))
        self.write("{} http://pgconfig.org\n\n".format(default_comment * 2))

    def write_comment(self, format_type, comment):
        default_comment = "--"

        if format_type == "conf":
            default_comment = "#"

        if comment != "NONE":
            self.write("\n{} {}\n".format(default_comment, comment))

    def write_config(self, output_data):

        if self.show_about is True:
            self.write_about_stuff("conf")

        for category in output_data:
            self.write("# {}\n".format(category["description"]))
            for parameter in category["parameters"]:
                config_value = parameter.get("config_value", "NI")
                value_format = parameter.get("format", ParameterFormat.NONE)

                if value_format in (ParameterFormat.String,
                                    ParameterFormat.Time):
                    config_value = "'{}'".format(config_value)

                parameter_comment = parameter.get("comment", "NONE")

                if parameter_comment != "NONE":
                    self.write_comment("conf", parameter_comment)

                self.write("{} = {}\n".format(parameter["name"], config_value))

            self.write("\n")

    def write_alter_system(self, output_data):
        
        if float(self.pg_version) <= 9.3:
            self.write("-- ALTER SYSTEM format it's only supported on version 9.4 and higher. Use 'conf' format instead.")
        else:
            if self.show_about is True:
                self.write_about_stuff()

            for category in output_data:
                self.write("-- {}\n".format(category["description"]))
                for parameter in category["parameters"]:
                    config_value = parameter.get("config_value", "NI")

                    parameter_comment = parameter.get("comment", "NONE")
                    self.write_comment("alter_system", parameter_comment)

                    self.write("ALTER SYSTEM SET {} TO '{}';\n".format(parameter[
                        "name"], config_value))
                self.write("\n")

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
        _meta["version"] = self.version
        _meta["arguments"] = self.request.arguments
        _document["meta"] = _meta

        _document["jsonapi"] = {"version": "1.0"}

        full_url = self.request.protocol + "://" + self.request.host + self.request.uri
        _document["links"] = {"self": full_url}

        self.write(
            json.dumps(
                _document,
                sort_keys=True,
                separators=(',', ': '),
                cls=EnumEncoder))

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
        elif self.default_format == "conf":
            self.write_config(message)
        elif self.default_format == "alter_system":
                self.write_alter_system(message)
        else:
            self.write_plain(message)


class GeneratorRequestHandler(DefaultRequestHandler):
    pass
