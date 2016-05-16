.. PGConfig API documentation master file, created by
   sphinx-quickstart on Sat May 14 17:30:16 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


PGConfig API's documentation
##############################

The API are deployed on http://api.pgconfig.org. Details about each method and options are detailed bellow.


Generators
************

.. note:: All generators support the common parameters ``pg_version`` and ``format``.

About output ``format``
==========================

The parameter ``format`` can be:




``json``:
	Exports ouput into json format. *It's the default value*. Example:

	.. code-block:: json

	   {
	    "output": 
	    [
	        "CREATE SCHEMA IF NOT EXISTS dev_sales_remote;",
	        "IMPORT FOREIGN SCHEMA sales_schema LIMIT TO (customer, sales) FROM SERVER dev_server INTO dev_sales_remote;"
	    ]
	   }

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