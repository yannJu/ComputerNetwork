import socket

#Build Socket
#IPv4 인터넷 사용 + 데이터를 Byte Stream으로 사용
receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#이미 사용된 주소도 재사용
receiveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receiveSocket.bind(("localhost", 9999))
receiveSocket.listen()

try:
    while True:
       #send의 접속 발생 ~> accept ~> send소켓, addr을 튜플로 받음
        sendConnect, addr = receiveSocket.accept()
        #ver 2. 한번만 통신해보기 
        data = sendConnect.recv(4)
        length = int.from_bytes(data, "little")
        data = sendConnect.recv(length)
        msg = data.decode()
        if (msg == "-1"): break
        print("Received Msg : ", msg)
        
except:
    print("Receive....")
finally:
    receiveSocket.close()        