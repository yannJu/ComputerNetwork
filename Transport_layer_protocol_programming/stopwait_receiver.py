import socket, random, time

#---------Ack발생을 동일한 확률로 랜덤---------
ackNum = 0 #받은 ack저장

#---------Build Socket---------
#---------IPv4 인터넷 사용 + 데이터를 Byte Stream으로 사용---------
receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#---------이미 사용된 주소도 재사용---------
receiveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receiveSocket.bind(("localhost", 9999))
receiveSocket.listen()
sendConnect, addr = receiveSocket.accept()
receiveSocket.settimeout(15)

while True:
    try:
        #---------Ack발생을 특정한 확률로 랜덤---------
        isAck = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
        isCorrupt = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
    #---------send의 접속 발생 ~> accept ~> send소켓, addr을 튜플로 받음---------
        data = sendConnect.recv(4)
        length = int.from_bytes(data, "little")
        data = sendConnect.recv(length)
        msg = data.decode()
        #---------msg와 packetNo를 분리---------
        splitIdx = msg.find(',')
        msg, senderPacket = msg[:splitIdx], int(msg[splitIdx + 1:])
        
        if(msg == '-1'): break
        #---------만약 packet이 제대로 도착한 경우---------
        if (ackNum == senderPacket): 
            #---------Ack가 lost된 경우---------
            if isAck == 0 or isCorrupt == 0:
                #print("Receiver Lost Packet or Corrupted Ack")
                time.sleep(7)
                continue
            print("Receive Ack : [{}], Msg : [{}]".format(senderPacket, msg))
            senderPacket = 1 - senderPacket
            print("Ack : [{}]".format(senderPacket))
            sendConnect.send(senderPacket.to_bytes(4, byteorder="little"))
            ackNum = senderPacket
            
    except socket.timeout:
        break
    except:
        print("Receive....")
        break
        