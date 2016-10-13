import tornado.web
from common import util

class NativeReplicationHandler(util.GeneratorRequestHandler):

    def get_master_config(self):

        return_data = list()
        category = {}
        category["category"] = "master_config"
        category["description"] = "Master replication Configuration"
        category["parameters"] = list()


        ## wal_level
        parameter = {}
        parameter["name"] = "wal_level"
        parameter["config_value"] = "hot_standby"
        parameter["format"] = "string"
        category["parameters"].append(parameter)
        
        ## max_wal_senders
        parameter = {}
        parameter["name"] = "max_wal_senders"
        parameter["config_value"] = 2
        category["parameters"].append(parameter)
        
        ## wal_sender_timeout
        parameter = {}
        parameter["name"] = "wal_sender_timeout"
        parameter["config_value"] = "60s"
        parameter["format"] = "time"
        category["parameters"].append(parameter)
        
        
        if float(self.pg_version) >= 8.0 and float(self.pg_version) <= 9.4:
            wal_keep_segments = 640 # ~10GB

            ## wal_keep_segments
            parameter = {}
            parameter["name"] = "wal_keep_segments"
            parameter["config_value"] = "640"
            parameter["comment"] = "10GB of WAL retention"
            category["parameters"].append(parameter)
        else:
            ## wal_sender_timeout
            parameter = {}
            parameter["name"] = "max_replication_slots"
            parameter["config_value"] = 1
            category["parameters"].append(parameter)


        category["sql_commands"] = list()
        create_role_sql = "CREATE ROLE {} WITH LOGIN REPLICATION PASSWORD '{}';".format(self.inputed_user, self.inputed_password)

        category["sql_commands"].append(create_role_sql)

        if float(self.pg_version) >= 9.5:
            category["sql_commands"].append(
                "SELECT * FROM pg_create_physical_replication_slot('{}');".format(self.inputed_slot_name)
            )

        category["hba_rules"] = list()
        category["hba_rules"].append(
            "host     replication     {}        {}/32      md5".format(self.inputed_user, self.inputed_standby_host)
        )

        # db_restart means restart of the database is needed
        category["execute_order"] = [ "parameters", "hba_rules", "db_restart", "sql_commands"]

        
        return_data.append(category)

        self.return_output(return_data)

    def get(self, slug = None):
        self.inputed_user = self.get_argument("user", "replicator", True)
        self.inputed_password = self.get_argument("password", "qwerty123#@!", True)
        self.inputed_standby_host = self.get_argument("standby-host", "192.168.10.1", True)
        self.inputed_slot_name = self.get_argument("slot-name", "standby_config_for_{}".format(self.inputed_user), True)

        if slug == "get-master-setup":
            self.get_master_config()
        else:
            raise tornado.web.HTTPError(404)