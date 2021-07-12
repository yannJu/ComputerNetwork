import random
import time

class CSMACD:
    def __init__(self, limit = 5, Tfr = 1):
        self.k = 0
        self.limit = limit
        self.Tfr = Tfr*10**(-3) #ms
        self.process()

    def persistent_1(self):
        lst = ["[Busy]", "[Transmission]"]
        result = random.choices(range(0, 2), weights=[1,1]) #0 : busy , 1 : idle
        print(lst[result[0]])
        return result[0]
    
    def collision(self):
        lst = ["[Not Collision]", "[Collision]"]
        result = random.choices(range(0, 2), weights=[1,1]) #0 : not collision, 1 = collision
        print(lst[result[0]])
        return result[0]

    def wait(self, k):
        R = random.randrange(0, pow(2, k))
        Tb = R * self.Tfr
        time.sleep(Tb*10**(-3))

    def process(self):
        while(True):
            print("Attemp : ", self.k + 1)
            while(True):
                if (self.persistent_1() == 1): break
            if (self.collision() == 0):
                print("SUCCESS!")
                return
            else :
                self.k += 1
                if not (self.k < self.limit):
                    print("FAIL")
                    return
                self. wait(self.k)

limit  = int(input("Enter the maximum number of attemps, between 5 and 15 >> "))
Tfr = int(input("Enter the Tfr, between 1 and 5 >> ")) #Tfr = 1ms or 2ms => 크게받아보고싶음
csmacd = CSMACD(limit, Tfr)