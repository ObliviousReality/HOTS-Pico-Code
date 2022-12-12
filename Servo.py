import random
from Component import Component

from machine import PWM, Pin

MIN = 750000
MID = 1500000
MAX = 2500000

LEG_FWD = 1800000
LEG_BCK = 1100000 
LEG_STP = 15000


class Servo(Component):

    pinNo = -1
    pin = None
    servo = None

    ds = MID

    moveRandomly = False
    
    movingForward = False

    def __init__(self, num) -> None:
        super().__init__()
        self.pinNo = num
        self.pin = Pin(num, Pin.OUT)
        self.servo = PWM(self.pin)
        self.servo.freq(50)
        self.servo.duty_ns(MID)
        self.setResetTimer(1)
        print("Servo running on pin: "+ str(self.pinNo))

    def angletods(self, angle):
        oldRange = (90 - -90)
        newRange = (MAX - MIN)
        d = (((angle - -90) * newRange) / oldRange) + MIN
        return d

    def dstoangle(self, d):
        oldRange = (MAX - MIN)
        newRange = (90 - -90)
        a = (((d - MIN) * newRange) / oldRange) + -90
        return a

    def update(self):
        if (self.check()):
            #print("Servo Updating")
            if self.moveRandomly:
                if self.movingForward:
                    self.ds = self.ds + LEG_STP
                    if self.ds > LEG_FWD:
                        self.movingForward = False
                        self.ds = LEG_FWD
                else:
                    self.ds = self.ds - LEG_STP
                    if self.ds < LEG_BCK:
                        self.movingForward = True
                        self.ds = LEG_BCK
            self.servo.duty_ns(self.ds)

    def setPos(self, ds):
        self.ds = ds
        

    def setAngle(self, a):
        newDS = self.angletods(a)
        if newDS > MAX:
            newDS = MAX
        elif newDS < MIN:
            newDS = MIN
        self.ds = newDS

    def moveByAngle(self, a):
        currentAngle = self.dstoangle(self.ds)
        newAngle = currentAngle + a
        newDS = self.angletods(newAngle)
        if newDS > MAX:
            newDS = MAX
        elif newDS < MIN:
            newDS = MIN
        self.ds = newDS

    def maxLeft(self):
        self.ds = MIN

    def maxRight(self):
        self.ds = MAX

    def center(self):
        self.ds = MID

    def randPos(self, lb, ub):
        test = random.randint(10, 100)
        x = random.randint(int(lb), int(ub))
        self.ds = x

    def randAngle(self, lb, ub):
        self.randPos(self.angletods(lb), self.angletods(ub))
        #self.ds = random.randint(self.angletods(lb), self.angletods(ub))
    
    def off(self):
        self.moveRandomly = False

    def setRandomMove(self, bool, pos):
        if bool == "True":
            if pos == 1:
                self.movingForward = True
            else:
                self.movingForward = False
            self.moveRandomly = True
        else:
            self.moveRandomly = False
            self.center()
            self.setResetTimer(1)
