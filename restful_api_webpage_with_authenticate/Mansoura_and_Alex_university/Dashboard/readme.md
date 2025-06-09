<br>
terminal (1) to run TOPO
<br>

 clear && sudo mn -c ;sudo mn --controller=remote,ip=192.168.127.133:6644 --mac -i 10.0.0.0/24 --switch=ovsk,protocols=OpenFlow13 --topo=single,4
<br>
terminal (2) to run ryu
<br>
 sudo ryu-manager ryu.app.rest_firewall  ryu.app.ofctl_rest /home/ubuntu/sdn/sources/flowmanager/flowmanager.py  --ofp-tcp-listen-port 6644 --wsapi-port 8085 --observe-links


<br>
<br>
terminal (3) to run listener at port 5000
<br>

cd dashboard
python app.py

<br>
