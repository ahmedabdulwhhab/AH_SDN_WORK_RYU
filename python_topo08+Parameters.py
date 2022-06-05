#clear && ryu-manager ryu.app.simple_monitor_13 --ofp-tcp-listen-port 6644
#clear && ryu-manager --ofp-tcp-listen-port 6644 ryu.app.simple_switch_13
#sudo mn --topo tree,depth=1,fanout=3 --switch ovsk --controller ryu --mac --link tc,bw=100,delay=20ms
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import OVSSwitch, Controller, RemoteController

class RoutingTopo(Topo):
        def build(self):
                s1=self.addSwitch('s1',dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
                h1= self.addHost('h1',mac="00:00:00:00:00:02",ip="10.0.0.2/24")
                h2= self.addHost('h2',mac="00:00:00:00:00:03",ip="10.0.0.3/24")
                h3= self.addHost('h3',mac="00:00:00:00:00:04",ip="10.0.0.4/24")
                h4= self.addHost('h4',mac="00:00:00:00:00:05",ip="10.0.0.5/24")
                h5= self.addHost('h5',mac="00:00:00:00:00:06",ip="10.0.0.6/24")
                h6= self.addHost('h6',mac="00:00:00:00:00:07",ip="10.0.0.7/24")
                h7= self.addHost('h7',mac="00:00:00:00:00:08",ip="10.0.0.8/24")                   

                s2=self.addSwitch('s2',dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
                self.addLink(h1,s1, port1 = 0,port2 = 1,bw=10.0, delay='10ms', use_htb=True)
                self.addLink(h2,s1, port1 = 0,port2 = 2,bw=20.0, delay='20ms', use_htb=True)
                self.addLink(h3,s1, port1 = 0,port2 = 3,bw=30.0, delay='30ms', use_htb=True)                
                self.addLink(h4,s2, port1 = 0,port2 = 1,bw=40.0, delay='40ms', use_htb=True)
                self.addLink(h5,s2, port1 = 0,port2 = 2,bw=50.0, delay='50ms', use_htb=True)
                self.addLink(h6,s2, port1 = 0,port2 = 3,bw=60.0, delay='60ms', use_htb=True)                
                self.addLink(s1,s2, port1 = 4,port2 = 4,bw=70.0, delay='100ms', use_htb=True)                                
                s3=self.addSwitch('s3',dpid='0000000000000003',cls=OVSSwitch, protocols='OpenFlow13')
                s4=self.addSwitch('s4',dpid='0000000000000004',cls=OVSSwitch, protocols='OpenFlow13')                
                s5=self.addSwitch('s5',dpid='0000000000000005',cls=OVSSwitch, protocols='OpenFlow13', failMode='standalone')
                self.addLink(s2,s3, port1 = 5,port2 = 1,bw=70.0, delay='100ms', use_htb=True)                                
                self.addLink(s3,s4, port1 = 2,port2 = 1,bw=70.0, delay='100ms', use_htb=True)                                
             
                ss_link = {'bw':400,'loss':0,'delay':'100ms'}
                self.addLink(s4,s5, port1 = 2,port2 = 2,**ss_link)
                self.addLink(h7, s5, port1 = 0,port2 = 1, bw=10, delay='70ms', loss=0, use_htb=True)    
#h1 ping h7  10+100+100+100+100+70=480*2=960 ms
if __name__ == "__main__":
        setLogLevel('info')
        topo = RoutingTopo()
        c1 = RemoteController('c1',ip='127.0.0.1',port=6644)
        net = Mininet(topo=topo, link=TCLink, controller=c1)
        net.start()
        h1=net.get('h1')
        h2=net.get('h2')
        h3=net.get('h3')
        h4=net.get('h4')
        h5=net.get('h5')
        h6=net.get('h6')
        h7=net.get('h7')        

        CLI(net)
        net.stop()


############### case 1
#clear && sudo mn --topo tree,depth=1,fanout=3 --switch ovsk --controller ryu --mac --link tc,bw=1,delay=20ms
#*** Adding links: (1.00Mbit 20ms delay) 
#mininet> iperf h1 h3
#*** Iperf: testing TCP bandwidth between h1 and h3 
#*** Results: ['958 Kbits/sec', '1.59 Mbits/sec']

############### case 2
#clear && sudo mn --topo tree,depth=1,fanout=3 --switch ovsk --controller ryu --mac --link tc,bw=10,delay=20ms
#*** Adding links: (10.00Mbit 20ms delay) 
#mininet> iperf h1 h3
#*** Iperf: testing TCP bandwidth between h1 and h3 
#*** Results: ['9.32 Mbits/sec', '11.4 Mbits/sec']
#mininet> 

############### case 3
#clear && sudo mn --topo tree,depth=1,fanout=3 --switch ovsk --controller ryu --mac --link tc,bw=100,delay=20ms
#*** Adding links: (100.00Mbit 20ms delay) 
#mininet> iperf h1 h3
#*** Iperf: testing TCP bandwidth between h1 and h3 
#*** Results: ['64.5 Mbits/sec', '75.1 Mbits/sec']
#mininet> 

############### case 4
#clear && sudo mn --topo tree,depth=1,fanout=3 --switch ovsk --controller ryu --mac --link tc,bw=100,delay=20ms
#*** Adding links: (1000.00Mbit 20ms delay)  
#mininet> iperf h1 h3
#*** Iperf: testing TCP bandwidth between h1 and h3 
#*** Results: ['295 Mbits/sec', '299 Mbits/sec']
#mininet> 



#iperf
#xterm h4
#  iperf -u -s


#xterm h1
#   iperf -u -c 10.0.0.5 -b 10m -i 10 -t 30
