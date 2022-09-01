#!/bin/bash
ryu-manager --observe-links --ofp-tcp-listen-port 6633 MasterApp.py ryu.app.simple_switch_13
