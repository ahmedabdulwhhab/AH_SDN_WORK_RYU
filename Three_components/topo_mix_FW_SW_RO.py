#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch
from mininet.topo import Topo


class MyTopo(Topo):
    "Simple topology example."

    def emptyNet():
        net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

        c1 = net.addController('c1', controller=RemoteController, ip="192.168.1.8", port=6632)
        

        h1 = net.addHost( 'h1', ip='10.0.0.2/24', mac='00:00:00:00:00:01' )
        h2 = net.addHost( 'h2', ip='10.0.0.3/24', mac='00:00:00:00:00:02' )
        h3 = net.addHost( 'h3', ip='100.0.0.2/8', mac='00:00:00:00:00:03' )
        h4 = net.addHost( 'h4', ip='100.0.0.3/8', mac='00:00:00:00:00:04' )

        # For 2 host 2 switch Topology



        sw_1 = net.addSwitch('sw_1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        sw_2 = net.addSwitch('sw_2',dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
        ro_1 = net.addSwitch('ro_1',dpid='0000000000000021',cls=OVSSwitch, protocols='OpenFlow13')
        fw_1 = net.addSwitch('fw_1',dpid='0000000000000031',cls=OVSSwitch, protocols='OpenFlow13')


        sw_1.linkTo(h1)
        sw_1.linkTo(h2)
        sw_2.linkTo(h3)
        sw_2.linkTo(h4)

        sw_1.linkTo(fw_1)
        fw_1.linkTo(ro_1)
        sw_2.linkTo(ro_1)

        net.build()
        c1.start()

        sw_1.start([c1])
        sw_2.start([c1])
        ro_1.start([c1])
        fw_1.start([c1])
        h1.cmd('ip route add default via 10.0.0.1')
        h2.cmd('ip route add default via 10.0.0.1')
        h3.cmd('ip route add default via 100.0.0.1')
        h4.cmd('ip route add default via 100.0.0.1')


        net.start()
        net.staticArp()
        CLI(net)
        net.stop()

    if __name__ == '__main__':
        setLogLevel('info')
    emptyNet()


topos = {'mytopo': (lambda: MyTopo())}
