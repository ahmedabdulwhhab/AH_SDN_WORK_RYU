

##################################
#for router 0000000000000021
#assign address for each port
curl -X POST -d '{"address": "10.0.0.1/24"}' http://localhost:8086/router/0000000000000021


curl -X POST -d '{"address": "100.0.0.1/8"}' http://localhost:8086/router/0000000000000021


curl -X POST -d '{"address": "100.0.0.1/8"}' http://localhost:8086/l3sw/0000000000000011


##################################
#firewall 0000000000000031

curl -X PUT http://192.168.1.8:8086/firewall/module/enable/0000000000000031


#firewall
#to enable ping from h1/h2 to router port 10.0.0.1
 curl -X POST -d '{"nw_src": "10.0.0.1/24", "nw_dst": "10.0.0.2/24", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031
 
 
 #to enable ping from h1/h2 to router port 100.0.0.1
 curl -X POST -d '{"nw_src": "10.0.0.1/24", "nw_dst": "100.0.0.1", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.1", "nw_dst": "10.0.0.1/24", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031



 to enable ping from h1 to router port 100.0.0.2
 curl -X POST -d '{"nw_src": "10.0.0.2", "nw_dst": "100.0.0.2", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.2", "nw_dst": "10.0.0.2", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031
 
 
 to enable ping from h2 to router port 100.0.0.2
 curl -X POST -d '{"nw_src": "10.0.0.3", "nw_dst": "100.0.0.3", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031
 curl -X POST -d '{"nw_src": "100.0.0.3", "nw_dst": "10.0.0.3", "nw_proto": "ICMP"}' http://192.168.1.8:8086/firewall/rules/0000000000000031



 curl -X POST -d '{
    "dpid": 1,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst" :"100.0.0.0/24",
        "ipv4_src" : "100.0.0.0/24"
        }
    ,"actions":[
        {"type":"OUTPUT","NORMAL"}       
        ]}' http://localhost:8086/stats/flowentry/add
