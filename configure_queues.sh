#!/usr/bin/env bash
set -x

curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr

sleep 1

curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "10000000", "queues": [{"max_rate": "10000000"}, {"min_rate": "75000000"}]}' http://localhost:8080/qos/queue/0000000000000001

curl -X POST -d '{"match": {"nw_dst": "10.0.0.3", "nw_proto": "UDP", "tp_dst": "1234"}, "actions":{"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001

curl -X GET http://localhost:8080/qos/rules/0000000000000001
