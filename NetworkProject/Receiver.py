import Application as app
import StopAndWait as sw
import bitStuff_Unstuff as stuff
import CSMACD as csma
import MLT3 as mlt
import socket, time
from threading import Thread, Event
from queue import Queue

curAck = 0
t = 2
#---------Condition Variable---------
appFlag = [0, 0]
tranFlag = [0, 0]
nwkFlag = [0, 0]
dlFlag = [0, 0]
phyFlag = [0, 0]
#---------Set host & host---------
HOST = '127.0.0.1'
PORT = 9999
#---------socket Build---------
receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#---------이미 사용된 주소도 재사용---------
receiveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiveSocket.bind(("localhost", PORT))
receiveSocket.listen()

#---------Application Layer---------
def Application(sendQ, receiveQ):
    #---------receiveQ가 비어있다면 sleep---------
    while (Queue.empty(receiveQ) == True or appFlag[1] == 0): time.sleep(t)    
    #---------ack도착시 data를 get---------
    data = receiveQ.get()
    data = app.Application_Receive(data)
    appFlag[1] = 0 #ack를 consume
    tranFlag[0] = 1

def Transport(sendQ, receiveQ):
    global appFlag, tranFlag, nwkFlag, t
    #---------application layer에서 채우고 + sendQ에 data가 찰 때 까지 Sleep---------
    while (Queue.empty(receiveQ) == True or tranFlag[1] == 0): time.sleep(t)
    #---------sendQ에 data가 들어왔다면 msg를 가지고 s&w---------
    data= receiveQ.get()
    msg, packet = data.split(',')
    tranFlag[1] = 0
    ackMsg = sw.SWServer(data, curAck)
    receiveQ.put(msg)
    appFlag[1] = 1
    
    #---------nwk layer에서 ack가 오길 기다림 == wait---------
    while (tranFlag[0] == 0): time.sleep(t)
    #---------ack가 오면 receiveQ에 data가 들어옴(그 전 까지 sleep)---------
    tranFlag[0] = 0 #nwk에서 받은 ack consume
    ackBit = sw.SWSendAck(sendQ, ackMsg)
    print("Connected [Transport Layer] ! Ack [ {} ] _ ".format(ackBit))
    nwkFlag[0] = 1

def Network(sendQ, receiveQ):
    global tranFlag, nwkFlag, dlFlag, t
    #---------transport layer에서 채우고 + sendQ에 data가 찰 때 까지 Sleep---------
    while (Queue.empty(receiveQ) == True or nwkFlag[1] == 0): time.sleep(t)
    data = receiveQ.get()
    nwkFlag[1] = 0
    receiveQ.put(data)
    tranFlag[1] = 1
    print("Connected [NWK Layer] ! Ack [ {} ] _ ".format(data))
   
    #---------- dl layer에서 ack가 오길 기다림 == wait---------
    while (Queue.empty(sendQ) == True or nwkFlag[0] == 0): time.sleep(t)
    ack  = sendQ.get()
    nwkFlag[0] = 0
    sendQ.put(ack)
    dlFlag[0] = 1
    print("Connected [NWK Layer] ! Ack [ {} ] _ ".format(ack))
    
def Datalink(sendQ, receiveQ):
    global nwkFlag, dlFlag, phyFlag, t
    csmacd = 0
     #---------nwk layer에서 채우고 + receiveQ에 data가 찰 때 까지 1초씩 Sleep---------
    while (Queue.empty(receiveQ) == True or dlFlag[1] == 0): time.sleep(t)
    data = receiveQ.get()
    data, packet = data.split(',')
    dlFlag[1] = 0
    #---------data를 bitUnStuffing---------
    bitUnStuffData = stuff.BitUnstuff(data)
    print("Connected [DataLink Layer] ! Receive [ {} ] _ ".format(bitUnStuffData))
    msg = bitUnStuffData + ',' + packet
    receiveQ.put(msg)
    nwkFlag[1] = 1
    
    #---------- phy layer에서 ack가 오길 기다림 == wait---------
    while (Queue.empty(sendQ) == True or dlFlag[0] == 0): time.sleep(t)
    dlFlag[0] = 0
    ack  = sendQ.get()
    bitStuffAck = stuff.BitStuff(ack)
    print("Connected [DataLink Layer] ! Ack [ {} ] _ ".format(bitStuffAck))
    #---------csma/cd---------
    #collision 이 없을때까지 기다림
    while(csmacd == 0): csmacd = csma.CSMACD(7, 1)
    sendQ.put(bitStuffAck)
    phyFlag[0] = 1
    
def Physical(sock, host, port, sendQ, receiveQ):
    global dlFlag, phyFlag
    
    #---------sender에서 보내는 msg를 기다림---------
    sendConnect, addr = sock.accept()
    while True:
        try:
            receiveMsg = sendConnect.recv(1024)
            break
        except:
            continue
    #---------받은 msg를 decode---------
    receiveMsg = receiveMsg.decode("ascii")
    #---------패킷과 메시지를 분리---------
    data, packet = receiveMsg.split(',')
    print("-----------------Receive Msg-----------------")
    print("Received MSG :", receiveMsg)
    
    #---------reverseMlt3---------
    unMlt = mlt.UnMLT3_Proc(data)
    msg = unMlt + "," + packet
    print("Connected [Physical Layer] ! Receive [ {} ] _ ".format(receiveMsg))
    #---------receiveQ에 넣어주고 다음 layer에서 접근이 가능함을 표시---------
    receiveQ.put(msg)
    dlFlag[1] = 1
    
    #---------Queue가 채워지면서 phyLayer에 접근할 수 있을때 까지 기다림---------
    while (Queue.empty(sendQ) == True or phyFlag[0] == 0): time.sleep(t)
    
    ackData = sendQ.get()
    phyFlag[0] = 0
    ackMlt = mlt.MLT3_Proc(ackData)    
    ackMsg = ackMlt.encode('ascii')
    print("Connected [Physical Layer] ! Ack [ {} ] _ ".format(ackMsg))
    
    sendConnect.send(ackMsg)
    print("-----------------Send Ack-----------------")
    
if __name__ == "__main__":
    sendQue = Queue()
    receiveQue = Queue()
    
    appThread = Thread(target=Application, args=[sendQue, receiveQue])
    tranThread = Thread(target=Transport, args=[sendQue, receiveQue])
    nwkThread = Thread(target=Network, args=[sendQue, receiveQue])
    dlThread = Thread(target=Datalink, args=[sendQue, receiveQue])
    phyThread = Thread(target=Physical, args=[receiveSocket, HOST, PORT, sendQue, receiveQue])
    
    appThread.start()
    tranThread.start()
    nwkThread.start()
    dlThread.start()
    phyThread.start()