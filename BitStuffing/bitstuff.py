def BitStuff(data):
    cnt = 0
    for i in range(len(data)):
        if (data[i] == '1'): cnt += 1
        else: cnt = 0
        if (cnt == 5):
            cnt = 0
            data = data[:i + 1] + '0' + data[i + 1:]
    print("STUFF : ", data)

BitStuff(str(input("Input Data(bit) : ")))