# Multi-Control and master salve.
# Master Slave SDN Controller Architecture
Here Master App which only make check whether I am master or not
<br> <b>
  
and slave App which only make check whether I am slave or not
<br> <b>

# Steps
  1) run mininet topo (modify your two machines IP (for me I have single machine one is 192.168.0.103 and the other is local host 127.0.0.1)
  2) modify layer 2 or layer 3 in shell file (run_slave.sh) and (run_master.sh)
  3) Add ofctl_rest
  4) Send Curl to switch to different role.
  
<br>
  # sudo ryu-manager SlaveApp.py controller.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 8081
<br>
#curl -X GET http://localhost:8081/stats/role/1
  <br>
#curl -X POST -d '{"dpid": 1, "role":"MASTER"}' http://localhost:8081/stats/role
  <br>
#curl -X POST -d '{"dpid": switch-dpid, "role":"EQUAL"}'    http://localhost:8081/stats/role
  <br>
#curl -X POST -d '{"dpid": switch-dpid, "role":"SLAVE"}'    http://localhost:8081/stats/role
  <br>
