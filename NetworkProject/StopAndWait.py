import time
from queue import Queue

def SWClient(q, msg, curAck):
    try:
        #---------Ack발생을 특정한 확률로 랜덤---------
        # isAck = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
        isAck = 1 #Error Free라고 가정(+ Corrupted도 X)
        data = msg + ",{}".format(curAck)
        #---------msg의 길이와 data를 전송---------
        if msg != "-1" and isAck == 0: 
            #print("Sender Lost Packet")
            time.sleep(7) #만약 isAck가 0인 경우는 sleep을 통해 ack가 전송되지 않도록 함
            raise TimeoutError
        q.put(data)
            
            #---------통신종료---------
        if (msg == "-1"):  return
        print("Connected [Transport Layer] ! Send : Packet \' {} \' msg \'{}\'".format(curAck, msg))
        
    except TimeoutError: #Timeout인경우 다시 재전송(try 문으로 다시 진입)---------
        print("Time Out! ... Packet Resent ...")
        print("------------------------------------")
        
def bin2int(b):
    result = 0
    for i in range(len(b)):
        if b[len(b) - i - 1] == '1':
            result += pow(2, i)
    return result

def SWClientCkAck(q):
    ackLst = []
    result = ""
    ackMsg = q.get()
    #---------8bit씩 ack가 ascii로 보내짐, 따라서 8bit씩 나누어서 처리---------
    for i in range(0, len(ackMsg) // 8):
        idx = i * 8
        ackLst.append(ackMsg[idx : idx + 8])
    #---------ascii로 receive된 ack를 변환하여 string으로 변환---------
    for r in ackLst:
        result += chr(bin2int(r))
        
    q.put(result)
    return result
        
def SWServer(data, curAck):
#---------Ack발생을 특정한 확률로 랜덤---------
    #isAck = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
    #isCorrupt = 0 if int(random.random() * 100) < 10 else 1 #0 : 유실, 1 : ack보내기
    isAck = 1
    isCorrupt = 1

    msg, packet = data.split(',')
    
    try:
        if(msg == '-1'): return
        #---------만약 packet이 제대로 도착한 경우---------
        if (curAck == packet): 
            #---------Ack가 lost된 경우---------
            if isAck == 0 or isCorrupt == 0:
                #print("Receiver Lost Packet or Corrupted Ack")
                time.sleep(7)
                raise TimeoutError
        print("Receive Ack : [{}], Msg : [{}]".format(packet, msg))
        ackMsg = "ACK"
        return ackMsg
    except TimeoutError:
        print("Time Out! ... ")
        print("------------------------------------")

def SWSendAck(q, msg):
    result = ""
    for i in msg:
        result += "{0:b}".format(ord(i)).zfill(8)
    
    q.put(result)
    return result
        