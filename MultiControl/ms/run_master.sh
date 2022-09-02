#!/bin/bash
sudo ryu-manager MasterApp.py controller.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py  ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6632 --wsapi-port 8080