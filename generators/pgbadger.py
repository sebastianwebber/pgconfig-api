import tornado.web

from common import ParameterFormat, util


class PGBadgerConfigurationHandler(util.GeneratorRequestHandler):

    """
    Implements a PGBadger Configuration Generator
    """

    def get_config(self):

        return_data = list()
        category = {}
        category["category"] = "log_config"
        category["description"] = "Logging configuration for pgbadger"
        category["parameters"] = list()


        ## logging_collector
        parameter = {}
        parameter["name"] = "logging_collector"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_checkpoints
        parameter = {}
        parameter["name"] = "log_checkpoints"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_connections
        parameter = {}
        parameter["name"] = "log_connections"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_connections
        parameter = {}
        parameter["name"] = "log_connections"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_disconnections
        parameter = {}
        parameter["name"] = "log_disconnections"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_lock_waits
        parameter = {}
        parameter["name"] = "log_lock_waits"
        parameter["config_value"] = "on"
        category["parameters"].append(parameter)

        ## log_temp_files
        parameter = {}
        parameter["name"] = "log_temp_files"
        parameter["config_value"] = "0"
        category["parameters"].append(parameter)


        ## lc_messages
        parameter = {}
        parameter["name"] = "lc_messages"
        parameter["config_value"] = "C"
        parameter["format"] = ParameterFormat.String
        category["parameters"].append(parameter)

        ## log_min_duration_statement
        parameter = {}
        parameter["name"] = "log_min_duration_statement"
        parameter["config_value"] = "10s"
        parameter["format"] = ParameterFormat.Time
        parameter["comment"] = "Adjust the minimum time to collect data"
        category["parameters"].append(parameter)
        
        ## log_autovacuum_min_duration
        parameter = {}
        parameter["name"] = "log_autovacuum_min_duration"
        parameter["config_value"] = "0"

        category["parameters"].append(parameter)

        return_data.append(category)


        category = {}
        category["category"] = "{}_config".format(self.log_format)
        category["description"] = "'{}' format configuration".format(self.log_format)
        category["parameters"] = list()

        if self.log_format == "stderr":
            ## log_destination
            parameter = {}
            parameter["name"] = "log_destination"
            parameter["config_value"] = self.log_format
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)

            ## log_line_preffix
            parameter = {}
            parameter["name"] = "log_line_preffix"
            parameter["config_value"] = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)

        elif self.log_format == "syslog":
            ## log_destination
            parameter = {}
            parameter["name"] = "log_destination"
            parameter["config_value"] = self.log_format
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)

            ## log_line_prefix
            parameter = {}
            parameter["name"] = "log_line_prefix"
            parameter["config_value"] = "user=%u,db=%d,app=%a,client=%h "
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)

            ## syslog_facility
            parameter = {}
            parameter["name"] = "syslog_facility"
            parameter["config_value"] = "LOCAL0"
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)

            ## syslog_ident
            parameter = {}
            parameter["name"] = "syslog_ident"
            parameter["config_value"] = "postgres"
            parameter["format"] = ParameterFormat.String
            category["parameters"].append(parameter)



        elif self.log_format == "csvlog":
            ## log_destination
            parameter = {}
            parameter["name"] = "log_destination"
            parameter["config_value"] = self.log_format
            category["parameters"].append(parameter)

        return_data.append(category)

        self.return_output(return_data)

    def get(self, slug=None):
        
        self.log_format = self.get_argument("log_format", "stderr", True)

        if slug == "get-config":
            self.get_config()
        else:
            raise tornado.web.HTTPError(404)
