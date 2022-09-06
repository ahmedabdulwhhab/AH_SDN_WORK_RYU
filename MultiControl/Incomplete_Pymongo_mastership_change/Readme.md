# To change master ship between controller 1 and controller 2
<br>

# clear && sudo ryu-manager  controller_1.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py  ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6632 --wsapi-port 8080
<br>

# sudo service mongod stop && sudo service mongod start && sudo rm -r data/db/* && sudo mongod --dbpath='/home/ubuntu/sdn/projects/Multi-control/controller_mongo/data/db'
<br>
# clear && sudo ryu-manager  controller_2.py /home/ubuntu/sdn/sources/flowmanager/flowmanager.py  ryu.app.ofctl_rest --observe-links --ofp-tcp-listen-port 6633 --wsapi-port 8081

<br>
# sudo service mongod stop && sudo service mongod start && sudo rm -r data/db/* && sudo mongod --dbpath='/home/ubuntu/sdn/projects/Multi-control/controller_mongo/data/db'
<br>
 python3 local_collection.py

<br>
https://youtu.be/21p0-HLrkow
