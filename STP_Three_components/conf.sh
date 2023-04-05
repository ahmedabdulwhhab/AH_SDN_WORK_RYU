
##################################
#for router 0000000000000021
#assign address for each port
curl -X POST -d '{"address": "192.168.10.1/24"}' http://localhost:8086/router/0000000000000021
curl -X POST -d '{"address": "192.168.20.1/24"}' http://localhost:8086/router/0000000000000021

#firewall
curl -X PUT http://127.0.0.1:8086/firewall/module/enable/0000000000000031

curl -X POST -d '{"nw_src": "192.168.10.0/24", "nw_dst": "192.168.20.0/24", "nw_proto": "ICMP"}' http://127.0.0.1:8086/firewall/rules/0000000000000031

curl -X POST -d '{"nw_src": "192.168.20.0/24", "nw_dst": "192.168.10.0/24", "nw_proto": "ICMP"}' http://127.0.0.1:8086/firewall/rules/0000000000000031
