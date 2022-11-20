import socket
from _thread import *
import time
import re

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip='127.0.0.1'
port=1025
threadCounter =0
try:
    serverSocket.bind((ip,port))
except socket.error as e:
    print(str(e))
serverSocket.listen(5)
print()
print("Server is Now Available :)")

inf_list = []

def threadConnection(connection,addr):
    count = 0 ;
    segmentcount = 1 ;
    data = connection.recv(1024)
    inf = open('inf.txt','wb')
    inf.write(data)
    while (data):
        try:
            #Control Connection
            if data and count == 0 :
                connection.send(str.encode("200 Ok"))
                count = count + 1
                inf.close()
                temp = open('inf.txt','r')
                for line in temp:
                    temp = line.strip()
                    inf_list.append(temp)
            #Data Connection
            if data and count > 0 :
                #authentication has accepted
                if inf_list[0] == 'Sina' and inf_list[1] == 'SinaSina' and inf_list[2] == '127.0.0.1' and inf_list[3] == '1025' :
                    connection.send(str.encode("Access Approved"))
                    p = open('server.mp4','wb')
                    data = connection.recv(1024)
                    while data:
                        print ("Segment "+str(segmentcount) +" is  Receiving ... ")
                        segmentcount = segmentcount + 1   
                        p.write(data)
                        data = connection.recv(1024)
                        if len(re.findall(r"close", str(data).strip())) != 0:
                            p.write(data)
                            break
                #authentication has denied
                else :
                    connection.send(str.encode("Access Denied"))
                    connection.close()
            else :
                connection.send(str.encode("404 Not Found"))
            try:
                data = connection.recv(1024)
            except:
                print("Connection was Closed By the Client")
                break
            
        except Exception as exc:
            print("Error Occured", exc.args)
            break
    print()
    print("Connection Client " +str(threadCounter) + " Has Closed :(")
    print()
    p.close()
    connection.close()

try:
    while 1 :
        (clientConnetion, addr)= serverSocket.accept()
        start_new_thread(threadConnection, (clientConnetion,addr))
        threadCounter =threadCounter+1
        print()
        print( "Client "+str(threadCounter) +" is  Connected ")
        print()
finally:
    serverSocket.close()




