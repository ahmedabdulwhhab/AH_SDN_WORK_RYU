ryu controller
<br>
#cmd
 clear ; sudo ryu-manager   simple_switch_13_custom.py rest_router_custom.py rest_firewall_custom.py  /home/ubuntu/sdn/sources/flowmanager/flowmanager.py   --observe-links --ofp-tcp-listen-port 6632 --wsapi-port 8085
##############################
 h1 ifconfig
h1-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:01
          inet addr:10.0.0.2  Bcast:10.0.0.255  Mask:255.255.255.0


h2 ifconfig
h2-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:02
          inet addr:10.0.0.3  Bcast:10.0.0.255  Mask:255.255.255.0


h3 ifconfig
h3-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:03
          inet addr:100.0.0.2  Bcast:100.255.255.255  Mask:255.0.0.0



 h4 ifconfig
h4-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:04
          inet addr:100.0.0.3  Bcast:100.255.255.255  Mask:255.0.0.0


from mininet 
set gateway
h1 ip route add default via 10.0.0.1
h2 ip route add default via 10.0.0.1
h3 ip route add default via 100.0.0.1
h4 ip route add default via 100.0.0.1

##################################
for router 0000000000000021
assign address for each port
curl -X POST -d '{"address": "10.0.0.1/24"}' http://localhost:8085/router/0000000000000021
flow table after above line
	1037	eth_type = 2048
ipv4_dst = 10.0.0.1	1	4	0	0	OUTPUT:CONTROLLER	0	0	0
	36	eth_type = 2048
ipv4_src = 10.0.0.0/255.255.255.0
ipv4_dst = 10.0.0.0/255.255.255.0	1	4	0	0	OUTPUT:NORMAL	0	0	0
	2	eth_type = 2048
ipv4_dst = 10.0.0.0/255.255.255.0	1	4	0	0	OUTPUT:CONTROLLER	0	0	0

*******
h1 ping -c3 10.0.0.1
blocked
*******

curl -X POST -d '{"address": "100.0.0.1/8"}' http://localhost:8085/router/0000000000000021
h3 ping -c3 100.0.0.1
PING 100.0.0.1 (100.0.0.1) 56(84) bytes of data.
64 bytes from 100.0.0.1: icmp_seq=1 ttl=64 time=12.9 ms
64 bytes from 100.0.0.1: icmp_seq=2 ttl=64 time=10.6 ms
64 bytes from 100.0.0.1: icmp_seq=3 ttl=64 time=18.0 ms

--- 100.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 10.683/13.895/18.093/3.107 ms

##################################


curl -X PUT http://192.168.1.8:8082/firewall/module/enable/0000000000000001

curl -X POST -d '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.1.2/32", "nw_proto": "ICMP"}' http://192.168.1.8:8082/firewall/rules/0000000000000001

curl -X POST -d '{"nw_src": "10.0.0.2/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"}' http://192.168.1.8:8082/firewall/rules/0000000000000001

#firewall




curl -X PUT http://192.168.1.8:8080/firewall/module/enable/0000000000000031

curl -X POST -d '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP"}' http://192.168.1.8:8080/firewall/rules/0000000000000031


video <br>

https://youtu.be/gIoki9wpsqw
