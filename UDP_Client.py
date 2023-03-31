from socket import *
import sys

n = len(sys.argv)
UDPClientHost = sys.argv[1]
UDPClientPort = int(sys.argv[2])
UDPConnectionID = sys.argv[3]

UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

UDPClientSocket.connect((UDPClientHost, UDPClientPort))

msg = ('Hello ' + UDPConnectionID)

UDPClientSocket.sendto(msg.encode(), (UDPClientHost, UDPClientPort))

UDPClientSocket.settimeout(300)

while (True):
    # message from server
    message, serverHost = UDPClientSocket.recvfrom(1024)
    print(str(message))
