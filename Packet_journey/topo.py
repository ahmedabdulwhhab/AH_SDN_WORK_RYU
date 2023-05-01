
"""
 clear; sudo ryu-manager ryu.app.rest_router  ryu.app.ofctl_rest   /home/ubuntu/sdn/sources/flowmanager/flowmanager.py    --observe-links --ofp-tcp-listen-port 6632 --wsapi-port 8080

"""

#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topo import Topo


class RoutingTopo(Topo):
 def build(self):

        # Add switches
        r1 = self.addSwitch('r1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        r2 = self.addSwitch('r2',dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
        r3 = self.addSwitch('r3',dpid='0000000000000003',cls=OVSSwitch, protocols='OpenFlow13')
 
        # Add hosts
        h1 = self.addHost('h1',ip='172.16.20.10/24',mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',ip='172.16.10.10/24',mac='00:00:00:00:00:02')
        h3 = self.addHost('h3',ip='192.168.30.10/24',mac='00:00:00:00:00:03')


        self.addLink(h1,r1, port1 = 0,port2 = 1)
        self.addLink(h2,r2, port1 = 0,port2 = 1)
        self.addLink(h3,r3, port1 = 0,port2 = 1)
        self.addLink(r1,r2, port1 = 2,port2 = 2)
        self.addLink(r3,r2, port1 = 2,port2 = 3)

                





if __name__ == "__main__":
        setLogLevel('info')
        topo = RoutingTopo()
        c1 = RemoteController('c1',ip='127.0.0.1',port=6632)
        net = Mininet(topo=topo,controller=c1)
        net.start()
        h1=net.get('h1')
        h2=net.get('h2')
        h3=net.get('h3')
        h1.cmd(' ip route add default via 172.16.20.1')
        h2.cmd(' ip route add default via 172.16.10.1')
        h3.cmd(' ip route add default via 192.168.30.1')

     

        CLI(net)
        net.stop()