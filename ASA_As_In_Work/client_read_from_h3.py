import socket

print("send message, Bye or bye to End")
s = socket.socket()
s.connect(('100.0.0.3',12345))
while True:
    str = input(" ip_1 for h1  for ip address: ")        #python 3
    #str = raw_input("S: ")      #python 2
    str="t"
    s.send(str.encode());
    received_data=s.recv(1024).decode()
    print ("received data",received_data)
    #if(len(received_data) >5):
    #    print ("length of received data is ",len(received_data))
    #    import os
        #os.system('ifconfig')
    #    my_cmd="sudo ifconfig h3-eth0  " + received_data
        #os.system(my_cmd)
        #str="bye"
    #s.send(str.encode());
        #break


s.close()
