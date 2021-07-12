# MLT3
* 디지털 데이터를 디지털 신호로 변환
* 이전과 동일한 voltage가 유지될 경우 에러 발생 확률이 높아짐
* 따라서 이를 해결하기 위해 예시로 `Multilevel Transmit-three level` 를 사용
---
### Multilevel Transmit-three level
1.  첫번째 bit (시작bit)
       - 첫번째 bit가 0인경우 **0**으로 유지
       - 첫번째 bit가 1인경우 **+** 로 유지
2. 들어올 bit
   - 다음에 들어올 bit가  0인경우 **0**으로 유지
   - 다음에 들어올 bit가 1인경우
     - 이전bit가 0인경우 : 마지막 voltage가 -라면 **+** 로, +라면 **-** 로 유지
     - 이전 bit가 0이 아닌경우 : **0**으로 유지
  ---
  
[*Multi_transition_MLT3_Scheme.py*](https://github.com/yannJu/ComputerNetwork/blob/master/MLT3-BitStuffing/Multi_transition_MLT3_Scheme.py)
###  **실행방법**
- 파일 실행 후 bitStream을 입력

`111110111 입력 -> +0-0++0-0 출력`

---
## bitStuff/MLT3 와 UnMLT3/bitUnstuff

* DataLink Layer에서 bitStuff/bitUnstuff 및 Physical Layer에서 MLT3와 UnMLT3적용

[*receiver.py*](https://github.com/yannJu/ComputerNetwork/blob/master/MLT3-BitStuffing/receiver.py)
###  **실행방법**
- 파일 실행 후 디지털 신호를 입력하여 MLT3된 신호를 bitStream으로 변환
- 변환된 bitStream은 bitUnstuffing을 통해  **ESC**를 구분
  
    ` +0-0++0-0 입력시 -> 111110111로 UnMLT3 -> 11111111로 bitUnstuffing`

[*sender.py*](https://github.com/yannJu/ComputerNetwork/blob/master/MLT3-BitStuffing/sender.py)
###  **실행방법**
- 파일 실행 후 bitStream을 입력하여 bitStuffing 진행
- bitStuffing된 bitStream은 MLT3를 통해 디지털 신호로 변환
  
    ` 11111111 입력시 -> 111110111로 bitStuffing -> +0-0++0-0로 MLT3`