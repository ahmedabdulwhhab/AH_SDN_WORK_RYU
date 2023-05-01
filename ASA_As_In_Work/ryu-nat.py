# The code is this file is derived from:
# https://raw.githubusercontent.com/osrg/ryu/master/ryu/app/simple_switch.py
# which is protected by the Apache 2.0 license.  
# The modifications are protected by the GENI license.
# Both licenses are included below.
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
# limitations under the License.import logging

# Copyright (c) 2014 Raytheon BBN Technologies

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and/or hardware specification (the "Work") to
# deal in the Work without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Work, and to permit persons to whom the Work
# is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Work.

# THE WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE WORK OR THE USE OR OTHER DEALINGS
# IN THE WORK.

"""
An OpenFlow 1.0 L2 NAT implementation.
"""
import logging

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp 
from ryu.lib.packet import icmp
from ryu.controller import dpset
from netaddr import *
from collections import namedtuple

class NAT(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    global Ipv4_addr 
    Ipv4_addr = namedtuple("Ipv4_addr", ["addr", "port"])    

    def __init__(self, *args, **kwargs):
        super(NAT, self).__init__(*args, **kwargs)
        global ex_ip
        ex_ip = "128.128.128.100"
        global maps
        maps = {}
        global ports
        ports = range(50000,60000)
    def add_flow(self, datapath, match, actions, priority=0, hard_timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, actions=actions, hard_timeout=hard_timeout, cookie=0, command=ofproto.OFPFC_ADD)
        datapath.send_msg(mod)
        self.logger.debug("add_flow:"+str(mod))

    @set_ev_cls(dpset.EventDP, dpset.DPSET_EV_DISPATCHER)
    def _event_switch_enter_handler(self, ev):
        dl_type_arp = 0x0806
        dl_type_ipv4 = 0x0800
        dl_type_ipv6 = 0x86dd
        dp = ev.dp
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        self.logger.info("switch connected %s", dp)

        # pass packet directly
        actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]	

        # arp
        match = parser.OFPMatch(dl_type = dl_type_arp)

        self.add_flow(dp, match, actions)

        # ipv6
        match = parser.OFPMatch(dl_type = dl_type_ipv6)
        self.add_flow(dp, match, actions)

        # igmp
        match = parser.OFPMatch(dl_type = dl_type_ipv4, nw_proto = 2)

        self.add_flow(dp, match, actions)

        # do address translation for following types of packet
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]

        # icmp
        match = parser.OFPMatch(dl_type = dl_type_ipv4, nw_proto = 1)

        self.add_flow(dp, match, actions)

        # tcp
        match = parser.OFPMatch(dl_type = dl_type_ipv4, nw_proto = 6)

        self.add_flow(dp, match, actions)

        # udp
        match = parser.OFPMatch(dl_type = dl_type_ipv4, nw_proto = 17)

        self.add_flow(dp, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        #self.logger.info("msg in")

        message = ev.msg
        #self.logger.info("message %s", message)
        datapath = message.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(message.data)
        #self.logger.info("pkt %s", pkt)
        ip = pkt.get_protocol(ipv4.ipv4)
        #self.logger.info("ipv4 %s", ip)


        bitmask = "24"
        src_match = IPNetwork("10.10.1.0"+ "/" + bitmask)
        dst_match = ex_ip

        if message.in_port == ofproto.OFPP_LOCAL :
             out_port = 1
        else :
             out_port = ofproto.OFPP_LOCAL

        if ip.proto == 17 or ip.proto == 6 :
                t = pkt.get_protocol(tcp.tcp)
                #self.logger.info("tcp %s", t)
                u = pkt.get_protocol(udp.udp)
                #self.logger.info("udp %s", u)

            if IPNetwork( ip.src + "/" + bitmask ) == src_match :
			#print "convert src"
            src_port = t.src_port if t else u.src_port
			#print src_port
            ipv4_addr = Ipv4_addr(addr=ip.src , port=src_port)

            if ipv4_addr in maps :
                port = maps[ipv4_addr]
            else:
                port = ports.pop()
                maps[ ipv4_addr ] = port
                maps[ port ] = ipv4_addr
            print(f"Created mapping: {ipv4_addr.addr} {ipv4_addr.port} to {ex_ip} {port}")

            actions = [
				parser.OFPActionSetNwSrc( self.ipv4_to_int(ex_ip) ),
				parser.OFPActionSetTpSrc( port ),
				parser.OFPActionOutput(out_port)
				]
            data = None;
					# Check the buffer_id and if needed pass the whole message down
            if message.buffer_id == 0xffffffff:
                  data=message.data
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, data=data, in_port=message.in_port,actions=actions)
            datapath.send_msg(out)
            return
        elif ip.dst  == dst_match :
                #print "convert dst"
                dst_port = t.dst_port if t else u.dst_port
					#print dst_port

        if dst_port in maps :
            ipv4_addr = maps[dst_port]
        else :
            print "Dropping msg as dst is not understood"
            return
        actions = [
							parser.OFPActionSetNwDst( self.ipv4_to_int(ipv4_addr.addr) ),
							parser.OFPActionSetTpDst( ipv4_addr.port ),
							parser.OFPActionOutput(out_port)
							]
        data = None;
					# Check the buffer_id and if needed pass the whole message down
        if message.buffer_id == 0xffffffff:
            data=message.data
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, data=data, in_port=message.in_port,actions=actions)
        datapath.send_msg(out)
					return

	elif ip.proto == 1 :
		ping = pkt.get_protocol(icmp.icmp)
        	#self.logger.info("icmp %s", ping)
		
		if IPNetwork( ip.src + "/" + bitmask ) == src_match :
			#print "convert src"

			icmp_id = ping.data.id
			#print icmp_id

			if not icmp_id in maps :
				maps[icmp_id] = ip.src

			actions = [
                                parser.OFPActionSetNwSrc( self.ipv4_to_int(ex_ip) ),
                                parser.OFPActionOutput(out_port)
                                ]
                        data = None;
                        # Check the buffer_id and if needed pass the whole message down
                        if message.buffer_id == 0xffffffff:
                                data=message.data
                        out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, data=data,  in_port=message.in_port,actions=actions)
                        datapath.send_msg(out)
                        return

		elif ip.dst  == dst_match :
			#print "convert dst"

			icmp_id = ping.data.id
                        #print icmp_id

			if icmp_id in maps :
				dst_addr = maps[icmp_id]
			else :
				print "Dropping msg as dst is not understood"
				return
						
			actions = [
                                parser.OFPActionSetNwDst( self.ipv4_to_int(dst_addr) ),
                                parser.OFPActionOutput(out_port)
                                ]
                        data = None;
                        # Check the buffer_id and if needed pass the whole message down
                        if message.buffer_id == 0xffffffff:
                                data=message.data
                        out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, data=data, in_port=message.in_port,actions=actions)
                        datapath.send_msg(out)
                        return
	else:
		#print "other"
		actions = [parser.OFPActionOutput(out_port)]
                data = None;
                # Check the buffer_id and if needed pass the whole message down
                if message.buffer_id == 0xffffffff:
                	data=message.data
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, data=data, in_port=message.in_port,actions=actions)
                datapath.send_msg(out)		

    def ipv4_to_str(self, integre):
	ip_list = [str((integre >> (24 - (n * 8)) & 255)) for n in range(4)]
        return '.'.join(ip_list)

    def ipv4_to_int(self, string):
       	ip = string.split('.')
       	assert len(ip) == 4
       	i = 0
       	for b in ip:
    		b = int(b)
        	i = (i << 8) | b
        return i
