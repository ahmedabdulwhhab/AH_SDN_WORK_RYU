#!/usr/bin/python

'''

             s1            
    
    s2     s3    s4    s5
          
   h1      h2    h3    h4 h5 h6


s2 - c0
s1,s3,s4,s5 - c1


.start the controllers:

controller1:
------------
ryu-manager --ofp-tcp-listen-port 6653 ryu.app.simple_switch_13 


controller2:
------------

ryu-manager --ofp-tcp-listen-port 6654 L3_switch.py 


test method - generate a ping from h1 to h2
              generate a iperf UDP Parallel connection(50) from h2 to h5  continuously  for every 10 seconds

'''


from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.10.10.0/24')

    info( '*** Adding controller\n' )

    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6654)


    info( '*** Add switches\n')

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)



    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, mac='00:00:00:00:00:01', ip='10.10.10.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, mac='00:00:00:00:00:02', ip='10.10.10.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, mac='00:00:00:00:00:03', ip='10.10.10.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, mac='00:00:00:00:00:04', ip='10.10.10.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, mac='00:00:00:00:00:05', ip='10.10.10.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, mac='00:00:00:00:00:06', ip='10.10.10.6', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s2)
    net.addLink(h2, s3)
    net.addLink(h3, s4)
    net.addLink(h4, s5)
    net.addLink(h5, s5)
    net.addLink(h6, s5)

    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s1, s5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c1])
    net.get('s3').start([c1])
    net.get('s4').start([c1])
    net.get('s5').start([c1])
    net.get('s2').start([c0])

    net.pingAll()
    #start server in h5
    #h1 = net.get('h1')
    #cmd1 = "ping 10.10.10.6 &"
    #h1.cmd(cmd1)


    #Generate some random traffic at interval of 10
    
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')

    cmd1 = "iperf -u -s &"
    h1.cmd(cmd1)
    h2.cmd(cmd1)
    h3.cmd(cmd1)
    h4.cmd(cmd1)
    h5.cmd(cmd1)
    h6.cmd(cmd1)


    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

