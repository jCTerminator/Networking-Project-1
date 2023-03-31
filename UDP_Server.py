import socket
import sys
from threading import Timer

bufferSize = 1024

n = len(sys.argv)
connectionList = []
connectionID = ""
inConnectionList = False

n_of_reattempts = 3
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a datagram socket

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((serverHost, serverPort))

print("UDP server up and listening")

UDPServerSocket.settimeout(300)
# Listen for incoming datagrams

while (True):

    def timeout():
        print("Connection Error(Timeout) " + str(connectionID))
        del connectionList[0]

    connection_timer = Timer(60, timeout)
    connection_timer.start()

    # receive HELLO message
    bytesAddrPair = UDPServerSocket.recvfrom(1024)

    # split message/addr tuple and save to vars
    message = bytesAddrPair[0]

    clientAddr = bytesAddrPair[1]

    # receive + store connectionID(gets and stores the last 4 characters)
    connectionID = message[-4:]

    for i in connectionList:

        # if the connection_ID equals a value in connectionList
        if (connectionID == i):
            connection_timer.cancel()

            if (n_of_reattempts <= 0):
                # send "Connection Failure" msg to client
                failure_msg = ("Connection Failure")
                UDPServerSocket.sendto(failure_msg.encode(), (clientAddr))
                # then exit gracefully
                UDPServerSocket.close()
                sys.exit()

            # in use - print RESET Connection_ID
            print("RESET " + str(connectionID))
            inConnectionList = True

            # send "Connection Error" msg to Client
            error_msg = ("Connection Error " + str(connectionID))
            UDPServerSocket.sendto(error_msg.encode(), (clientAddr))

            # decrement number of re-attempts
            n_of_reattempts -= 1

        else:
            # reset number of re-attempts if connection established
            n_of_reattempts = 3
            inConnectionList = False

    if (inConnectionList == False):
        # add new connection to list of connections IDs
        connectionList.append(connectionID)

        print("OK " + str(connectionID) + " " + str(clientAddr))
        # UDPClientHost + " " + str(UDPClientPort))

# type-cast int as String for concat & print
        connection_msg = ("Connection Established " +
                          str(connectionID) + " " + str(clientAddr))
        # str(UDPClientHost) + " " + str(UDPClientPort))
        UDPServerSocket.sendto(connection_msg.encode(), (clientAddr))

# stop the timer as was able to receive message from server in time
        connection_timer.cancel()
