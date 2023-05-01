#set ip for ports of r1
curl -X POST -d '{"address":"172.16.20.1/24"}' http://localhost:8080/router/0000000000000001

curl -X POST -d '{"address": "172.16.30.30/24"}' http://localhost:8080/router/0000000000000001

#set ip for ports of r2
curl -X POST -d '{"address":"172.16.10.1/24"}' http://localhost:8080/router/0000000000000002

curl -X POST -d '{"address": "172.16.30.1/24"}' http://localhost:8080/router/0000000000000002

curl -X POST -d '{"address": "192.168.10.1/24"}' http://localhost:8080/router/0000000000000002

#set ip for r3
curl -X POST -d '{"address": "192.168.30.1/24"}' http://localhost:8080/router/0000000000000003


curl -X POST -d '{"address": "192.168.10.20/24"}' http://localhost:8080/router/0000000000000003

#default route for r1
curl -X POST -d '{"gateway": "172.16.30.1"}' http://localhost:8080/router/0000000000000001

#default route for r2
curl -X POST -d '{"gateway": "172.16.30.30"}' http://localhost:8080/router/0000000000000002

#default route fo r3
curl -X POST -d '{"gateway": "192.168.10.1"}' http://localhost:8080/router/0000000000000003



#static route for r2
curl -X POST -d '{"destination": "192.168.30.0/24", "gateway": "192.168.10.20"}' http://localhost:8080/router/0000000000000002