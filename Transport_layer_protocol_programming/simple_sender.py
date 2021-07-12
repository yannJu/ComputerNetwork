import socket

#Set host & host
HOST = '127.0.0.1'
PORT =  9999

#Build Socket
#IPv4 인터넷 사용 + 데이터를 Byte Stream으로 사용

while True:
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSocket.connect((HOST, PORT))
    msg = input("보내기(-1을 입력시 종료됩니다. >> ")
    data = msg.encode() #change type byte
    length = len(data)
    #msg의 길이를 전송
    sendSocket.send(length.to_bytes(4, byteorder="little"))
    sendSocket.send(data)
    
    if (msg == "-1"):  break
    print("Send msg : " + msg)
        
sendSocket.close()