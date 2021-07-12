import socket, random, time, sys
from threading import Thread

curAck = 1
isTimeOut = 0 #timeOut의 여부 확인
start, end = 0, 0 #시작시간, 끝난시간
sF, sN = 0, 0 #도착한 packet 시작과 끝
windowSz = pow(2, int(input("Input Sequence Num __ "))) - 1 #sequence Num을 받아서 윈도우 크기 설정
tmpData = [i + 10 for i in range(windowSz + 1)] #임시로 데이터 packet을 고정

PORT = 9999
HOST = '127.0.0.1'
#---------socket Build---------
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#---------Send Func---------
def Sender(sock):
    global sF, sN
    global windowSz
    global tmpData
    global start, end, isTimeOut
    
    #---------일단 시작 -> 무한 loop---------
    while True:
        try:
            #---------10%확률로 Send Ack 발생---------
            isAck = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
            print("is Ack? : ", isAck)
            #---------맨처음 시작인 경우 start를 줌---------
            if (sN == sF): start = time.time()
            #---------윈도우가 꽉 찬 경우---------
            if sN == sF + windowSz:
                print("Window is FULL-\nWait...")
                raise socket.error
            #---------TimeOut이 된 경우 재전송---------
            if (isTimeOut == 1): 
                #---------재전송을 위해 sN을 초기화 하고 다시 전송---------
                sN = sF
                isTimeOut = 0
                print("Time Out")
            #---------msg를 전송---------
            msg = "{},{},{}".format(windowSz, sN % windowSz, tmpData[sN % windowSz])
            msg = msg.encode()
            print("Send Packet [ {} ], Msg [ {} ]".format(sN % windowSz , tmpData[sN % windowSz]))
            print("-------------------------")
            sN += 1
            if (isAck == 1): sock.sendto(msg, (HOST, PORT))
            time.sleep(4)   #---------sN을 증가시키고 5초 기다림---------
        except socket.error:
            print("Send ")
            break
        except :
            break
        
#---------Ack Func---------
def Ack(sock):
    global curAck
    global sF, sN
    global windowSz
    global tmpData
    global start, end, isTimeOut
    
    #---------일단 Loop ---------
    while True:
        try:
            time.sleep(4)
            #---------Ack가 들어온경우---------
            receivedAck, addr = sock.recvfrom(2048)
            receivedAck = int.from_bytes(receivedAck, "little")
            #---------sF보다는 크거나 같으면서 sN을 넘지 않는 경우 Err Free Ack---------
            end = time.time()
            if (end - start > 10): 
                #다시 타이머 초기화
                isTimeOut = 1
                continue
            if sF < receivedAck <= sN: 
                #---------Ack가 sN과 같으면 timer를 멈춤---------
                start = time.time()
                if receivedAck == sN: sF = sN
                else: sF = receivedAck
                    
                print("Receive Ack [ {} ] ".format(receivedAck % windowSz))
            print("sF : [ {} ], receive Ack : [ {} ],  sN : [ {} ]".format(sF % windowSz , receivedAck % windowSz, sN % windowSz))
            print("-------------------------")
                #else: #sN보다 크거나 같은경우 packet이 잘못 온 것 
            
        except socket.error as err:
            print("Ack : ", err)
            break

if __name__ == "__main__":
    try:
        #senderSocket.settimeout(8)
        sendThread = Thread(target=Sender, args=[senderSocket])
        ackThread = Thread(target=Ack, args=[senderSocket])
        sendThread.start()
        ackThread.start()
    except socket.timeout:
        print("Time Out!.. Resent..")
        print("-------------------------")
    except socket.error as err:
        sys.exit(err)