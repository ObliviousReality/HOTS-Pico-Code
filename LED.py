from Component import Component
from machine import Pin
from neopixel import Neopixel


class LED(Component):
    MAX_BRIGHTNESS = 255  # variable
    MED_BRIGHTNESS = 128
    MIN_BRIGHTNESS = 1
    FADE_INCREMENT = 10

    colour = "FFFFFF"
    powered = False
    pulseRate = 0
    brightness = MED_BRIGHTNESS
    onTheUp = True

    pinNo = 0
    numLEDs = 0
    pin = None

    def __init__(self, pinNumber, numLEDs) -> None:
        super().__init__()
        self.pinNo = pinNumber
        self.numLEDs = numLEDs
        self.pin = Neopixel(numLEDs, 28, pinNumber)
        self.setBrightness(self.MED_BRIGHTNESS)  # 0 - 255
        self.pin.fill((0, 0, 0))
        self.pin.show()
        print("Initted")

    def update(self):
        if self.check():
            if self.powered or self.getPulseRate() > 0:
                self.pin.show()
                newB = self.getBrightness()
                if self.onTheUp:
                    newB += self.FADE_INCREMENT
                    if newB > self.MAX_BRIGHTNESS:
                        self.onTheUp = False
                        newB -= self.FADE_INCREMENT
                else:
                    newB -= self.FADE_INCREMENT
                    if newB < self.MIN_BRIGHTNESS:
                        self.onTheUp = True
                        newB += self.FADE_INCREMENT
                self.setBrightness(newB)
            else:
                self.setBrightness(self.MED_BRIGHTNESS)
                self.pin.fill((0, 0, 0))
                # off?

    def setColour(self, newColour):
        # newColour = newColour[1:] ??
        r = int(newColour[0:2], 16)
        g = int(newColour[2:4], 16)
        b = int(newColour[4:6], 16)
        self.setBrightness(self.MIN_BRIGHTNESS)
        self.colour = (r, g, b)

    def getColour(self):
        return self.colour

    def setBrightness(self, newB):
        self.brightness = newB
        self.pin.brightness(self.brightness)

    def getBrightness(self):
        return self.brightnesss

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
