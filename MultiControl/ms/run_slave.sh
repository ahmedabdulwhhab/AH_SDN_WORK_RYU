#!/bin/bash
sudo ryu-manager SlaveApp.py controller.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 8081
