# Network Project(Final Exam)
* 이전에 작성한 모든 소스코드를 활용하여 하나의 Network를 작성
* `시나리오 1 : receiver -> sender로 메시지를 전송`
* `시나리오 2 : sender -> receiver로 AckMsg를 전송`
* **Application Layer**
    - 시나리오1 :
        - Client _ 메시지를 입력받은 후 다음계층에 전달
        - Server_ 메시지를 받아 스크린에 출력
    - 시나리오 2:
        - Client _ AckMsg를 받아 스크린에 출력
        - Server_ **X**
* **Transport Layer**
    - `Stop And Wait` 프로토콜을 사용
    - 시나리오1 :
        - Client _ Application Layer에서 전달받은 메시지를 Stop And Wait을 이용하여 Send
        - Server_ 메시지가 제대로 왔는지 Packet Number와 Ack Number를 비교
    - 시나리오 2:
        - Client _  제대로 전송된 Packet인 경우 다음 Packet을 받기 위해 제대로 메시지가 전송되었음을 알림 **(ACK라는 String을 Ascii로 변환)**
        - Server_ Ack메시지가 제대로 전송되었을 경우 화면에 출력
* **Network Layer**
    - Application Layer과 동일하게 그냥 **pass**시킴
* **DataLink Layer**
    - 시나리오1 :
        - Client _ bitStuffing을 진행한 후 CSMA/CD를 이용하여 collision처리를 함 **(bypass를 위해 무조건 collision이 일어나지 않도록 설정하였음)**
        - Server_ bitUnstuffing을 통해 ESC를 구분지음
    - 시나리오 2:
        - Client _ 인코딩 되어있는 Ack메시지를 bitStuffing 후에 CSMA/CD를 통해 collision 처리를 함 **(bypass를 위해 무조건 collision이 일어나지 않도록 설정하였음)**
        - Server_ bitUnstuffing 을 통해 ESC를 구분지음
* **Physical Layer**
    - 시나리오1 :
        - Client _ Stuffing되어있는 bitStream을 **MLT-3**를 통해 디지털 신호로 변환 후 소켓통신을 통해 통신
        - Server_ 소켓통신을 통해 전달받은 메시지를 **MLT-3**를 통해 다시 디지털 신호에서 bitStream으로 변환
    - 시나리오 2:
        - Client _ 소켓통신을 통해 전달받은 메시지를 **MLT-3**를 통해 다시 디지털 신호에서 bitStream으로 변환
        - Server_ Stuffing되어있는 bitStream을 **MLT-3**를 통해 디지털 신호로 변환 후 소켓통신을 통해 통신

---

*Sender.py & Receiver.py*
###  **실행방법**
1. 두개의 커맨드창(혹은 터미널)을 엶
2. Receiver.py를 먼저 실행
3. Receive준비가 되었으면 Sender.py를 실행함
4. 전송할 메시지(byte단위의 bitStream)를 커맨드창에 입력
5. 제대로 전송되고 ACK가 반환되어 출력되는지 확인
   
#현재 **bypass및 Err가 없는 상황**임을 가정하에 구현