import socket, random, time, sys
from threading import Thread

ackNum = 0
windowSz = 0
HOST = '127.0.0.1'
PORT = 9999
#---------socket Build---------
receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiveSocket.bind(("localhost", PORT))
receiveSocket.settimeout(15)

#---------일단 loop---------
while True:
    try:
        #---------packet을 받음---------
        receivedData, addr = receiveSocket.recvfrom(2048)
        data = receivedData.decode()
        windowSz, receivedPacket, receivedMsg = list(map(int, data.split(',')))
        print("Received Ack : [ {} ], Msg : [ {} ]".format(receivedPacket, receivedMsg))
        
        #---------제대로 packet이 왔다면 다음 패킷을 요구---------
        if ackNum % windowSz == receivedPacket:
            ackNum += 1
        print("SendAck : [ {} ]".format(ackNum % windowSz))
        print("-------------------------")
        receiveSocket.sendto(ackNum.to_bytes(4, "little"), addr)
    except socket.timeout:
        print("END")
        sys.exit()
    except ValueError:
        continue
    except socket.error as err:
        print("Receive : ", err)
        sys.exit()
    