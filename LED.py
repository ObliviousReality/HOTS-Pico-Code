from machine import Pin


class LED:
    colour = "#FFFFFF"
    powered = False
    pulseRate = 0

    pinNo = -1
    pin = None

    def __init__(self, pinNumber) -> None:
        self.pinNo = pinNumber
        pin = Pin(pinNumber, Pin.OUT)
        pin.low()

    def update(self):
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

    def toggle(self):
        self.powered = not self.powered

    def setPulseRate(self, rate):
        self.pulseRate = rate

    def getPulseRate(self):
        return self.pulseRate
