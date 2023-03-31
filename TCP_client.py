from socket import *
import sys #for command line arguments

#number of arguments: 3- Server_IP Server_Port ConnectionID
n = len(sys.argv)

clientHost = sys.argv[1]
clientPort = sys.argv[2]
connectionID = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)

#type-cast clientPort as integer
clientPort = int(clientPort)

try:
    #connects to server
    clientSocket.connect((clientHost,clientPort))
except:
    #client should gracefully time out after 5 min if no requests/unable to connect
    clientSocket.settimeout(300)


#build message to send to server
message = ("HELLO " + connectionID)
clientSocket.send(message.encode())

#read server's failure/success msg
response_msg = clientSocket.recv(1024).decode()
print(response_msg)

clientSocket.close()

