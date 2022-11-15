from Component import Component
from machine import Pin


class LED(Component):
    colour = "#FFFFFF"
    powered = False
    pulseRate = 0

    pinNo = 0
    pin = None

    def __init__(self, pinNumber) -> None:
        super().__init__()
        self.pinNo = pinNumber
        self.pin = Pin(pinNumber, Pin.OUT)
        self.pin.low()
        print("Initted")

    def update(self):
        if self.check():
            if self.powered:
                self.pin.high()
            else:
                self.pin.low()

    def setColour(self, newColour):
        self.colour = newColour

    def getColour(self):
        return self.colour

    def on(self):
        self.powered = True

    def off(self):
        self.powered = False
        
    def setStatus(self, status):
        if status == "True":
            self.on()
        elif status == "False":
            self.off()
            
    def toggle(self):
        self.powered = not self.powered

    def setPulseRate(self, rate):
        self.pulseRate = rate

    def getPulseRate(self):
        return self.pulseRate
