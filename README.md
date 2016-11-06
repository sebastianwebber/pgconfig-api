# PGConfig API

This project it's API that [pgconfig.org](http://pgconfig.org) uses to calculate the tuning values and stuff.

### How it works

The web interface ([pgconfig.org website](http://pgconfig.org) or just `UI`) access this api on the address [`https://api.pgconfig.org/v1/tuning/get-config`](https://api.pgconfig.org/v1/tuning/get-config).

You can call it from `curl`, eg:

```bash
$ curl 'https://api.pgconfig.org/v1/tuning/get-config'
{"data": [{"category": "memory_related","description": "Memory Configuration","parameters": [{"config_value": "512MB","format": "Bytes","name": "shared_buffers"},{"config_value": "2GB","format": "Bytes","name": "effective_cache_size"},{"config_value": "20MB","format": "Bytes","name": "work_mem"},{"config_value": "128MB","format": "Bytes","name": "maintenance_work_mem"}]},{"category": "checkpoint_related","description": "Checkpoint Related Configuration","parameters": [{"config_value": "512MB","format": "Bytes","name": "min_wal_size"},{"config_value": "2GB","format": "Bytes","name": "max_wal_size"},{"config_value": 0.7,"format": "Float","name": "checkpoint_completion_target"},{"config_value": "15MB","format": "Bytes","name": "wal_buffers"}]},{"category": "network_related","description": "Network Related Configuration","parameters": [{"config_value": "*","format": "String","name": "listen_addresses"},{"config_value": 100,"format": "Decimal","name": "max_connections"}]}],"jsonapi": {"version": "1.0"},"links": {"self": "http://api.pgconfig.org/v1/tuning/get-config"},"meta": {"arguments": {},"copyright": "PGConfig API","version": "2.0 beta"}}
```

With a litle formating, looks like this:

```json
{  
   "data":[  
      {  
         "category":"memory_related",
         "description":"Memory Configuration",
         "parameters":[  
            {  
               "config_value":"512MB",
               "format":"Bytes",
               "name":"shared_buffers"
            },
            {  
               "config_value":"2GB",
               "format":"Bytes",
               "name":"effective_cache_size"
            },
            {  
               "config_value":"20MB",
               "format":"Bytes",
               "name":"work_mem"
            },
            {  
               "config_value":"128MB",
               "format":"Bytes",
               "name":"maintenance_work_mem"
            }
         ]
      },
      {  
         "category":"checkpoint_related",
         "description":"Checkpoint Related Configuration",
         "parameters":[  
            {  
               "config_value":"512MB",
               "format":"Bytes",
               "name":"min_wal_size"
            },
            {  
               "config_value":"2GB",
               "format":"Bytes",
               "name":"max_wal_size"
            },
            {  
               "config_value":0.7,
               "format":"Float",
               "name":"checkpoint_completion_target"
            },
            {  
               "config_value":"15MB",
               "format":"Bytes",
               "name":"wal_buffers"
            }
         ]
      },
      {  
         "category":"network_related",
         "description":"Network Related Configuration",
         "parameters":[  
            {  
               "config_value":"*",
               "format":"String",
               "name":"listen_addresses"
            },
            {  
               "config_value":100,
               "format":"Decimal",
               "name":"max_connections"
            }
         ]
      }
   ],
   "jsonapi":{  
      "version":"1.0"
   },
   "links":{  
      "self":"http://api.pgconfig.org/v1/tuning/get-config"
   },
   "meta":{  
      "arguments":{  

      },
      "copyright":"PGConfig API",
      "version":"2.0 beta"
   }
}
```

Basically, the important data are in the `data` node, grouped by categories, just like in the `UI`. :)

A important thing about this is that you can format the output displayed more conveniently, only informing the `format=conf` parameters, eg:

```bash
$ curl 'https://api.pgconfig.org/v1/tuning/get-config?format=conf'
# Generated by PGConfig 2.0 beta
## http://pgconfig.org

# Memory Configuration
shared_buffers = 512MB
effective_cache_size = 2GB
work_mem = 20MB
maintenance_work_mem = 128MB

# Checkpoint Related Configuration
min_wal_size = 512MB
max_wal_size = 2GB
checkpoint_completion_target = 0.7
wal_buffers = 15MB

# Network Related Configuration
listen_addresses = '*'
max_connections = 100
```

Another options for the `format` parameters are `json` (the default value) and `alter_system`, take a look:

```bash
$ curl 'https://api.pgconfig.org/v1/tuning/get-config?format=alter_system'
-- Generated by PGConfig 2.0 beta
---- http://pgconfig.org

-- Memory Configuration
ALTER SYSTEM SET shared_buffers TO '512MB';
ALTER SYSTEM SET effective_cache_size TO '2GB';
ALTER SYSTEM SET work_mem TO '20MB';
ALTER SYSTEM SET maintenance_work_mem TO '128MB';

-- Checkpoint Related Configuration
ALTER SYSTEM SET min_wal_size TO '512MB';
ALTER SYSTEM SET max_wal_size TO '2GB';
ALTER SYSTEM SET checkpoint_completion_target TO '0.7';
ALTER SYSTEM SET wal_buffers TO '15MB';

-- Network Related Configuration
ALTER SYSTEM SET listen_addresses TO '*';
ALTER SYSTEM SET max_connections TO '100';
```

In short: to change the output, all you need is to do it's puting the parameters in the URL.

### Available parameters

The list below lists the available parameters:

<table class="table table-striped table-bordered">
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Possible values</th>
                <th>Default Value</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>pg_version</code></td>
                <td>from <code>9.0</code> version until <code>9.6</code></td>
                <td><code>9.6</code></td>
                <td>Sets the PostgreSQL version</td>
            </tr>
            <tr>
                <td><code>total_ram</code></td>
                <td>any value above <code>1GB</code></td>
                <td><code>2GB</code></td>
                <td>Total memory <strong>dedicated</strong> to the PostgreSQL.</td>
            </tr>
            <tr>
                <td><code>max_connections</code></td>
                <td>any value above <code>1</code></td>
                <td><code>100</code></td>
                <td><strong>expected</strong> number of connections</td>
            </tr>
            <tr>
                <td><code>env_name</code></td>
                <td><code>WEB</code>, <code>OLTP</code>, <code>DW</code>, <code>Mixed</code> and <code>Desktop</code></td>
                <td><code>WEB</code></td>
                <td>Sets the environment that the server will run (more details below)</td>
            </tr>
            <tr>
                <td><code>os_type</code></td>
                <td><code>Linux</code>, <code>Windows</code> and <code>Unix</code></td>
                <td><code>Linux</code></td>
                <td>Sets the type of operating system used</td>
            </tr>
            <tr>
                <td><code>arch</code></td>
                <td><code>x86-64</code> and <code>i686</code></td>
                <td><code>x86-64</code></td>
                <td>Sets the server architecture</td>
            </tr>
            <tr>
                <td><code>format</code></td>
                <td><code>json</code>, <code>conf</code> and <code>alter_system</code></td>
                <td><code>json</code></td>
                <td>changes the output format</td>
            </tr>
            <tr>
                <td><code>show_doc</code></td>
                <td><code>true</code> and <code>false</code></td>
                <td><code>false</code></td>
                <td>Shows the documentation (valid only for the <code>json</code> format)</td>
            </tr>
            <tr>
                <td><code>include_pgbadger</code></td>
                <td><code>true</code> and <code>false</code></td>
                <td><code>false</code></td>
                <td>Add the settings to enable pgbadger</td>
            </tr>
        </tbody>
    </table>

> **Important** Don't forget, when setting the `total_ram` parameter, set the value like the expression `[0-9]{1,}GB`, eg: `4GB`.

#### About the environment

The list below explains a bit more about the environments:

<table class="table table-bordered">
    <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Use cases</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>WEB</code></td>
            <td>General web applications</td>
            <td>web applications like portal or corporate application</td>
        </tr>
        <tr>
            <td><code>OLTP</code></td>
            <td>Applications with a large volume of transactions</td>
            <td>Applications of ERP type or big corporate systems with a lot of simultaneous transactions</td>
        </tr>
        <tr>
            <td><code>DW</code></td>
            <td>Dataware house applications</td>
            <td>General Business Inteligence applications</td>
        </tr>
        <tr>
            <td><code>Mixed</code></td>
            <td>Environments who share the database and the application in the same server</td>
            <td>Small applications, typically running on the web</td>
        </tr>
        <tr>
            <td><code>Desktop</code></td>
            <td>Development environment</td>
            <td>development machine, support or pre-sales</td>
        </tr>
    </tbody>
</table>


#### Full example

The example below its used by the `UI`:

```bash
$ curl 'https://api.pgconfig.org/v1/tuning/get-config?env_name=WEB&format=alter_system&include_pgbadger=true&log_format=stderr&max_connections=100&pg_version=9.6&total_ram=2GB'
```

### How the values are calculated?

In an attempt to make the process simpler, i created a API context to list the rules. It can be access by the URL below:

- [/v1/tuning/get-rules](https://api.pgconfig.org/v1/tuning/get-rules) 

> **Important:** This context supports the follow parameters: `os_type`, `arch` e `env_name`. 

The fields who contains details how each parameter are calculated are `formula` and `max_value`, eg:

```json
...
"format": "Bytes",
"formula": "TOTAL_RAM / 4",
"max_value": "2047MB",
"name": "shared_buffers"
...
```

> Note that the values are influenced by the filters mentioned above.

#### Calling the `get-rules` context

I recommend that you open the URL below on the browser for easy viewing (or just [format the json](https://jsonformatter.curiousconcept.com/)):

```bash
curl 'https://api.pgconfig.org/v1/tuning/get-rules?os_type=Windows&arch=i686&env_name=OLTP'
```

### Another API Options

<table class="table table-striped table-bordered">
    <thead>
        <tr>
            <th>Address</th>
            <th>Description</th>
            <th>Output example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://api.pgconfig.org/v1/tuning/get-config-all-environments"><code>/v1/tuning/get-config-all-environments</code></a></td>
            <td>show rules for all environments</td>
            <td><pre><code class="language-json"></code>...
"data": [
    {
    "configuration": [..],
    "environment": "WEB"
    },
    {
    "configuration": [..],
    "environment": "OLTP"
    },
    {
    "configuration": [..],
    "environment": "DW"
    },
    {
    "configuration": [..],
    "environment": "Mixed"
    },
    {
    "configuration": [..],
    "environment": "Desktop"
    }
]
...</pre></td>
        </tr>
        <tr>
            <td><a href="https://api.pgconfig.org/v1/tuning/list-enviroments"><code>/v1/tuning/list-enviroments</code></a></td>
            <td>Show all environments</td>
            <td><pre><code class="language-json"></code>...
"data": [
    "WEB",
    "OLTP",
    "DW",
    "Mixed",
    "Desktop"
],
...</pre></td>
        </tr>
        <tr>
            <td><a href="https://api.pgconfig.org/v1/generators/pgbadger/get-config"><code>/v1/generators/pgbadger/get-config</code></a></td>
            <td>Show the pgbadger configurations (accepts the <code>format</code> parameter)</td>
            <td><pre><code class="language-json"></code>...
"data": [
    {
    "category": "log_config",
    "description": "Logging configuration for pgbadger",
    "parameters": [
        {
        "config_value": "on",
        "name": "logging_collector"
        },
        {
        "config_value": "on",
        "name": "log_checkpoints"
        },
        {
        "config_value": "on",
        "name": "log_connections"
        },
        {
        "config_value": "on",
        "name": "log_disconnections"
        },
        {
        "config_value": "on",
        "name": "log_lock_waits"
        },
        {
        "config_value": "0",
        "name": "log_temp_files"
        },
        {
        "config_value": "C",
        "format": "String",
        "name": "lc_messages"
        },
        {
        "comment": "Adjust the minimum time to collect data",
        "config_value": "10s",
        "format": "Time",
        "name": "log_min_duration_statement"
        },
        {
        "config_value": "0",
        "name": "log_autovacuum_min_duration"
        }
    ]
},
...</pre></td>
        </tr>
    </tbody>
</table>

Another contexts are being developed.