# clear ; sudo ryu-manager simple_switch_13_custom.py  rest_router_FW_custom.py  ryu.app.ofctl_rest   /home/ubuntu/sdn/sources/flowmanager/flowmanager.py --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 8085
#Mac_of_inside_port =macofinsideport
#Mac_of_outside_port =macofoutsideport

#mininet> h8 iperf -s &
#mininet> h7 iperf -s &
#mininet> h6 iperf -s &
#mininet> h5 iperf -s &
#mininet> h4 iperf -s &

#b. TCP Traffic Test between h1 to h4
#
#Run IPERF TCP Server in h4
#
#iperf -s
#
#-s means server mode
#
#RUN IPERF TCP Client in h1
#
#iperf -c 100.0.0.4 -i 10 -t 30
#iperf -c 10.0.0.4 -i 10 -b 10m -t 30
#iperf -c 10.0.0.4 -i 10 -P 10 -t 30
#
#-c means client mode.
#
#-i means reporting interval
#
#-t means test duration in seconds
#
#-b means bandwidth 10m means 10Mbps
#
#-P means parallel connections
#
#c. UDP Traffic Test between h1 to h4
#
#Run IPERF UDP Server in h4
#
#iperf -u -s
#
#-u means udp
#
#RUN IPERF UDP Client in h1
#
#iperf -u -c 10.1.1.4 -b 10m -i 10 -t 30
#iperf -u -c 10.1.1.4 -b 10m -i 10 -P 10 -t 30
#
#-b means bandwidth 10m means 10Mbps

##################################
#for router 0000000000000021
#assign address for each port
curl -X POST -d '{"address": "10.0.0.1/24"}' http://localhost:8085/router/0000000000000021


curl -X POST -d '{"address": "100.0.0.1/8"}' http://localhost:8085/router/0000000000000021


#Give rules to Router
curl -X POST -d '{
    "dpid": 33,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 1001,
    "hard_timeout": 0,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" : "100.0.0.1/8",
        "icmpv4_type": "8",
        }
    ,"actions":[{"type":"DROP"}]      
        }' http://localhost:8085/stats/flowentry/add
		
		
		
curl -X POST -d '{
    "dpid": 33,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst":"172.16.20.1",
        "ipv4_src" : "172.16.20.10",
        "ip_proto" : 6,
        "tcp_dst": 54321
        }
    ,"actions":[
        {"type": "DEC_NW_TTL"},
        {"type":"OUTPUT","port": 2},
        {"type":"SET_FIELD","field":"ipv4_dst","value":"172.16.10.10"},
        {"type":"SET_FIELD","field":"ipv4_src","value":"172.16.20.10"},
        {"type":"SET_FIELD","field":"tcp_dst","value":12345}        
        ]}' http://localhost:8085/stats/flowentry/add		
