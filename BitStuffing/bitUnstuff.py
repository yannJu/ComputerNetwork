def BitUnstuff(data):
    chngData = "111110"
    data = data.replace(chngData, "11111")
    print("UNSTUFF : ", data)

BitUnstuff(str(input("input Data(bit) : ")))