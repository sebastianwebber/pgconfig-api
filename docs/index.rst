.. PGConfig API documentation master file, created by
   sphinx-quickstart on Sat May 14 17:30:16 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


PGConfig API's documentation
##############################

The API are deployed on http://api.pgconfig.org/v1/. Details about each method and options are detailed bellow.

.. note:: All generators and advisors support the common parameters ``pg_version`` and ``format``.

Advisors
**********

Tuning
==========================



About output ``format``
==========================

On tuning advisor, extra formats are avaliable:

``conf``:
	Exports ouput into configuration file ( ``.conf``) format. Example:

	.. code-block:: bash
	
		# Memory Configuration
		shared_buffers = 2.00GB
		effective_cache_size = 6.00GB
		work_mem = 40.96MB
		maintenance_work_mem = 512.00MB

		# Checkpoint Related Configuration
		min_wal_size = 512.00MB
		max_wal_size = 1.50GB
		checkpoint_completion_target = 0.7
		wal_buffers = 61.44MB


``alter_system``:
	Exports ouput into ``ALTER SYSTEM`` command format. Example:

	.. code-block:: sql
	
		-- Memory Configuration
		ALTER SYSTEM SET shared_buffers TO '2.00GB';
		ALTER SYSTEM SET effective_cache_size TO '6.00GB';
		ALTER SYSTEM SET work_mem TO '40.96MB';
		ALTER SYSTEM SET maintenance_work_mem TO '512.00MB';

		-- Checkpoint Related Configuration
		ALTER SYSTEM SET min_wal_size TO '512.00MB';
		ALTER SYSTEM SET max_wal_size TO '1.50GB';
		ALTER SYSTEM SET checkpoint_completion_target TO '0.7';
		ALTER SYSTEM SET wal_buffers TO '61.44MB';

List Enviroments
--------------------

.. automethod:: advisors.tuning.TuningHandler.list_enviroments

Get Rules
--------------------

.. automethod:: advisors.tuning.TuningHandler.get_rules

Get Configuration
--------------------

.. automethod:: advisors.tuning.TuningHandler.get_config

Generators
************

About output ``format``
==========================

The parameter ``format`` can be:

``json``:
	Exports ouput into json format. Example:

	.. code-block:: json

	   {
	    "output": 
	    [
	        "CREATE SCHEMA IF NOT EXISTS dev_sales_remote;",
	        "IMPORT FOREIGN SCHEMA sales_schema LIMIT TO (customer, sales) FROM SERVER dev_server INTO dev_sales_remote;"
	    ]
	   }
	.. note:: ``json`` format is the default value.
	

``bash``:
	Exports ouput into bash format. Example:

	.. code-block:: bash

   		#!/bin/bash

		SQL_QUERY="CREATE SCHEMA IF NOT EXISTS dev_sales_remote;"
		psql -c "${SQL_QUERY}"

		SQL_QUERY="IMPORT FOREIGN SCHEMA sales_schema LIMIT TO (customer, sales) FROM SERVER dev_server INTO dev_sales_remote;"
		psql -c "${SQL_QUERY}"

``sql``:
	Exports ouput into SQL format. Example:

	.. code-block:: SQL

   		CREATE SCHEMA IF NOT EXISTS dev_sales_remote;
		IMPORT FOREIGN SCHEMA sales_schema LIMIT TO (customer, sales) FROM SERVER dev_server INTO dev_sales_remote;


Foreign Data Wrappers
==========================

Generate Connection
--------------------
	
.. automethod:: generators.fdw.FDWHandler.generate_connection

Generate User Mapping
-----------------------
	
.. automethod:: generators.fdw.FDWHandler.generate_user_mapping

Import foreign schema
-----------------------
	
.. automethod:: generators.fdw.FDWHandler.import_foreign_schema