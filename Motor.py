from Component import Component
from machine import Pin


class Motor(Component):

    enabled = False

    rate = 0  # number of times/minute

    pinNo = 0
    motorpin = None
    
    beating = False

    def __init__(self, pinNoIn) -> None:
        super().__init__()
        self.pinNo = pinNoIn
        self.motorpin = Pin(self.pinNo, Pin.OUT)
        print("Motor running on pin: "+ str(self.pinNo))

    def update(self):
        if self.check():
            #self.toggle()
            if self.rate > 0:
                self.beat()
            if (self.enabled):
                self.motorpin.high()
            else:
                self.motorpin.low()

    def toggle(self):
        self.enabled = not self.enabled

    def off(self):
        self.enabled = False
        
    def on(self):
        self.enabled = True

    def setVibration(self, bool):
        if bool == "True": 
            self.enabled = True
        else:
            self.rate = 0
            self.enabled = False

    def setRate(self, rate):
        self.rate = int(rate)
        self.setResetTimer(1)
        self.beating = True
        
    def beat(self):
        if self.beating:
            self.off()
            self.beating = False
            self.setResetTimer((60 / int(self.rate)) * 50)
        else:
            self.on()
            self.beating = True
            #self.setResetTimer(3)
            self.setResetTimer((60 / int(self.rate)) * 50)
