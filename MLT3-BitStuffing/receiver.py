def UnMLT3_Proc(data):
    answer = ""
    for i in range(1, len(data)):
        if (i == 1): #Check First bit
            if (data[0] == "+"): answer += "1" #if Fist Bit is +
            else: answer += "0" #if Fist Bit is 0
        if (data[i] == data[i - 1]): answer +="0"
        else: answer += "1"

    print("UNMLT3 : ", answer)
    return answer

def BitUnstuff(data):
    chngData = "111110"
    data = data.replace(chngData, "11111")
    
    print("UNSTUFF : ", data)
    return(data)

chngUnMLT3 = UnMLT3_Proc(input("INPUT  : "))
chngUnstuff = BitUnstuff(chngUnMLT3)
print("OUTPUT : ", chngUnstuff)