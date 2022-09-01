#!/bin/bash
 sudo ryu-manager --observe-links --ofp-tcp-listen-port 6633 SlaveApp.py controller.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py --observe-links --wsapi-port 8081

