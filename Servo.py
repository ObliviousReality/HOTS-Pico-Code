import random
from Component import Component

from machine import PWM, Pin

MIN = 1000000
MID = 1500000
MAX = 2000000


class Servo(Component):

    pinNo = -1
    pin = None
    servo = None

    ds = MID

    moveRandomly = False

    def __init__(self, num) -> None:
        super().__init__()
        self.pinNo = num
        pin = Pin(num, Pin.OUT)
        servo = PWM(pin)
        servo.freq(50)
        servo.duty_ns(MID)

    def angletods(angle):
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
            if self.moveRandomly:
                self.randAngle(-20, 20)
                # Random time between 0.2s and 0.8s
                self.setResetTimer(random.randint(2, 8))
            self.pwm.duty_ns(self.ds)

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
        self.ds = random.randint(lb, ub)

    def randAngle(self, lb, ub):
        self. ds = random.randint(self.angletods(lb), self.angletods(ub))

    def setRandomMove(self, bool):
        if bool == "True":
            self.moveRandomly = True
        else:
            self.moveRandomly = False
            self.setResetTimer(1)
