# BitStuff-UnStuff
* 발신측에서 flag와 data bit를 구분하기 위해 1이 연속적으로 5개가 오는 경우 바로 뒤에 0을 삽입 -> `ex ) 11111101 -> 111110101`
*  수신측에서는 1이 연속으로 5번 오는 경우 뒤에있는 0을 제거
  
  ---
  [*bitstuff.py*](https://github.com/yannJu/ComputerNetwork/blob/master/BitStuffing/bitstuff.py)
###  **실행방법**
- 파일실행 후 byte 단위로 커맨드창에 입력
  
`ex)11111101 입력 -> 111110101 출력`


[*bituUnstuff.py*](https://github.com/yannJu/ComputerNetwork/blob/master/BitStuffing/bitUnstuff.py)
###  **실행방법**
- 파일실행 후 byte 단위로 커맨드창에 입력
  
`ex)111110101 입력 -> 11111101 출력`