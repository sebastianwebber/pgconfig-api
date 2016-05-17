# -*- coding: UTF-8 -*-

import tornado.web
import json
from common import util
from common import bytes

class TuningHandler(util.DefaultRequestHandler):
	
	def initialize(self):
		super(TuningHandler, self).initialize()
		self.enviroment_name = self.get_argument("enviroment_name", "WEB", True)
	
	def write_config(self, output_data):
		for category in output_data:
			self.write("# {}\n".format(category["description"]))
			for parameter in category["paramater-list"]:
				config_value = parameter.get("config_value", "NI")
				self.write(
					"{} = {}\n".format(parameter["name"], config_value)
				)
			self.write("\n")
	
	def write_alter_system(self, output_data):
		for category in output_data:
			self.write("-- {}\n".format(category["description"]))
			for parameter in category["paramater-list"]:
				config_value = parameter.get("config_value", "NI")
				self.write(
					"ALTER SYSTEM SET {} TO '{}';\n".format(parameter["name"], config_value)
				)
			self.write("\n")
				
	def return_output(self, message):
		self.set_header('Content-Type', 'application/json')
		self.write( json.dumps(message, sort_keys = True,separators=(',', ': ')))

	
	def list_enviroments(self):
		self.write_json_api([ "WEB", "OLTP", "DW", "Mixed", "Desktop" ]) 

	def _get_rules(self, enviroment_name):
	
		return_output = list()
		
		##### Memory Related
		category = {}
		category["category"] = "memory_related"
		category["description"] = "Memory Configuration"
		category["paramater-list"] = list()
	
		## shared_buffers
		parameter = {}
		parameter["name"] = "shared_buffers"
		parameter["max_value"] = "8GB"
		parameter["format"] = "bytes"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-resource.html#GUC-SHARED-BUFFERS".format(self.pg_version)
		
		if	enviroment_name == "Desktop":
			parameter["formula"] = "TOTAL_RAM / 16"
		else:
			parameter["formula"] = "TOTAL_RAM / 4"
		
		category["paramater-list"].append(parameter)
		
		## effective_cache_size
		parameter = {}
		parameter["name"] = "effective_cache_size"
		parameter["format"] = "bytes"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-resource.html#GUC-WORK-MEM".format(self.pg_version)
		
		if	enviroment_name == "Desktop":
			parameter["formula"] = "TOTAL_RAM / 4"
		else:
			parameter["formula"] = "(TOTAL_RAM / 4) * 3"
		
		category["paramater-list"].append(parameter)
		
		## work_mem
		parameter = {}
		parameter["name"] = "work_mem"
		parameter["format"] = "bytes"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE".format(self.pg_version)
		
		if enviroment_name in [ "WEB", "OLTP" ]:
			parameter["formula"] = "(TOTAL_RAM / MAX_CONNECTIONS)"
		elif enviroment_name in [ "DW", "Mixed" ]:
			parameter["formula"] = "((TOTAL_RAM / 2) / MAX_CONNECTIONS)"
		else:
			parameter["formula"] = "((TOTAL_RAM / 6) / MAX_CONNECTIONS)"
		
		category["paramater-list"].append(parameter)
		
		## maintenance_work_mem
		parameter = {}
		parameter["name"] = "maintenance_work_mem"
		parameter["format"] = "bytes"
		parameter["max_value"] = "2GB"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM".format(self.pg_version)
		
		if enviroment_name in [ "WEB", "OLTP" ]:
			parameter["formula"] = "(TOTAL_RAM / 16)"
		elif enviroment_name == "DW":
			parameter["formula"] = "(TOTAL_RAM / 8)"
		else:
			parameter["formula"] = "(TOTAL_RAM / 16)"
		
		category["paramater-list"].append(parameter)
		
		return_output.append(category)
		
		##### Checkpoint Related Configuration
		category = {}
		category["category"] = "checkpoint_related"
		category["description"] = "Checkpoint Related Configuration"
		category["paramater-list"] = list()
		
		## checkpoint_segments
		if float(self.pg_version) >= 8.0 and float(self.pg_version) <= 9.4:
			parameter = {}
			parameter["name"] = "checkpoint_segments"
			# parameter["min_version"] = 8.0
			# parameter["max_version"] = 9.4
			parameter["format"] = "decimal"
			parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-wal.html#GUC-CHECKPOINT-SEGMENTS".format(self.pg_version)
			
			if enviroment_name in [ "WEB", "Mixed" ]:
				parameter["formula"] = 32
			elif enviroment_name == "OLTP":
				parameter["formula"] = 64
			elif enviroment_name == "DW":
				parameter["formula"] = 128
			else:
				parameter["formula"] = 3
			
			category["paramater-list"].append(parameter)
		
		## min_wal_size
		if float(self.pg_version) >= 9.5:
			parameter = {}
			parameter["name"] = "min_wal_size"
			parameter["min_version"] = 9.5
			parameter["format"] = "bytes"
			parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-wal.html#GUC-MIN-WAL-SIZE".format(self.pg_version)
			
			if enviroment_name in [ "WEB", "Mixed" ]:
				parameter["formula"] = 536870912
			elif enviroment_name == "OLTP":
				parameter["formula"] = 1073741824
			elif enviroment_name == "DW":
				parameter["formula"] = 2147483648
			else:
				parameter["formula"] = 2147483648
			
			category["paramater-list"].append(parameter)
			
			## max_wal_size
			parameter = {}
			parameter["name"] = "max_wal_size"
			parameter["min_version"] = 9.5
			parameter["format"] = "bytes"
			parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-wal.html#GUC-MIN-WAL-SIZE".format(self.pg_version)
			
			if enviroment_name in [ "WEB", "Mixed" ]:
				parameter["formula"] = 1610612736
			elif enviroment_name == "OLTP":
				parameter["formula"] = 3221225472
			elif enviroment_name == "DW":
				parameter["formula"] = 6442450944
			else:
				parameter["formula"] = 1073741824
			
			category["paramater-list"].append(parameter)
		
		## checkpoint_completion_target
		parameter = {}
		parameter["name"] = "checkpoint_completion_target"
		parameter["format"] = "float"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET".format(self.pg_version)
		
		if enviroment_name ==  "WEB":
			parameter["formula"] = 0.7
		elif enviroment_name in [ "OLTP", "DW", "Mixed" ]:
			parameter["formula"] = 0.9
		else:
			parameter["formula"] = 0.5
		
		category["paramater-list"].append(parameter)
		
		## wal_buffers
		parameter = {}
		parameter["name"] = "wal_buffers"
		parameter["format"] = "bytes"
		parameter["max_value"] = "16MB"
		parameter["doc_url"] = "http://www.postgresql.org/docs/{}/static/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET".format(self.pg_version)
		
		if enviroment_name in [ "WEB", "OLTP", "DW", "Mixed" ]:
			parameter["formula"] = "(TOTAL_RAM / 4 ) * 0.03"
		else:
			parameter["formula"] = "(TOTAL_RAM / 16 ) * 0.03"
		
		category["paramater-list"].append(parameter)
		
		return_output.append(category)
		
		return return_output
		
	def get_rules(self):
		return_data = self._get_rules(self.enviroment_name)
		self.return_output(return_data)
		
	def get_config(self):
		message = self._get_config()
	
		if self.default_format == "conf":
			self.write_config(message)
		elif self.default_format == "alter_system":
			self.write_alter_system(message)	
		else:	
			self.write_json_api(message)

	def _get_config(self):
		total_ram = bytes.human2bytes(self.get_argument("total_ram", "2GB", True))
		max_connections = self.get_argument("max_connections", 100, True)
	
		self.set_header('Content-Type', 'application/json')
		
		rule_list = self._get_rules(self.enviroment_name)
		
		for category in rule_list:
			for parameter in category["paramater-list"]:
			
				formula = parameter["formula"]
				
				if isinstance(formula, str):
					formula = formula.replace("TOTAL_RAM", str(total_ram))
					formula = formula.replace("MAX_CONNECTIONS", str(max_connections))
					
				parameter["config_value"] = eval(str(formula))
				
				if parameter["format"] == "bytes":
					parameter["config_value"] = bytes.bytes2human(parameter["config_value"])
						
				parameter.pop("doc_url", None)
				parameter.pop("formula", None)
				parameter.pop("max_value", None)
				parameter.pop("format", None)
				parameter.pop("min_version", None)
				parameter.pop("max_version", None)

		return rule_list
		
        
	def get(self, slug=None):		
		if slug == "get-config":
			self.get_config()
		elif slug == "list-enviroments":
			self.list_enviroments()
		elif slug == "get-rules":
			self.get_rules()
		else:
			raise tornado.web.HTTPError(404)