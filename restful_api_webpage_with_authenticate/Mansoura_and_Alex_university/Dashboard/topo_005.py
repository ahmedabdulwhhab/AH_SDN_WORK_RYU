"""
sudo python3 py_topo_00.py
sudo ovs-vsctl set Bridge s1 protocols=OpenFlow13
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.link import TCLink  # So we can rate limit links
from mininet.cli import CLI  # So we can bring up the Mininet CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class RoutingTopo(Topo):
    def build(self):
        s1  =self.addSwitch('s1', dpid='0000000000000001',cls=OVSSwitch, protocols='OpenFlow13')
        s2  =self.addSwitch('s2', dpid='0000000000000002',cls=OVSSwitch, protocols='OpenFlow13')
        s21 =self.addSwitch('s21',dpid='0000000000000021',cls=OVSSwitch, protocols='OpenFlow13')
        h1= self.addHost('h1',mac="00:00:00:00:00:01",ip="10.0.0.1/32")
        h2= self.addHost('h2',mac="00:00:00:00:00:02",ip="10.0.0.2/32")
        h3= self.addHost('h3',mac="00:00:00:00:00:03",ip="10.0.0.3/32")
        h4= self.addHost('h4',mac="00:00:00:00:00:04",ip="10.0.0.4/32")
        h5= self.addHost('h5',mac="00:00:00:00:00:05",ip="10.0.0.5/32")
        h6= self.addHost('h6',mac="00:00:00:00:00:06",ip="10.0.0.6/32")        

        # Wire the switches and hosts together. Note there is a loop!
        self.addLink("h1", "s1", bw=20.0, delay='10ms', use_htb=True)
        self.addLink("h2", "s1", bw=25.0, delay='10ms', use_htb=True)
        self.addLink("h3", "s1", bw=25.0, delay='10ms', use_htb=True)
        self.addLink("h5", "s2", bw=11.0, delay='40ms', use_htb=True)
        self.addLink("h6", "s2", bw=15.0, delay='7ms', use_htb=True)
        self.addLink("s1", "s21", bw=5.0, delay='7ms', use_htb=True)
        self.addLink("s2", "s21", bw=5.0, delay='7ms', use_htb=True)
        self.addLink("h4", "s21", bw=5.0, delay='7ms', use_htb=True)
        


if __name__ == "__main__":
        setLogLevel('info')
        topo = RoutingTopo()
        c1 = RemoteController('c1',ip='192.168.127.128',protocol='tcp',port=6644)
        net = Mininet(topo=topo,link=TCLink,controller=c1)
        net.start()
        h1=net.get('h1')
        h2=net.get('h2')
        h3=net.get('h3')
        h4=net.get('h4')
        h5=net.get('h5')
        h6=net.get('h6')        
        #net.start()
        CLI(net)  # Bring up the mininet CLI
        net.stop()

