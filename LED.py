from Component import Component
from machine import Pin
from neopixel import Neopixel
COLOUR = 0
POWERED = 1
PULSERATE  = 2
BRIGHTNESS = 3
ONTHEUP = 4

OFFC = (0,0,0)

CHEST = 0
HEAD = 1

class LED(Component):
    MAX_BRIGHTNESS = 255  # variable
    MED_BRIGHTNESS = 128
    MIN_BRIGHTNESS = 1
    FADE_INCREMENT = 10
    #Colour|Powered|Pulse Rate|Brightness|OnTheUp
    leds = [[(0,0,0), False, 0, MED_BRIGHTNESS, True],
    [(0,0,0), False, 0, MED_BRIGHTNESS, True]]

    pinNo = 0
    numLEDs = 0
    pin = None

    def __init__(self, pinNumber, numLEDs) -> None:
        super().__init__()
        self.pinNo = pinNumber
        self.numLEDs = numLEDs
        self.pin = Neopixel(numLEDs, 0, pinNumber, "GRB")
        #self.setBrightness(self.MED_BRIGHTNESS)  # 0 - 255
        self.pin.set_pixel(CHEST, self.leds[CHEST][COLOUR])
        self.pin.set_pixel(HEAD, self.leds[HEAD][COLOUR])
        self.pin.show()
        self.setResetTimer(1)
        print("Initted")

    def update(self):
        for i in range(0, 2):
            if self.leds[i][PULSERATE] > 0:
                if self.leds[i][ONTHEUP]:
                    self.leds[i][BRIGHTNESS]+= 255 / (6000 / self.leds[i][PULSERATE])
                    if self.leds[i][BRIGHTNESS] >= self.MAX_BRIGHTNESS:
                        self.leds[i][BRIGHTNESS] = self.MAX_BRIGHTNESS
                        self.leds[i][ONTHEUP] = False
                else:
                    self.leds[i][BRIGHTNESS]-=255 / (6000 / self.leds[i][PULSERATE])
                    if self.leds[i][BRIGHTNESS] <= self.MIN_BRIGHTNESS:
                        self.leds[i][BRIGHTNESS] = self.MIN_BRIGHTNESS
                        self.leds[i][ONTHEUP] = True
                self.refresh()
        return
    
    def refresh(self):
        for i in range(0, 2):
            self.pin.set_pixel(i, self.leds[i][COLOUR], int(self.leds[i][BRIGHTNESS]))
        self.pin.show()

    def setColour(self, ID, newColour):
        r = int(newColour[0:2], 16)
        g = int(newColour[2:4], 16)
        b = int(newColour[4:6], 16)
        self.leds[ID][BRIGHTNESS] = self.MAX_BRIGHTNESS
        self.leds[ID][COLOUR] = (r, g, b)
        self.pin.set_pixel(ID, self.leds[ID][COLOUR], self.leds[ID][BRIGHTNESS])
        self.pin.show()

    def setBrightness(self, ID, newB):
        self.leds[ID][BRIGHTNESS] = newB
        self.pin.brightness(self.brightness)

    def on(self, ID):
        self.leds[ID][POWERED] = True
        
    def off(self, ID):
        self.leds[ID][COLOUR] = OFFC
        self.refresh()

    def allOff(self):
        for i in range(0, 2):
            self.leds[i][COLOUR] = OFFC
            self.leds[i][PULSERATE] = 0
        self.refresh()

    def setStatus(self, ID, status):
        if status == "True":
            self.on(ID)
        elif status == "False":
            self.setPulseRate(ID, 0)
            self.off(ID)

    def toggle(self, ID):
        self.leds[ID][POWERED] = not self.leds[ID][POWERED]
        if (not self.leds[ID][POWERED]):
            self.leds[ID][PULSERATE] = 0

    def setPulseRate(self, ID, rate):
        self.leds[ID][PULSERATE] = int(rate)
        if(int(rate) == 0):
            self.leds[ID][BRIGHTNESS] = self.MAX_BRIGHTNESS
            self.refresh()

    def getPulseRate(self, ID):
        return self.leds[ID][PULSERATE]
