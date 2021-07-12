# Transport Layer
* transport layer에서 사용하는 protocol들을 구현
* Simple Protocol
    - 일괄적으로 그냥 send
* Stop And Wait
    - sender와 receiver 모두 window의 크기가 1
    - Ack Msg에 따라 제대로 전송이 되었는지, corrupt등을 확인
* Go Back N (미완)
    - window의 크기(N)를 정함, 단 receiver의 window크기는 여전히 1
    - Ack에 맞게 전송
  - <u>*현재 Corrupt등 에러처리가 제대로 이루어지지않음*</u>
* Selective Repeat<u>(작성안함)</u>
    - sender와 receiver 둘 다 window의 크기가 1이상
    - Ack, Window 크기 모두를 고려
---

### Simple Protocol

*simple_receiver.py & simple_sender.py*
###  **실행방법**
* 두개의 커맨드창(혹은 터미널)을 엶
* 먼저 simple_receiver.py 를 실행
* receive 준비가 되었으면 simple_sender.py를 실행
* sender에 전송하려는 메시지를 커맨드 창에 입력
* receiver에서 제대로 받았는데 출력창 확인

#**-1**을 입력하면 종료

---

### StopAndWait Protocol

*stopwait_receiver.py & stopwait_sender.py*
###  **실행방법**
* 두개의 커맨드창(혹은 터미널)을 엶
* 먼저 stopwait_receiver.py 를 실행
* receive 준비가 되었으면 stopwait_sender.py를 실행
* sender에 전송하려는 메시지를 커맨드 창에 입력
* receiver에서 제대로 받았는데 출력창 확인

#**-1**을 입력하면 종료</br>
#Stop And Wait부터는 **Window**와 **Ack**에 따라 **Err처리**가 필요함</br>
#0번째 Packet을 받았다면 Ack로 1을 보내고 그에 맞는 Packet을 보내는데 Window의 크기가 **1**이므로 `0, 1`으로만 Ack번호가 생성

---

### GBN Protocol (<u>미완성</u>)

*gbn_receiver.py & gbn_sender.py*
###  **실행방법**
* 두개의 커맨드창(혹은 터미널)을 엶
* 먼저 gbn_receiver.py 를 실행
* receive 준비가 되었으면 gbn_sender.py를 실행
* sender에 전송하려는 메시지를 커맨드 창에 입력
* receiver에서 제대로 받았는데 출력창 확인

#**-1**을 입력하면 종료</br>
#Sender의 Window의 크기가 1보다 크기 때문에 맞는 Packet의 번호가 제대로 전달되는것이 관건</br>
*<u>#현재  Err혹은 Corrupt처리를 하게 될 경우 packet전송에서 충돌이 나는 경우가 생김</u>*

---

### SR Protocol (<u>작성안함</u>)