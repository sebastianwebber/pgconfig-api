#!/bin/bash

#format
for format in json conf alter_system; do
    # enviroments
    for env_name in  WEB OLTP DW Mixed Desktop; do
        # versions
        for version in 9.{1..5}; do
            file_name="${env_name}_${version}.${format}"
            test_name=$(echo "${env_name}_${version}_${format}" | tr -d '.')
            curl -X GET http://localhost:5000/v1/tuning/get-config\?env_name\=${env_name}\&format\=${format}\&max_connections\=150\&pg_version\=${version}\&total_ram\=10GB > ${file_name} 2> /dev/null

            echo
            echo "def test_${test_name}(self):"
            echo "    self.run_test('${format}', '${env_name}', '${version}')"

        done
    done 
done