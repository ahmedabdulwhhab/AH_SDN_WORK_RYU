#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topo import Topo


class MyTopo(Topo):
    "Simple topology example."

    def emptyNet():
        net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

        c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6633)


        # h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
        # h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )        
        # For 4 host four switch Topology

        h1 = net.addHost('h1',ip='192.168.10.5/24',mac='00:00:00:00:00:01')
        h2 = net.addHost('h2',ip='192.168.10.6/24',mac='00:00:00:00:00:02')
        h3 = net.addHost('h3',ip='192.168.20.7/24',mac='00:00:00:00:00:03')
        h4 = net.addHost('h4',ip='192.168.20.8/24',mac='00:00:00:00:00:04')
        sw1 = net.addSwitch('sw1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        sw2 = net.addSwitch('sw2',dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
        sw3 = net.addSwitch('sw3',dpid='0000000000000003',cls=OVSSwitch, protocols='OpenFlow13')
        sc1 = net.addSwitch('sc1',dpid='0000000000000004',cls=OVSSwitch, protocols='OpenFlow13')
        sc2 = net.addSwitch('sc2',dpid='0000000000000005',cls=OVSSwitch, protocols='OpenFlow13')
        RGW_1 = net.addSwitch('RGW_1',dpid='0000000000000021',cls=OVSSwitch, protocols='OpenFlow13')
        FW_1 = net.addSwitch('FW_1',dpid='0000000000000031',cls=OVSSwitch, protocols='OpenFlow13')


        sw1.linkTo(h1)
        sw1.linkTo(h2)
        sw1.linkTo(sc1)     #yes
        sw1.linkTo(sc2)     #yes
        # #############################
        sw3.linkTo(h3)
        sw3.linkTo(h4)
        sw2.linkTo(sc1)     #yes
        
        # #############################

        # ##########################        
        sw2.linkTo(RGW_1)   #yes     
        FW_1.linkTo(RGW_1)   #yes     
        sw3.linkTo(FW_1)   #yes     
        # sc2.linkTo(RGW_1)   #yes     
        # #sc2.linkTo(RGW_2)        
        #############################        
        #RGW_1.linkTo(RGW_3)
        #RGW_2.linkTo(RGW_3)


        net.build()
        c1.start()

        sw1.start([c1])
        sw2.start([c1])
        sw3.start([c1])
        sc1.start([c1])
        sc2.start([c1])
        RGW_1.start([c1])
        FW_1.start([c1])
        #RGW_3.start([c1])
        h1.cmd('ip route add default via 192.168.10.1')
        h2.cmd('ip route add default via 192.168.10.1')
        h3.cmd('ip route add default via 192.168.20.1')
        h4.cmd('ip route add default via 192.168.20.1')

        net.start()
        # net.staticArp()
        CLI(net)
        net.stop()

    if __name__ == '__main__':
        setLogLevel('info')
    emptyNet()


topos = {'mytopo': (lambda: MyTopo())}
