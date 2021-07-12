import socket, random, time

#---------현재 Ack state를 cp하기 위한 변수---------
curAck = 0 
msg = ''

#---------Set host & host---------
HOST = '127.0.0.1'
PORT =  9999

#---------Build Socket---------
#---------IPv4 인터넷 사용 + 데이터를 Byte Stream으로 사용---------
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sendSocket.connect((HOST, PORT))
#---------5초 동안 accept되지 않으면 time out---------
sendSocket.settimeout(7)

while True:
    #---------보낼 MSG 입력---------
    msg = input("Input 1Byte Bin (-1 : END) >> ")  
    
    while True:   
        try:
            #---------Ack발생을 특정한 확률로 랜덤---------
            isAck = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
            isCorrectAck = 0 #1 : correct Ack 0 : errAck
            data = msg + ",{}".format(curAck)
            data = data.encode() #change type byte
            length = len(data)
            #---------msg의 길이와 data를 전송---------
            if msg != "-1" and isAck == 0: 
                #print("Sender Lost Packet")
                time.sleep(7) #만약 isAck가 0인 경우는 sleep을 통해 ack가 전송되지 않도록 함
                raise socket.timeout
            sendSocket.send(length.to_bytes(4, byteorder="little"))
            sendSocket.send(data)
            
            #---------통신종료---------
            if (msg == "-1"):  break
            print("Connected! Send : Packet \' {} \' msg \'{}\'".format(curAck, msg))
            #---------Ack를 확인---------
            while (isCorrectAck == 0):
                recData =sendSocket.recv(4)
                recAck = int.from_bytes(recData, "little")
                #---------Ack가 Error없이 제대로 도착했다면---------
                if ((1 - recAck) == curAck): 
                    curAck = 1 - curAck #Ack 번호를 save
                    isCorrectAck = 1 #Ack를 바꾸어서 while문을 빠져나옴
            break
        except socket.timeout: #Timeout인경우 다시 재전송(try 문으로 다시 진입)---------
            print("Time Out! ... Packet Resent ...")
            print("------------------------------------")
            continue
    if msg == '-1': break
sendSocket.close()