#FOR DMZ_L3
#DPID 0000000000000012
curl -X POST -d '{"address": "192.168.100.1/24"}' http://localhost:8086/l3sw/0000000000000012
curl -X POST -d '{"address": "192.168.43.1/24"}' http://localhost:8086/l3sw/0000000000000012

for DPID12 we consider it as layer 3 switch and router
so we assign IP address for both ports (in and out).
####################################################################################################
as we have two different IP class network, DPID 18 or 0x12, if dst is 172.43.10.0/24 output is port 1

 curl -X POST -d '{
    "dpid": 18,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst" :"172.43.10.0/24",
        "ipv4_src" : "192.168.100.0/24"
        }
    ,"actions":[{"type":"OUTPUT","port": 1}]      
        }' http://localhost:8086/stats/flowentry/add
        
  ******************************************      
 as we have two different IP class network, DPID 18 or 0x12, if dst is 192.168.100.0/24 output is port 2       
 curl -X POST -d '{
    "dpid": 18,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" :"172.43.10.0/24",
        "ipv4_dst" : "192.168.100.0/24"
        }
    ,"actions":[{"type":"OUTPUT","port": 2}]      
        }' http://localhost:8086/stats/flowentry/add        
        
#####################################################################################################
as we have two different IP class network, DPID 18 or 0x12, if dst is 192.168.30.0/24 output is port 1       
    curl -X POST -d '{
    "dpid": 18,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst" :"192.168.30.0/24",
        "ipv4_src" : "192.168.100.0/24"
        }
    ,"actions":[{"type":"OUTPUT","port": 1}]      
        }' http://localhost:8086/stats/flowentry/add
 ********************************************************       
as we have two different IP class network, DPID 18 or 0x12, if dst is 192.168.100.0/24 output is port 1         
   
 curl -X POST -d '{
    "dpid": 18,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" :"192.168.30.0/24",
        "ipv4_dst" : "192.168.100.0/24"
        }
    ,"actions":[{"type":"OUTPUT","port": 2}]      
        }' http://localhost:8086/stats/flowentry/add        

#####################################################################################################
 #learning modifying packets
  curl -X POST -d '{
    "dpid": 5,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 100,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" :"192.168.100.5",
        "ipv4_dst" : "192.168.100.6"
        }
    ,"actions":[
            {"type": "DEC_NW_TTL"},
           {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:01"},
           {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:66"},
           {"type":"OUTPUT","port": 2},
           ]      
        }' http://localhost:8086/stats/flowentry/add
##################################################################################################

#################update Mac here 
#mac 03 IP 192.168.30.30 to port 1 of layer 3 switch
        #h4 = self.addHost('h4',ip='192.168.30.40/24',mac='00:00:00:00:00:04') 
at the end point which is s2 while (Email ping h3)
we have to confirm mac of h3 is mentioned as per below                 {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:03"},out is port 1
so modifiation is done in DPID 19
so we update dst mac in packet
        
 curl -X POST -d '{
    "dpid": 19,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 101,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" :"192.168.100.5",
        "ipv4_dst" : "192.168.30.30"
        }
    ,"actions":[
                {"type": "DEC_NW_TTL"},
                {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:03"},
                {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:01"},
                {"type":"OUTPUT","port": 1}
    ]      
        }' http://localhost:8086/stats/flowentry/add


*********************************
   
 curl -X POST -d '{
    "dpid": 19,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 101,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst" :"192.168.100.5",
        "ipv4_src" : "192.168.30.30"
        }
    ,"actions":[
                {"type": "DEC_NW_TTL"},
                {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:01"},
                {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:03"},
                {"type":"OUTPUT","port": 2}
    ]      
        }' http://localhost:8086/stats/flowentry/add


***********************************************************
#mac 04 IP 192.168.30.40 to port 1 of layer 3 switch
        #h4 = self.addHost('h4',ip='192.168.30.40/24',mac='00:00:00:00:00:04')            
         
 curl -X POST -d '{
    "dpid": 19,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 101,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_src" :"192.168.100.6",
        "ipv4_dst" : "192.168.30.30"
        }
    ,"actions":[
                {"type": "DEC_NW_TTL"},
                {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:03"},
                {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:02"},
                {"type":"OUTPUT","port": 1}
    ]      
        }' http://localhost:8086/stats/flowentry/add


**********************************************************
   
 curl -X POST -d '{
    "dpid": 19,
    "cookie": 1,
    "cookie_mask": 1,
    "table_id": 0,
    "priority": 101,
    "hard_timeout": 3000,
    "flags": 1,
    "match":{
        "eth_type" : 2048,
        "ipv4_dst" :"192.168.100.6",
        "ipv4_src" : "192.168.30.30"
        }
    ,"actions":[
                {"type": "DEC_NW_TTL"},
                {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:02"},
                {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:03"},
                {"type":"OUTPUT","port": 2}
    ]      
        }' http://localhost:8086/stats/flowentry/add
##################################

##################################################################################################

in above curl
if match criterio occurs, modify packet to be src mac 00:00:00:00:00:01, modify dst mac to be 00:00:00:00:00:66

The arrangement of action must be as per this
            {"type": "DEC_NW_TTL"},
           {"type":"SET_FIELD","field":"eth_src","value":"00:00:00:00:00:01"},
           {"type":"SET_FIELD","field":"eth_dst","value":"00:00:00:00:00:66"},
           {"type":"OUTPUT","port": 2},
output must be last line           
