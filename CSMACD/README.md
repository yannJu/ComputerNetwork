# CSMA/CD
* Carrier Sense Multiple Access/Collision Detection
*  Carrier Sense  Multiple Access : 네트워크 자원을 쓰고 있는 PC 혹은 서버가 있는지 확인 
    - persistent_1 을 이용 (무조건 데이터를 전송 해본 후 Transmisson이 되었는지 확인후 Transmisson 되었을 경우 전송)
    - 통신이 일어나지 않고 있다는 것을 알아냈을 경우 네트워크 상에 실어서 보냄
  *  Collision Deteciton : 데이터를 동시에 보내려다 부딪치는 경우를 Detect
      - collision이 발생되었을 경우 랜덤한 시간(Tb)만큼 Wait후 재전송
  ---

[*CSMACD.py*](https://github.com/yannJu/ComputerNetwork/blob/master/CSMACD/CSMACD.py)
###  **실행방법**
- 파일 실행 후 커맨드창에 limit(재전송 횟수)와 Tfr(Wait Time)을 입력
- 랜덤하게 transmission과 collision이 발생

    `SUCCESS! / FAIL이 출력`