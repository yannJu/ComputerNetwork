bitStream = input()
resultLst = list()
transitionFlag = 1 #transitionFlag = 1 : up, = 0 : down
levelFlag = False # T : up status, F : down status
answer = ""

#At the beginning
if (bitStream[0] == '0'): resultLst.append(0) #beginning of a 0bit
else:  #beginning of a 1bit
    resultLst.append(1)
    levelFlag = True

for i in range(1, len(bitStream)): #next bit : bitStream[i], current level : resultLst[-1]
    if (bitStream[i] == '0'): resultLst.append(resultLst[-1]) #next bit is 0
    else: #next bit is 1
        if (resultLst[-1] == 0): #current level is 0
            if levelFlag: 
                levelFlag = False
                resultLst.append(resultLst[-1] - 1)
            else:
                levelFlag = True
                resultLst.append(resultLst[-1] + 1)
        else: #current level is not 0
            resultLst.append(0)
            
for a in resultLst:
    if (a == -1): answer += '-'
    elif (a == 1): answer += '+'
    else: answer += '0'

print(answer)