from machine import Pin, PWM
import random

MIN = 1000000
MID = 1500000
MAX = 2000000


class Servo:

    pinNo = -1
    pin = None
    servo = None

    ds = MID

    def __init__(self, num) -> None:
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

    def update(self):
        self.pwm.duty_ns(self.ds)

    def setPos(self, ds):
        self.ds = ds
    
    def setAngle(self, a):
        oldRange = (90 - -90)
        newRange = (MAX - MIN)
        d = (((a - -90) * newRange) / oldRange) + MIN
        self.ds = d

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
