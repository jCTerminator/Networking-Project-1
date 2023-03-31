from socket import *
import sys #for command line arguments
from threading import Timer #for Timer

#number of arguments: 2- Server_IP Server_Port 
n = len(sys.argv)
connectionList = []
connectionID = ""
inConnectionList = False

#user gets three tries to establish connection after RESET msg 
n_of_reattempts = 3

serverHost = sys.argv[1]
serverPort = sys.argv[2]

#AF_INET is Internet address for IPv4, SOCK_STREAM is socket type for TCP
serverSocket = socket(AF_INET,SOCK_STREAM)

#type-cast serverPort as integer
serverPort = int(serverPort)

#can use an empty string '' in place of serverHost to connect on all available IPv4 interfaces
serverSocket.bind((serverHost,serverPort))

#enables server to accept connections
serverSocket.listen()
print('The server is ready to receive')

#server should gracefully time out after 5 min if no requests/unable to connect
serverSocket.settimeout(300)
while True:
     #define function for what occurs on timeout of 60 sec connection timer
     def timeout():
          print("Connection Error(Timeout) " + connectionID)
          del connectionList[0]

     #blocks execution and waits for incoming connection
     connectionSocket, addr = serverSocket.accept()
     
     #setup 60-sec connection_timer
     connection_timer = Timer(60, timeout)
     connection_timer.start()
     
     #addr contains (clientHost, clientPort) tuple - declare vars
     clientHost, clientPort = addr

     #receive HELLO message
     message = connectionSocket.recv(1024).decode()

     #receive + store connectionID(gets and stores the last 4 characters) 
     connectionID = message[-4:]

     for i in connectionList:

          #if the connection_ID equals a value in connectionList
          if (connectionID == i):
               connection_timer.cancel()
               #if client fails to connect after three tries
               if(n_of_reattempts <= 0):
                    #send "Connection Failure" msg to client
                    failure_msg = ("Connection Failure")
                    connectionSocket.send(failure_msg.encode())
                    #then exit gracefully
                    serverSocket.close()
                    connectionSocket.close()
                    sys.exit()
          
               #in use - print RESET Connection_ID
               print("RESET " + str(connectionID))
               inConnectionList = True

               #send "Connection Error" msg to Client
               error_msg = ("Connection Error " + str(connectionID))
               connectionSocket.send(error_msg.encode())

               #decrement number of re-attempts 
               n_of_reattempts -= 1
               
          else:
               #reset number of re-attempts if connection established
               n_of_reattempts = 3
               inConnectionList = False

     if (inConnectionList == False):
          #add new connection to list of connections IDs
          connectionList.append(connectionID)

          #type-cast int as String for concat & print
          print("OK " + str(connectionID) + " " + clientHost + " " + str(clientPort))
          
          #send "Connection Established" msg 
          connection_msg = ("Connection Established " + str(connectionID) + " " + str(clientHost) + " " + str(clientPort))
          connectionSocket.send(connection_msg.encode()) 
          connection_timer.cancel()
          connectionSocket.close()
          



    
