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

        c1 = net.addController('c1', controller=RemoteController, ip="192.168.0.106", port=6632)
        c2 = net.addController('c2', controller=RemoteController, ip="127.0.0.1", port=6633)
        c3 = net.addController('c3', controller=RemoteController, ip="127.0.0.1", port=6634)

        h1 = net.addHost( 'h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01' )
        h2 = net.addHost( 'h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02' )
        h3 = net.addHost( 'h3', ip='10.0.1.3/8', mac='00:00:00:00:00:03' )
        h4 = net.addHost( 'h4', ip='10.0.1.4/8', mac='00:00:00:00:00:04' )

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
        c2.start()
        c3.start()
        sw_1.start([c1])
        sw_2.start([c1])
        ro_1.start([c2])
        fw_1.start([c3])


        net.start()
        net.staticArp()
        CLI(net)
        net.stop()

    if __name__ == '__main__':
        setLogLevel('info')
    emptyNet()


topos = {'mytopo': (lambda: MyTopo())}
