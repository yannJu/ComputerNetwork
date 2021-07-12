import time

#---------SendFunc---------
def Application_Send():
    #---------Send를 위해 msg를 받음---------   
    message = input("Please Input MSG for bin >> ")
    message = message.replace(' ', '')
    time.sleep(3)
    return message

#---------ReceiveFunc---------
def Application_Receive(ackMsg):
    print("[ {} ] is Arrived_".format(ackMsg))