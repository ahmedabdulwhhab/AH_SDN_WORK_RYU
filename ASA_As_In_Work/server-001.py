import socket

port = 12345
"""
manually confirm port is not used.
#find the process using the port
lsof -i :8000
#and kill it
kill -
"""
while True:
    print("waiting client to send message, Bye or bye to End")
    s = socket.socket()
    #print("socket.socke()==",s)
    s.bind(('', port))
    s.listen(5)
    c, addr = s.accept()
    print ("Socket Up and running with a connection from",addr)
    while True:
        rcvdData = c.recv(1024).decode()
        print ("S:",rcvdData)
        if(rcvdData=='t'):
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            c.send(current_time.encode())
        elif(rcvdData=='d'):
            from datetime import date
            today = date.today()
            #dd/mm/YY
            d1 = today.strftime("%d/%m/%Y")
            c.send(d1.encode())
        elif(rcvdData=='bye'):
            print("bye bye bye")
            break
        elif(rcvdData=='ip_1'):
            sendData = '192.168.178.31/24'
            c.send(sendData.encode())
        elif(rcvdData=='ip_2'):
            sendData = '192.168.178.32/24'
            c.send(sendData.encode())
        elif(rcvdData=='ip_3'):
            sendData = '192.168.178.33/24'
            c.send(sendData.encode())
        else:
            sendData = input("N: ")
            c.send(sendData.encode())
    c.close()
