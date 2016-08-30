# -*- coding: UTF-8 -*-

import tornado.web
import json
from common import util, bytes, ParameterFormat


class TuningHandler(util.DefaultRequestHandler):
    def initialize(self):
        super(TuningHandler, self).initialize()
        self.enviroment_name = self.get_argument("enviroment_name", "WEB",
                                                 True)
        self.show_doc = self.get_argument("show_doc", False, True)
        self.include_pgbadger = self.get_argument("include_pgbadger", None,
                                                  True)

    def get_all_environments(self):
        return ["WEB", "OLTP", "DW", "Mixed", "Desktop"]

    def list_enviroments(self):
        """
        **Get a list of the proposed environments**


        Returns
            list of proposed environments
        Sample URL
            ::

                /v1/tuning/list-enviroments
            ::

        Sample output
            ::

                {
                    "data": [
                        "WEB",
                        "OLTP",
                        "DW",
                        "Mixed",
                        "Desktop"
                    ],
                    "jsonapi": {
                        "version": "1.0"
                    },
                    "links": {
                        "self": "http://api.pgconfig.org/v1/tuning/list-enviroments"
                    },
                    "meta": {
                        "copyright": "PGConfig API",
                        "version": "1.0"
                    }
                }
            ::

        """
        self.write_json_api(self.get_all_environments())

    def _define_doc(self,
                    parameter_name,
                    doc_url,
                    abstract="",
                    default_value="",
                    recomendations={}):
        doc_stuff = {}
        doc_file_name = "pg_doc/{}/{}.txt".format(parameter_name,
                                                  self.pg_version)
        doc_stuff[
            "url"] = "http://www.postgresql.org/docs/{}/static/{}".format(
                self.pg_version, doc_url)

        # if parameter_name in [ "shared_buffers", "effective_cache_size", "work_mem" ]  :
        doc_file = open(doc_file_name, 'r')
        file_content = doc_file.readlines()
        doc_file.close()

        doc_stuff["type"] = file_content[0].split(' ')[1].replace(
            '(', '').replace(')', '').replace('\n', '')

        details = list()
        for line in file_content[1:]:
            if line != "\n":
                details.append(line.replace('\n', ''))

        doc_stuff["details"] = details

        if abstract != "":
            doc_stuff["abstract"] = abstract

        if abstract != "":
            doc_stuff["default_value"] = default_value

        if recomendations:
            doc_stuff["recomendations"] = recomendations

        return doc_stuff

    def _get_rules(self, enviroment_name):

        return_output = list()

        # ---> Memory Related
        category = {}
        category["category"] = "memory_related"
        category["description"] = "Memory Configuration"
        category["parameters"] = list()

        ## shared_buffers
        parameter = {}
        parameter["name"] = "shared_buffers"
        parameter["max_value"] = "8GB"
        parameter["format"] = ParameterFormat.Bytes

        recomendation_posts = {}
        recomendation_posts[
            "Tuning Your PostgreSQL Server"] = "https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server#shared_buffers"
        recomendation_posts[
            "Tuning shared_buffers and wal_buffers"] = "http://rhaas.blogspot.com.br/2012/03/tuning-sharedbuffers-and-walbuffers.html"

        abstract = "This parameter allocate memory slots, used by all process. Mainly works as the disk cache and its similar to oracle's SGA buffer."
        default_value = ""

        if float(self.pg_version) in (9.1, 9.2):
            default_value = "32MB"
        elif float(self.pg_version) >= 9.3:
            default_value = "128MB"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-resource.html#GUC-SHARED-BUFFERS", abstract,
            default_value, recomendation_posts)

        if enviroment_name == "Desktop":
            parameter["formula"] = "TOTAL_RAM / 16"
        else:
            parameter["formula"] = "TOTAL_RAM / 4"

        category["parameters"].append(parameter)

        ## effective_cache_size
        parameter = {}
        parameter["name"] = "effective_cache_size"
        parameter["format"] = ParameterFormat.Bytes

        abstract = "This parameter does not allocate any resource, just tells to the query planner how much of the operating system cache are avaliable to use. Remember that shared_buffers needs to smaller than 8GB, then the query planner will prefer read the disk because it will be on memory."
        default_value = ""

        if float(self.pg_version) in (9.1, 9.2):
            default_value = "128MB"
        elif float(self.pg_version) >= 9.4:
            default_value = "4GB"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE", abstract,
            default_value)

        if enviroment_name == "Desktop":
            parameter["formula"] = "TOTAL_RAM / 4"
        else:
            parameter["formula"] = "(TOTAL_RAM / 4) * 3"

        category["parameters"].append(parameter)

        ## work_mem
        parameter = {}
        parameter["name"] = "work_mem"
        parameter["min_value"] = "4MB"
        parameter["format"] = ParameterFormat.Bytes

        abstract = "This parameter defines how much a work_mem buffer can allocate. Each query can open many work_mem buffers when execute (normally one by subquery) if it uses any sort (or aggregate) operation. When work_mem its too small a temp file is created."
        default_value = ""

        if float(self.pg_version) >= 9.1 and float(self.pg_version) <= 9.3:
            default_value = "1MB"
        elif float(self.pg_version) >= 9.4:
            default_value = "4MB"

        recomendation_posts = {}
        recomendation_posts[
            "Understaning postgresql.conf: WORK_MEM"] = "https://www.depesz.com/2011/07/03/understanding-postgresql-conf-work_mem/"

        parameter["documentation"] = self._define_doc(
            parameter["name"], "runtime-config-resource.html#GUC-WORK-MEM",
            abstract, default_value, recomendation_posts)

        if enviroment_name in ["WEB", "OLTP"]:
            parameter["formula"] = "(TOTAL_RAM / MAX_CONNECTIONS)"
        elif enviroment_name in ["DW", "Mixed"]:
            parameter["formula"] = "((TOTAL_RAM / 2) / MAX_CONNECTIONS)"
        else:
            parameter["formula"] = "((TOTAL_RAM / 6) / MAX_CONNECTIONS)"

        category["parameters"].append(parameter)

        ## maintenance_work_mem
        parameter = {}
        parameter["name"] = "maintenance_work_mem"
        parameter["format"] = ParameterFormat.Bytes
        parameter["max_value"] = "2GB"

        abstract = "This parameter defines how much a maintenance operation (ALTER TABLE, VACUUM, REINDEX, AutoVACUUM worker, etc) buffer can use."
        default_value = ""

        if float(self.pg_version) >= 9.1 and float(self.pg_version) <= 9.3:
            default_value = "16MB"
        elif float(self.pg_version) >= 9.4:
            default_value = "64MB"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM", abstract,
            default_value)

        if enviroment_name in ["WEB", "OLTP"]:
            parameter["formula"] = "(TOTAL_RAM / 16)"
        elif enviroment_name == "DW":
            parameter["formula"] = "(TOTAL_RAM / 8)"
        else:
            parameter["formula"] = "(TOTAL_RAM / 16)"

        category["parameters"].append(parameter)

        return_output.append(category)

        ##### Checkpoint Related Configuration
        category = {}
        category["category"] = "checkpoint_related"
        category["description"] = "Checkpoint Related Configuration"
        category["parameters"] = list()

        ## checkpoint_segments
        if float(self.pg_version) >= 8.0 and float(self.pg_version) <= 9.4:
            parameter = {}
            parameter["name"] = "checkpoint_segments"
            # parameter["min_version"] = 8.0
            # parameter["max_version"] = 9.4
            parameter["format"] = ParameterFormat.Decimal

            recomendation_posts = {}
            recomendation_posts[
                "WRITE AHEAD LOG + UNDERSTANDING POSTGRESQL.CONF: CHECKPOINT_SEGMENTS, CHECKPOINT_TIMEOUT and CHECKPOINT_WARNING"] = "https://www.depesz.com/2011/07/14/write-ahead-log-understanding-postgresql-conf-checkpoint_segments-checkpoint_timeout-checkpoint_warning/"

            abstract = "This parameter defines how much WAL files can be stored before a automatic CHECKPOINT. All files are stored in the pg_xlog directory."
            default_value = ""

            if float(self.pg_version) >= 9.1:
                default_value = "3"

            parameter["documentation"] = self._define_doc(
                parameter["name"],
                "runtime-config-wal.html#GUC-CHECKPOINT-SEGMENTS", abstract,
                default_value, recomendation_posts)

            if enviroment_name in ["WEB", "Mixed"]:
                parameter["formula"] = 32
            elif enviroment_name == "OLTP":
                parameter["formula"] = 64
            elif enviroment_name == "DW":
                parameter["formula"] = 128
            else:
                parameter["formula"] = 3

            category["parameters"].append(parameter)

        ## min_wal_size
        if float(self.pg_version) >= 9.5:
            parameter = {}
            parameter["name"] = "min_wal_size"
            parameter["min_version"] = 9.5
            parameter["min_value"] = "80MB"
            parameter["format"] = ParameterFormat.Bytes

            abstract = "This parameter defines the minimum size of the pg_xlog directory. pgx_log directory contains the WAL files."
            default_value = ""

            if float(self.pg_version) >= 9.5:
                default_value = "80MB"

            parameter["documentation"] = self._define_doc(
                parameter["name"], "runtime-config-wal.html#GUC-MIN-WAL-SIZE",
                abstract, default_value)

            if enviroment_name in ["WEB", "Mixed"]:
                parameter["formula"] = 536870912
            elif enviroment_name == "OLTP":
                parameter["formula"] = 1073741824
            elif enviroment_name == "DW":
                parameter["formula"] = 2147483648
            else:
                parameter["formula"] = 2147483648

            category["parameters"].append(parameter)

            ## max_wal_size
            parameter = {}
            parameter["name"] = "max_wal_size"
            parameter["min_version"] = 9.5
            parameter["min_value"] = "1GB"
            parameter["format"] = ParameterFormat.Bytes

            abstract = "This parameter defines the maximun size of the pg_xlog directory. pgx_log directory contains the WAL files."
            default_value = ""

            if float(self.pg_version) >= 9.5:
                default_value = "1GB"

            parameter["documentation"] = self._define_doc(
                parameter["name"], "runtime-config-wal.html#GUC-MAX-WAL-SIZE",
                abstract, default_value)

            if enviroment_name in ["WEB", "Mixed"]:
                parameter["formula"] = 1610612736
            elif enviroment_name == "OLTP":
                parameter["formula"] = 3221225472
            elif enviroment_name == "DW":
                parameter["formula"] = 6442450944
            else:
                parameter["formula"] = 1073741824

            category["parameters"].append(parameter)

        ## checkpoint_completion_target
        parameter = {}
        parameter["name"] = "checkpoint_completion_target"
        parameter["format"] = ParameterFormat.Float

        abstract = "This parameter defines a percentual of checkpoint_timeout as a target to write the CHECKPOINT data on the disk."
        default_value = ""

        if float(self.pg_version) >= 9.1:
            default_value = "0.5"

        recomendation_posts = {}
        recomendation_posts[
            "Understaning postgresql.conf: CHECKPOINT_COMPLETION_TARGET"] = "https://www.depesz.com/2010/11/03/checkpoint_completion_target/"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET",
            abstract, default_value, recomendation_posts)

        if enviroment_name == "WEB":
            parameter["formula"] = 0.7
        elif enviroment_name in ["OLTP", "DW", "Mixed"]:
            parameter["formula"] = 0.9
        else:
            parameter["formula"] = 0.5

        category["parameters"].append(parameter)

        ## wal_buffers
        parameter = {}
        parameter["name"] = "wal_buffers"
        parameter["format"] = ParameterFormat.Bytes
        parameter["max_value"] = "16MB"

        abstract = "This parameter defines a buffer to store WAL changes before write it in the WAL file."
        default_value = ""

        if float(self.pg_version) >= 9.1:
            default_value = "3% of shared_buffers or 64KB at the minimum"

        parameter["documentation"] = self._define_doc(
            parameter["name"], "runtime-config-wal.html#GUC-WAL-BUFFERS",
            abstract, default_value)

        if enviroment_name in ["WEB", "OLTP", "DW", "Mixed"]:
            parameter["formula"] = "(TOTAL_RAM / 4 ) * 0.03"
        else:
            parameter["formula"] = "(TOTAL_RAM / 16 ) * 0.03"

        category["parameters"].append(parameter)

        return_output.append(category)

        ##### Checkpoint Related Configuration
        category = {}
        category["category"] = "network_related"
        category["description"] = "Network Related Configuration"
        category["parameters"] = list()

        ## listen_addresses
        parameter = {}
        parameter["name"] = "listen_addresses"
        parameter["format"] = ParameterFormat.String

        abstract = "This parameter defines a network address to bind to."
        default_value = ""

        if float(self.pg_version) >= 9.1:
            default_value = "localhost"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-connection.html#GUC-LISTEN-ADDRESSES", abstract,
            default_value)

        parameter["formula"] = "*"

        category["parameters"].append(parameter)

        ## max_connections
        parameter = {}
        parameter["name"] = "max_connections"
        parameter["format"] = ParameterFormat.Decimal

        abstract = "This parameter defines a max connections allowed."
        default_value = ""

        if float(self.pg_version) >= 9.1:
            default_value = "100"

        parameter["documentation"] = self._define_doc(
            parameter["name"],
            "runtime-config-connection.html#GUC-MAX-CONNECTIONS", abstract,
            default_value)

        parameter["formula"] = self.get_argument("max_connections", 100, True)

        category["parameters"].append(parameter)

        return_output.append(category)

        return return_output

    def get_rules(self):
        """
        **Get a list of rules **


        Returns
            list of rules (used to compute get-config) 
        Sample URL
            ::

                /v1/tuning/get-rules
            ::

        Sample output
            ::
            
                [{
                    "category": "memory_related",
                    "description": "Memory Configuration",
                    "parameters": [{
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-resource.html#GUC-SHARED-BUFFERS",
                        "format": "bytes",
                        "formula": "TOTAL_RAM / 4",
                        "max_value": "8GB",
                        "name": "shared_buffers"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-resource.html#GUC-WORK-MEM",
                        "format": "bytes",
                        "formula": "(TOTAL_RAM / 4) * 3",
                        "name": "effective_cache_size"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE",
                        "format": "bytes",
                        "formula": "(TOTAL_RAM / MAX_CONNECTIONS)",
                        "name": "work_mem"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM",
                        "format": "bytes",
                        "formula": "(TOTAL_RAM / 16)",
                        "max_value": "2GB",
                        "name": "maintenance_work_mem"
                    }]
                }, {
                    "category": "checkpoint_related",
                    "description": "Checkpoint Related Configuration",
                    "parameters": [{
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-wal.html#GUC-MIN-WAL-SIZE",
                        "format": "bytes",
                        "formula": 536870912,
                        "min_version": 9.5,
                        "name": "min_wal_size"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-wal.html#GUC-MIN-WAL-SIZE",
                        "format": "bytes",
                        "formula": 1610612736,
                        "min_version": 9.5,
                        "name": "max_wal_size"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET",
                        "format": "float",
                        "formula": 0.7,
                        "name": "checkpoint_completion_target"
                    }, {
                        "doc_url": "http://www.postgresql.org/docs/9.5/static/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET",
                        "format": "bytes",
                        "formula": "(TOTAL_RAM / 4 ) * 0.03",
                        "max_value": "16MB",
                        "name": "wal_buffers"
                    }]
                }]
            ::

        """
        return_data = self._get_rules(self.enviroment_name)
        self.return_output(return_data)

    def get_config(self):
        """
        **Get Configuration**


        Returns
            list of suggested parameters
        Sample URL
            ::

                /v1/tuning/get-config?enviroment_name=WEB&total_ram=8GB&max_connections=200&format=conf
            ::

        Sample output
            ::
            
                {
                    "data": [{
                        "category": "memory_related",
                        "description": "Memory Configuration",
                        "parameters": [{
                            "config_value": "2.00GB",
                            "name": "shared_buffers"
                        }, {
                            "config_value": "6.00GB",
                            "name": "effective_cache_size"
                        }, {
                            "config_value": "40.96MB",
                            "name": "work_mem"
                        }, {
                            "config_value": "512.00MB",
                            "name": "maintenance_work_mem"
                        }]
                    }, {
                        "category": "checkpoint_related",
                        "description": "Checkpoint Related Configuration",
                        "parameters": [{
                            "config_value": "512.00MB",
                            "name": "min_wal_size"
                        }, {
                            "config_value": "1.50GB",
                            "name": "max_wal_size"
                        }, {
                            "config_value": 0.7,
                            "name": "checkpoint_completion_target"
                        }, {
                            "config_value": "61.44MB",
                            "name": "wal_buffers"
                        }]
                    }],
                    "jsonapi": {
                        "version": "1.0"
                    },
                    "links": {
                        "self": "http://api.pgconfig.org/v1/tuning/get-config?enviroment_name=WEB&total_ram=8GB&max_connections=200&format=json"
                    },
                    "meta": {
                        "copyright": "PGConfig API",
                        "version": "1.0"
                    }
                }
            ::

        :param total_ram: Total dedicated of RAM memory of the database server
        :param max_connections: number of maximum espected connections
        :param enviroment_name: type of enviroment
        :param show_doc: show documentation details
        """
        message = self._get_config()

        if self.default_format == "conf":
            self.write_config(message)
        elif self.default_format == "alter_system":
            self.write_alter_system(message)
        else:
            self.write_json_api(message)

    def get_config_all_environments(self):
        self.write_json_api(self._get_config_all_environments())

    def _get_config_all_environments(self):

        all_rules = list()

        for env_name in self.get_all_environments():
            new_env = {}
            new_env["environment"] = env_name
            new_env["configuration"] = self._get_config(env_name)

            all_rules.append(new_env)

        return all_rules

    def _get_config(self, environment_name=None, include_pgbadger=None):
        total_ram = bytes.human2bytes(
            self.get_argument("total_ram", "2GB", True))
        max_connections = self.get_argument("max_connections", 100, True)

        if environment_name is None:
            environment_name = self.enviroment_name

        if include_pgbadger is None:
            include_pgbadger = self.include_pgbadger

        rule_list = self._get_rules(environment_name)

        for category in rule_list:
            for parameter in category["parameters"]:
                formula = parameter["formula"]

                if parameter["format"] != ParameterFormat.String:
                    if isinstance(formula, str):
                        formula = formula.replace("TOTAL_RAM", str(total_ram))
                        formula = formula.replace("MAX_CONNECTIONS",
                                                  str(max_connections))

                    config_value = eval(str(formula))

                    min_value = parameter.get("min_value", config_value)
                    max_value = parameter.get("max_value", config_value)

                    if parameter["format"] == ParameterFormat.Bytes:
                        if "b" in str(min_value).lower():
                            min_value = bytes.human2bytes(min_value)

                        if "b" in str(max_value).lower():
                            max_value = bytes.human2bytes(max_value)

                    parameter["config_value"] = config_value

                    if config_value < min_value:
                        parameter["config_value"] = min_value

                    if config_value > max_value:
                        parameter["config_value"] = max_value

                    if parameter["format"] == ParameterFormat.Bytes:
                        config_value = parameter["config_value"]
                        parameter["config_value"] = bytes.sizeof_fmt(
                            config_value)
                else:
                    parameter["config_value"] = parameter["formula"]

                parameter.pop("doc_url", None)
                parameter.pop("formula", None)
                parameter.pop("max_value", None)
                parameter.pop("min_value", None)
                # parameter.pop("format", None)
                parameter.pop("min_version", None)
                parameter.pop("max_version", None)

                if not self.show_doc:
                    parameter.pop("documentation", None)

        if include_pgbadger:
            from generators.pgbadger import PGBadgerConfigurationHandler

            handler = PGBadgerConfigurationHandler(self.application,
                                                   self.request)
            for category in handler._get_config():
                rule_list.append(category)

        return rule_list

    # TODO: Create a method to display parameters documentation

    def get(self, slug=None):
        if slug == "get-config":
            self.get_config()
        elif slug == "get-config-all-environments":
            self.get_config_all_environments()
        elif slug == "list-enviroments":
            self.list_enviroments()
        elif slug == "get-rules":
            self.get_rules()
        else:
            raise tornado.web.HTTPError(404)