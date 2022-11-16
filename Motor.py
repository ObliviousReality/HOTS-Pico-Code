from Component import Component
from machine import Pin


class Motor(Component):

    enabled = False

    rate = 0  # number of times/minute

    pinNo = 0
    pin = None

    def __init__(self, pinNoIn) -> None:
        super().__init__()
        self.pinNo = pinNoIn
        pin = Pin(self.pinNo, Pin.OUT)

    def update(self):
        if self.check():
            self.toggle()
            if (self.enabled):
                self.pin.high()
            else:
                self.pin.low()

    def toggle(self):
        self.enabled = not self.enabled

    def off(self):
        self.enabled = False

    def setVibration(self, bool):
        if bool == "True":
            self.enabled = True
        else:
            self.enabled = False

    def setRate(self, rate):
        self.rate = int(rate)
        self.setResetTimer(int(rate / 600))
