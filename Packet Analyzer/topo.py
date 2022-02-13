#!/usr/bin/env python
#multi controller
#clear && ryu-manager ./sdn/ryu-controller/muzixing/ryu/ryu/app/multipath.py  --observe-links --verbose --ofp-tcp-listen-port 6633
#clear && ryu-manager ./sdn/ryu-controller/ah_learn_ryu_00/ryu_multipath.py --observe-links --ofp-tcp-listen-port 6633

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm

if '__main__' == __name__:
    net = Mininet(controller=RemoteController)

    c0 = net.addController('c0', port=6633)
    c1 = net.addController('c1', port=6634)


    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')
    s8 = net.addSwitch('s8')
    s9 = net.addSwitch('s9')    

    h1 = net.addHost('h1',mac='00:00:01:00:00:00')  
    h2 = net.addHost('h2',mac='00:00:02:00:00:00')
    h3 = net.addHost('h3',mac='00:00:03:00:00:00')
    h4 = net.addHost('h4',mac='00:00:04:00:00:00')
    h5 = net.addHost('h5',mac='00:00:05:00:00:00')
    h6 = net.addHost('h6',mac='00:00:06:00:00:00')
    h7 = net.addHost('h7',mac='00:00:07:00:00:00')
    h8 = net.addHost('h8',mac='00:00:08:00:00:00')
    h9 = net.addHost('h9',mac='00:00:09:00:00:00')    

    net.addLink(s1, h1)
    net.addLink(s2, h2)
    net.addLink(s3, h3)
    net.addLink(s4, h4)
    net.addLink(s5, h5)
    net.addLink(s6, h6)
    net.addLink(s7, h7)
    net.addLink(s8, h8)
    net.addLink(s9, h9)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)
    net.addLink(s4, s5)
    net.addLink(s5, s6)
    net.addLink(s6, s7)
    net.addLink(s7, s8)
    net.addLink(s8, s9)




    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])
    c1.start()
    s5.start([c1])
    s6.start([c1])    
    s7.start([c1])
    s8.start([c1])        
    s9.start([c1])
        
    
    #net.startTerms()

    CLI(net)

    net.stop()
