

##################################
#for router 0000000000000021
#assign address for each port
curl -X POST -d '{"address": "10.0.0.1/24"}' http://localhost:8085/router/0000000000000021


curl -X POST -d '{"address": "100.0.0.1/8"}' http://localhost:8085/router/0000000000000021

##################################
#firewall 0000000000000031

curl -X PUT http://192.168.1.8:8085/firewall/module/enable/0000000000000031


#firewall
#to enable ping from h1/h2 to router port 10.0.0.1
 curl -X POST -d '{"nw_src": "10.0.0.1/24", "nw_dst": "10.0.0.2/24", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
 
 
 #to enable ping from h1/h2 to router port 100.0.0.1
 curl -X POST -d '{"nw_src": "10.0.0.1/24", "nw_dst": "100.0.0.1", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.1", "nw_dst": "10.0.0.1/24", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031



 to enable ping from h1 to router port 100.0.0.2
 curl -X POST -d '{"nw_src": "10.0.0.2", "nw_dst": "100.0.0.2", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.2", "nw_dst": "10.0.0.2", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
 
 
 to enable ping from h2 to router port 100.0.0.2
 curl -X POST -d '{"nw_src": "10.0.0.3", "nw_dst": "100.0.0.3", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.3", "nw_dst": "10.0.0.3", "nw_proto": "ICMP"}' http://192.168.1.8:8085/firewall/rules/0000000000000031
