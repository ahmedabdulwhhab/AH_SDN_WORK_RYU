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
        s1=self.addSwitch('s1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        h1 = self.addHost('h1',ip='192.168.10.5/24',mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',ip='192.168.10.6/24',mac='00:00:00:00:00:02')
        h3 = self.addHost('h3',ip='192.168.20.7/24',mac='00:00:00:00:00:03')
        h4 = self.addHost('h4',ip='192.168.20.8/24',mac='00:00:00:00:00:04')            




        s1=self.addSwitch('s1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        s2=self.addSwitch('s2',dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
        s11=self.addSwitch('s11',dpid='0000000000000003',cls=OVSSwitch, protocols='OpenFlow13')
        #sc2=self.addSwitch('sc2',dpid='0000000000000004',cls=OVSSwitch, protocols='OpenFlow13')
        s3=self.addSwitch('s3',dpid='0000000000000005',cls=OVSSwitch, protocols='OpenFlow13')
        s4=self.addSwitch('s4',dpid='0000000000000006',cls=OVSSwitch, protocols='OpenFlow13')
        R1=self.addSwitch('R1',dpid='0000000000000021',cls=OVSSwitch, protocols='OpenFlow13')
        F1=self.addSwitch('F1',dpid='0000000000000031',cls=OVSSwitch, protocols='OpenFlow13')

        self.addLink(h1,s4, port1 = 0,port2 = 1)
        self.addLink(h2,s4, port1 = 0,port2 = 2)
        self.addLink(s1,s4, port1 = 1,port2 = 3)
        self.addLink(s1,s2, port1 = 2,port2 = 4)
        #self.addLink(sw1,sc2, port1 = 3,port2 = 1)
        self.addLink(s1,s11, port1 = 3,port2 = 1)
        self.addLink(s2,s11, port1 = 1,port2 = 2)
        #self.addLink(sw2,sc2, port1 = 2,port2 = 2)
        self.addLink(s2,R1, port1 = 3,port2 = 1)
        self.addLink(F1,R1, port1 = 1,port2 = 2)
        self.addLink(s3,F1, port1 = 1,port2 = 2)
        self.addLink(s3,h3, port1 = 2,port2 = 0)
        self.addLink(s3,h4, port1 = 3,port2 = 0)





if __name__ == "__main__":
        setLogLevel('info')
        topo = RoutingTopo()
        c1 = RemoteController('c1',ip='127.0.0.1',port=6633)
        net = Mininet(topo=topo,controller=c1)
        net.start()
        h1=net.get('h1')
        h2=net.get('h2')
        h3=net.get('h3')
        h4=net.get('h4')
        h1.cmd(' ip route add default via 192.168.10.1')
        h2.cmd(' ip route add default via 192.168.10.1')
        h3.cmd(' ip route add default via 192.168.20.1')
        h4.cmd(' ip route add default via 192.168.20.1')
     

        CLI(net)
        net.stop()