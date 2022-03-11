#sudo mn -c && sudo python3 /home/ubuntu/sdn/projects/packet_analyzer/l4Switch/topo.py

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm

if '__main__' == __name__:
    net = Mininet(controller=RemoteController)

    c0 = net.addController('c0', port=6633)
    c1 = net.addController('c1', port=6653)


    H1 = net.addHost('h1', ip = '10.0.0.1', mac = '00:00:00:00:00:01')
    H2 = net.addHost('h2', ip = '10.0.0.2', mac = '00:00:00:00:00:02')
    H3 = net.addHost('h3', ip = '10.0.0.3', mac = '00:00:00:00:00:03')
    H4 = net.addHost('h4', ip = '10.0.0.4', mac = '00:00:00:00:00:04')

    print('***Adding Switch \n')
    S1 = net.addSwitch('s1')
    S2 = net.addSwitch('s2')
    S3 = net.addSwitch('s3')
    S4 = net.addSwitch('s4')    

    net.addLink(H1,S1)
    net.addLink(H2,S2)
    net.addLink(H3,S3)
    net.addLink(H4,S4)
    net.addLink(S1,S2)
    net.addLink(S2,S3)
    net.addLink(S3,S4)
    net.addLink(S4,S1)




    net.build()
    c0.start()
    S1.start([c1])
    S2.start([c1])
    S3.start([c1])
    S4.start([c1])
    c1.start()
#    s5.start([c1])
#    s6.start([c1])    
#    s7.start([c1])
#    s8.start([c1])        
#    s9.start([c1])
        
    
    #net.startTerms()

    CLI(net)

    net.stop()
