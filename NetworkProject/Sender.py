import Application as app
import StopAndWait as sw
import bitStuff_Unstuff as stuff
import CSMACD as csma
import MLT3 as mlt
import socket, time
from threading import Thread, Event
from queue import Queue

curAck = 0
t = 1
appFlag = [0, 0]
tranFlag = [0, 0]
nwkFlag = [0, 0]
dlFlag = [0, 0]
phyFlag = [0, 0]

#---------Set host & host---------
HOST = '127.0.0.1'
PORT = 9999
#---------socket Build---------
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
senderSocket.connect((HOST, PORT))

#---------Application Layer---------
def Application(sendQ, receiveQ):
    global appFlag, tranFlag, t
    #---------get Msg for send---------
    msg = app.Application_Send()
    #---------보내기 위해 Queue에 data를 넣음---------
    sendQ.put(msg)
    tranFlag[0] = 1 #transport 에서 받을 data가 찼다는 cv
    #---------receiveQ가 비어있다면 sleep---------
    while (Queue.empty(receiveQ) == True or  appFlag[1] == 0): time.sleep(t)    
    #---------ack도착시 data를 get---------
    data = receiveQ.get()
    data = app.Application_Receive(data)
    appFlag[1] = 0 #ack를 consume

def Transport(sendQ, receiveQ):
    global appFlag, tranFlag, nwkFlag, t
    #---------application layer에서 채우고 + sendQ에 data가 찰 때 까지 Sleep---------
    while (Queue.empty(sendQ) == True or  tranFlag[0] == 0): time.sleep(t)
    #---------sendQ에 data가 들어왔다면 msg를 가지고 s&w---------
    msg = sendQ.get()
    tranFlag[0] = 0 #application 의 data를 consume
    sw.SWClient(sendQ, msg, curAck)
    nwkFlag[0] = 1 #nwklayer에 msg를 전송한 cv
    
    #---------nwk layer에서 ack가 오길 기다림 == wait---------
    while (Queue.empty(receiveQ) == True or  tranFlag[1] == 0): time.sleep(t)
    #---------ack가 오면 receiveQ에 data가 들어옴(그 전 까지 sleep)---------
    ackMsg = sw.SWClientCkAck(receiveQ)
    tranFlag[1] = 0 #nwk에서 받은 ack consume
    print("Connected [Transport Layer] ! Ack [ {} ] _ ".format(ackMsg))
    appFlag[1] = 1 #application layer에 전달한 cv

def Network(sendQ, receiveQ):
    global tranFlag, nwkFlag, dlFlag, t
    #---------transport layer에서 채우고 + sendQ에 data가 찰 때 까지 Sleep---------
    while (Queue.empty(sendQ) == True or  nwkFlag[0] == 0): time.sleep(t)
    data = sendQ.get()
    nwkFlag[0] = 0
    sendQ.put(data)
    dlFlag[0] = 1
    print("Connected [NWK Layer] ! Send [ {} ] _ ".format(data))
   
    #---------- dl layer에서 ack가 오길 기다림 == wait---------
    while (Queue.empty(receiveQ) == True or nwkFlag[1] == 0): time.sleep(t)
    ack  = receiveQ.get()
    nwkFlag[1] = 0
    receiveQ.put(ack)
    print("Connected [NWK Layer] ! Ack [ {} ] _ ".format(ack))
    tranFlag[1] = 1
    
def Datalink(sendQ, receiveQ):
    global nwkFlag, dlFlag, phyFlag, t
    csmacd = 0
     #---------nwk layer에서 채우고 + sendQ에 data가 찰 때 까지 1초씩 Sleep---------
    while (Queue.empty(sendQ) == True or dlFlag[0] == 0): time.sleep(t)
    data = sendQ.get()
    dlFlag[0] = 0
    #---------data를 bitStuffing---------
    data, packet = data.split(',')
    bitStuffData = stuff.BitStuff(data) + "," +  packet
    print("Connected [DataLink Layer] ! Send [ {} ] _ ".format(bitStuffData))
    #---------csma/cd---------
    #collision 이 없을때까지 기다림
    while(csmacd == 0): csmacd = csma.CSMACD(7, 1)
    sendQ.put(bitStuffData)
    phyFlag[0] = 1
    
    #---------- phy layer에서 ack가 오길 기다림 == wait---------
    while (Queue.empty(receiveQ) == True or dlFlag[1] == 0): time.sleep(t)
    ack  = receiveQ.get()
    dlFlag[1] = 0
    ackUnStuff = stuff.BitUnstuff(ack)
    print("Connected [DataLink Layer] ! Ack [ {} ] _ ".format(ackUnStuff))
    receiveQ.put(ackUnStuff)
    nwkFlag[1] = 1
    
def Physical(sock, host, port, sendQ, receiveQ):
    global dlFlag, phyFlag, t
    #---------transport layer에서 채우고 + sendQ에 data가 찰 때 까지 Sleep---------
    while (Queue.empty(sendQ) == True or phyFlag[0] == 0): time.sleep(t)
    data = sendQ.get()
    data, packet = data.split(',')
    phyFlag[0] = 0
    mltMsg = mlt.MLT3_Proc(data)
    
    mltMsg = mltMsg + "," +  packet
    mltMsg = mltMsg.encode('ascii')
    print("Connected [Physical Layer] ! Send [ {} ] _ ".format(mltMsg))
    
    sock.send(mltMsg)
    print("-----------------Send Msg-----------------")
    
    #---------socket통신으로 ack를 받음---------
    ackMsg = sock.recv(1024)
    print("-----------------Receive Ack-----------------")
    ackMsg = ackMsg.decode('ascii')
    print("Received Ack :", ackMsg)
    ackUnMlt = mlt.UnMLT3_Proc(ackMsg)
    print("Connected [Physical Layer] ! Ack [ {} ] _ ".format(ackUnMlt))
    receiveQ.put(ackUnMlt)
    dlFlag[1] = 1
    
    
if __name__ == "__main__":
    sendQue = Queue()
    receiveQue = Queue()
    
    appThread = Thread(target=Application, args=[sendQue, receiveQue])
    tranThread = Thread(target=Transport, args=[sendQue, receiveQue])
    nwkThread = Thread(target=Network, args=[sendQue, receiveQue])
    dlThread = Thread(target=Datalink, args=[sendQue, receiveQue])
    phyThread = Thread(target=Physical, args=[senderSocket, HOST, PORT, sendQue, receiveQue])
    
    appThread.start()
    tranThread.start()
    nwkThread.start()
    dlThread.start()
    phyThread.start()