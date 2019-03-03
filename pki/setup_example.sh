#!/bin/bash
./clean.sh
./gen_root_ca.sh capass changeit
./gen_node_cert.sh 0 changeit capass 
./gen_client_node_cert.sh sgadmin changeit capass
rm -f ./*tmp*
