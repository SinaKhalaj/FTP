import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip='127.0.0.1'
port=1025
clientSocket.connect((ip,port))

#Control Connection
authentication = open('authentication.txt' , 'rb')
print()
print('Request for Starting a Connection ...')
print()
a = authentication.read(1024)
clientSocket.send(a)

#Open a file in which if the authentication has accepted the file uploads
segmentcount = 1 ;
#Response from Server
response = clientSocket.recv(1024)

try:
    while (response):
        temp = str(response.strip())
        if temp[2:-1] == '200 Ok' or temp[2:-1] == '404 Not Found' or temp[2:-1] == 'Access Approved' or temp[2:-1] == 'Access Denied':
            print("Received Message from Server is : " + response.decode())
            if temp[2:-1] == 'Access Approved' :
                print("Sending Data ...")
                print()
                
                pic = open('vid.mp4','rb')
                readpic = pic.read(1024)
                print ("Segment "+str(segmentcount) +" is  Sending ... ")
                while (readpic):
                    segmentcount = segmentcount + 1
                    print ("Segment "+str(segmentcount) +" is  Sending ... ")
                    writeCount = clientSocket.send(readpic)
                    readpic = pic.read(1024)
                # print("readPIC = ", readpic)
                clientSocket.send(readpic)
                pic.close()
                
                clientSocket.send(b'close')
                
                import time
                print()
                print("Sleeping ...")
                time.sleep(2)
                clientSocket.shutdown(socket.SHUT_RDWR)
                break
            elif temp[2:-1] == 'Access Denied' :
                print("Connection is Closing ...") 
            elif temp[2:-1] == '404 Not Found' :
                print("File Couldn't Found . Connection is closing ...")    
        response = clientSocket.recv(1024)
       
finally:
    authentication.close()
    print()
    print("Connection is Closing ...")
    print()
    clientSocket.close()




