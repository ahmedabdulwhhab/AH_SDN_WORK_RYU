#https://github.com/Yi-Tseng/SDN-Work/tree/master/MultiControl/ms
#https://aristasdn.blogspot.com/2019/01/day-12-master-slave-sdn-controller.html
'''
Master App, testing for master controller
'''
# -*- encoding: utf-8 -*-
# file: MasterApp.py

# clear && sudo ryu-manager  controller_1.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py  ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6632 --wsapi-port 8080


# sudo service mongod stop && sudo service mongod start && sudo rm -r data/db/* && sudo mongod --dbpath='/home/ubuntu/sdn/projects/Multi-control/controller_mongo/data/db'

#curl -X GET http://localhost:8081/stats/role/1
#curl -X POST -d '{"dpid": 1, "role":"MASTER"}' http://localhost:8080/stats/role
#curl -X POST -d '{"dpid": switch-dpid, "role":"EQUAL"}'    http://localhost:8080/stats/role
#curl -X POST -d '{"dpid": switch-dpid, "role":"SLAVE"}'    http://localhost:8080/stats/role

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import HANDSHAKE_DISPATCHER
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import ethernet
from ryu.lib.packet import packet
from ryu.controller import dpset
from ryu.ofproto import ofproto_v1_3
from threading import Thread


from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.lib.packet import ether_types
from ryu.lib import hub
#################new
from ryu.lib.packet import ipv4
from ryu.lib.packet import in_proto
import socket
import time
import pymongo




import os
os.system("  sudo lsof -ti tcp:7999  ")
os.system("  sudo pkill -9 -f  tcp:7999  ")
timeout = 10
class MasterApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(MasterApp, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.time_out = 0
        self.current_role = "ofp.OFPCR_ROLE_MASTER"
        self.datapaths = {}
        self.myclient = ""
        self.mydb = ""

        self.mycol = ""

        self.ctrl_id=1
        self.install_pymongo_db()
        self.monitor_thread = hub.spawn(self._monitor)
        
        
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
        self.time_out = 0
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    idle_timeout=self.time_out,   ##new
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    idle_timeout=self.time_out,   ##new
                                    match=match, instructions=inst)
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


        dpid = format(datapath.id, "d").zfill(16)
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
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.time_out = timeout
                #self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.time_out = timeout
                #self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dpid = datapath.id
        print ('dpid ',dpid, 'eth.src ',eth.src,' eth.dst ', eth.dst, ' port ',in_port)




    @set_ev_cls(dpset.EventDP, MAIN_DISPATCHER)
    def on_dp_change(self, ev):

        if ev.enter:
            dp = ev.dp
            dpid = dp.id
            ofp = dp.ofproto
            ofp_parser = dp.ofproto_parser

            print ('dp entered, id is %s' % (dpid))
            self.send_role_request(dp, ofp.OFPCR_ROLE_MASTER, 0)


    @set_ev_cls(ofp_event.EventOFPErrorMsg,
            [HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def on_error_msg(self, ev):
        msg = ev.msg
        #print ('receive a error message: %s' % (msg))
        print("e")

    @set_ev_cls(ofp_event.EventOFPRoleReply, MAIN_DISPATCHER)
    def on_role_reply(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        role = msg.role
        gen_id = msg.generation_id

        if role == ofp.OFPCR_ROLE_EQUAL:
            print ('now is equal')
        elif role == ofp.OFPCR_ROLE_MASTER:
            print ('now is master')
        elif role == ofp.OFPCR_ROLE_SLAVE:
            print ('now is slave')
        print ('for datapath with id , ', dp.id,' gen_id = ',msg.generation_id)

    def send_role_request(self, datapath, role, gen_id):
        ofp_parser = datapath.ofproto_parser
        msg = ofp_parser.OFPRoleRequest(datapath, role, gen_id)
        datapath.send_msg(msg)


##############new code
    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            if(self.current_role=="ofp.OFPCR_ROLE_SLAVE"):
                self.current_role="ofp.OFPCR_ROLE_MASTER"
                for datapath in self.datapaths.values():
                    #self._request_stats(dp)
                    ofp = datapath.ofproto
                    self.send_role_request(datapath, ofp.OFPCR_ROLE_MASTER,0)
                    self.update_pymongo_db(self.current_role)
                    pass
            else:
                self.current_role="ofp.OFPCR_ROLE_SLAVE"
                for datapath in self.datapaths.values():
                    #self._request_stats(dp)
                    ofp = datapath.ofproto
                    self.send_role_request(datapath, ofp.OFPCR_ROLE_SLAVE,0)
                    self.update_pymongo_db(self.current_role)
                    pass                


            hub.sleep(40)       #switch every 40 seconds



    def install_pymongo_db(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["customers"]
        

        mydict = { "contr": str(self.ctrl_id), 
                    "role": self.current_role ,
                    "packet_cnt":""}

        x = self.mycol.insert_one(mydict)
        
        
    def update_pymongo_db(self,current_role):

        
        # Updating fan quantity form 10 to 25.
        #self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["customers"]
        curr_role=current_role
        
        # Updating fan quantity form 10 to 25.
        myfilter = { "contr": str(self.ctrl_id) }
 
        # Values to be updated.
        #newvalues = { "$set": { 'quantity': 25 } }
 
        # Using update_one() method for single
        # updation.
        #collection.update_one(filter, newvalues)
        #for x in  self.mycol.find({},{ "contr": str(self.ctrl_id) }):
        #       for x in self.mycol.find()
                
        newvalues = {  "$set": { 
                    "role": curr_role ,
                    "packet_cnt":""}}
                #print("x = ",x)
        self.mycol.update_one(myfilter, newvalues)
        