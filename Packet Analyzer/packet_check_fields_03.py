
#sudo mn -c &&sudo mn --controller=remote,ip=192.168.1.10 --switch=ovsk,protocols=OpenFlow13 --topo=linear,3


# clear && sudo ryu-manager  --ofp-tcp-listen-port 6633  --observe-links  /home/ubuntu/sdn/sources/flowmanager/flowmanager.py /home/ubuntu/sdn/projects/packet_analyzer/app3.py


#ubuntu@ubuntu:~/sdn/nat$ sudo ryu-manager packet_check_fields.py ../flowmanager/flowmanager.py  --observe-links
#tcp
#h3 
#iperf -s
#h1 
#iperf -c 10.0.0.3 -p 5001


#udp
#iperf -u -s
#iperf -u -c 10.0.0.3 -b 10m -i 10 -t 30


#

# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

from ryu.lib.packet import in_proto
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import arp
from ryu.ofproto import inet

idle_time=40

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.en_clear_flow_entry = False

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    def add_flow(self, datapath, priority, match, actions, buffer_id=None): #modify flow entry
        # print ("Adding flow ", match, actions)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        print("en_clear_flow_entry = ",self.en_clear_flow_entry)
        if buffer_id:
            if(self.en_clear_flow_entry):
                mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,idle_timeout=idle_time,#*datapath.id,
                                    instructions=inst)
            else:
                mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            if(self.en_clear_flow_entry):
                mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, idle_timeout=idle_time,#*datapath.id
                                    instructions=inst)
            else:
                mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match,instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:

            # check IP Protocol and create a match for IP
            #if eth.ethertype == ether_types.ETH_TYPE_IP:
                #ip = pkt.get_protocol(ipv4.ipv4)
                pkt_arp = pkt.get_protocol(arp.arp)
                pkt_icmp = pkt.get_protocol(icmp.icmp)
                pkt_ip = pkt.get_protocol(ipv4.ipv4)
                pkt_tcp = pkt.get_protocol(tcp.tcp)
                pkt_udp = pkt.get_protocol(udp.udp)
                #skip_arp_request = False  
                
                if pkt_arp:
                    print("pkt_arp = ",pkt_arp)
                    
                    
                    if pkt_arp.opcode == arp.ARP_REPLY:
                        srcip = pkt_arp.src_ip
                        dstip = pkt_arp.dst_ip
                        #skip_arp_request = True
                        match = parser.OFPMatch(eth_type=0x0806, arp_spa=srcip, arp_tpa=dstip)
                        actions = [parser.OFPActionSetField(arp_tpa=dstip), #IP_TO_MAC_TABLE[target_ip]),
                        parser.OFPActionSetField(arp_spa=srcip),
                        #parser.OFPActionSetField(udp_src=nat_port),
                        parser.OFPActionOutput(out_port)] 
            
                # if ICMP Protocol
                elif pkt_icmp:
                    print("pkt_icmp = ",pkt_icmp)
                    srcip = pkt_ip.src
                    dstip = pkt_ip.dst
                    match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=srcip, ipv4_dst=dstip, ip_proto=inet.IPPROTO_ICMP)
                    actions = [parser.OFPActionSetField(ipv4_dst=dstip), #IP_TO_MAC_TABLE[target_ip]),
                       parser.OFPActionSetField(ipv4_src=srcip),
                       #parser.OFPActionSetField(udp_src=nat_port),
                       parser.OFPActionOutput(out_port)] 
            
                #  if TCP Protocol
                elif pkt_tcp:
                    print("pkt_tcp = ",pkt_tcp)
                    srcip = pkt_ip.src
                    dstip = pkt_ip.dst                
                    t = pkt.get_protocol(tcp.tcp)
                    match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=srcip, ipv4_dst=dstip,ip_proto=inet.IPPROTO_TCP, tcp_src=t.src_port, tcp_dst=t.dst_port,)
                    actions = [parser.OFPActionSetField(ipv4_dst=dstip), #IP_TO_MAC_TABLE[target_ip]),
                       parser.OFPActionSetField(ipv4_src=srcip),
                       parser.OFPActionSetField(tcp_src=t.src_port),
                       parser.OFPActionSetField(tcp_dst=t.dst_port),
                       parser.OFPActionOutput(out_port)]
            
                #  If UDP Protocol 
                elif pkt_udp:
                    print("pkt_udp = ",pkt_udp)
                    srcip = pkt_ip.src
                    dstip = pkt_ip.dst
                    u = pkt.get_protocol(udp.udp)
                    match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_src=srcip, ipv4_dst=dstip, ip_proto=inet.IPPROTO_UDP, udp_src=u.src_port, udp_dst=u.dst_port,)            
                    actions = [parser.OFPActionSetField(ipv4_dst=dstip), #IP_TO_MAC_TABLE[target_ip]),
                       parser.OFPActionSetField(ipv4_src=srcip),
                       parser.OFPActionSetField(udp_src=u.src_port),
                       parser.OFPActionSetField(udp_dst=u.dst_port),
                       parser.OFPActionOutput(out_port)]
#                else:
#                    print ("pkt is ",pkt)
#                    print("eth.ethertype ", eth.ethertype)
                
                
                # verify if we have a valid buffer_id, if yes avoid to send both
                # flow_mod & packet_out
                if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                    self.en_clear_flow_entry=True
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                    return
                else:
                    self.en_clear_flow_entry=True
                    self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
