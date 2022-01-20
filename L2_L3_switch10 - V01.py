#https://github.com/rafaelsilvag/Rypace/blob/master/app/rypace_switch_v01.py

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



#sudo ovs-ofctl -O openflow10 dump-flows s1
#sudo mn -c && sudo mn --controller=remote,ip=192.168.1.11 --switch=ovsk,protocols=OpenFlow10 --topo=linear,3 --mac
#sudo mn -c && sudo mn --controller=remote,ip=192.168.1.11 --switch=ovsk,protocols=OpenFlow10 --topo=linear,3,2 --mac
# clear && sudo ryu-manager --observe-links --verbose flowmanager_1.0/AH_SDN_WORK_RYU/flowmanager_1.0/flowmanager.py

import logging
import struct

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.ip import ipv4_to_bin, ipv4_to_str
from ryu.lib.packet.icmp import icmp
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import icmp
from ryu.lib import addrconv


class RypaceSwitch(app_manager.RyuApp):
    # Definicao da versao do OpenFlow - MK apenas suporta versao 1.0
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    #Metodo construtor
    def __init__(self, *args, **kwargs):
        super(RypaceSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        

        
    def ipv4_text_to_int(self, ip_text):
        if ip_text == 0:
            return ip_text
        assert isinstance(ip_text, str)
        return struct.unpack('!I', addrconv.ipv4.text_to_bin(ip_text))[0]

    def ipv4_int_to_text(ip_int):
        assert isinstance(ip_int, (int, long))
        return addrconv.ipv4.bin_to_text(struct.pack('!I', ip_int))

    # Adicionar regra na tabela  Fluxo.
    def add_flow(self, datapath, in_port, eth, ip_v4, actions):
        ofproto = datapath.ofproto
        idleTimeout = 20
        hardTimeout = 20
        """
   ================ ==================================================
    Attribute        Description
    ================ ==================================================
    wildcards        Wildcard fields.
    (match fields)   For the available match fields,
                     please refer to the following.
    ================ ==================================================

    ================ =============== ==================================
    Argument         Value           Description
    ================ =============== ==================================
    in_port          Integer 16bit   Switch input port.
    dl_src           MAC address     Ethernet source address.
    dl_dst           MAC address     Ethernet destination address.
    dl_vlan          Integer 16bit   Input VLAN id.
    dl_vlan_pcp      Integer 8bit    Input VLAN priority.
    dl_type          Integer 16bit   Ethernet frame type.
    nw_tos           Integer 8bit    IP ToS (actually DSCP field, 6 bits).
    nw_proto         Integer 8bit    IP protocol or lower 8 bits of
                                     ARP opcode.
    nw_src           IPv4 address    IP source address.
    nw_dst           IPv4 address    IP destination address.
    tp_src           Integer 16bit   TCP/UDP source port.
    tp_dst           Integer 16bit   TCP/UDP destination port.
    nw_src_mask      Integer 8bit    IP source address mask
                                     specified as IPv4 address prefix.
    nw_dst_mask      Integer 8bit    IP destination address mask
                                     specified as IPv4 address prefix.
    ================ =============== ==================================
    """
        if(ip_v4):
            nw_src = self.ipv4_text_to_int(ip_v4.src)
            nw_dst = self.ipv4_text_to_int(ip_v4.dst)

            match = datapath.ofproto_parser.OFPMatch(
                in_port=in_port,
                dl_type=eth.ethertype,
                dl_src=haddr_to_bin(eth.src),
                dl_dst=haddr_to_bin(eth.dst),
                nw_proto=ip_v4.proto,
                nw_src=nw_src,
                nw_dst=nw_dst,
            )
        else:
            match = datapath.ofproto_parser.OFPMatch(
                in_port=in_port, dl_type=eth.ethertype,
                dl_src=haddr_to_bin(eth.src),
                dl_dst=haddr_to_bin(eth.dst),)

            idleTimeout = 20
            hardTimeout = 20

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=idleTimeout, hard_timeout=hardTimeout,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)

        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        # Captura o pacote recebido pelo Controlador.
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        # Captura informacoes de IPv4 ou IPv6, TCP, UDP e ICMP, caso existam. Se o pacote
        # nao ter, a variavel recebera None
        ip_v4 = pkt.get_protocol(ipv4.ipv4)
        ip_v6 = pkt.get_protocol(ipv6.ipv6)
        tcp_port = pkt.get_protocol(tcp.tcp)
        udp_port = pkt.get_protocol(udp.udp)
        icmp_protocol = pkt.get_protocol(icmp.icmp)

        dst = eth.dst
        src = eth.src


        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {})

        # Log Packet-In
        self.logger.info("Packet(%s) in  %s %s %s", dpid, src, dst, msg.in_port)
        #self.logger.info(self.mac_to_port)
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = msg.in_port


        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]



        # install a flow to avoid packet_in next time
        if (out_port != ofproto.OFPP_FLOOD):
            self.add_flow(datapath, msg.in_port, eth, ip_v4, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
        datapath.send_msg(out)
            
            
 #######################################################################         
 