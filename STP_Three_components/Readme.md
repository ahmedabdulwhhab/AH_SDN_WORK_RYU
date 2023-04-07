#STP switches DPID 1,2,3
<br>
#Firewall DPID 49 (0x31)
<br>
#Router DPID 33 (0x21)
<br>
#simple Switches DPID 5,6
<br>
## CMD
<br>
clear ; sudo ryu-manager   stp_custom.py simple_switch_13_custom.py rest_router_custom.py rest_firewall_custom.py  /home/ubuntu/sdn/sources/flowmanager/flowmanager.py   --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 8086




<br>
  https://youtu.be/BnibijGTgTQ



