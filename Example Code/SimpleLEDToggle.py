from machine import Pin
import utime

led = Pin(2, Pin.OUT)
led.low()

d = 1

while True:
    try:
    	led.high()
    	utime.sleep(d)
    	led.low()
    	utime.sleep(d)
    except KeyboardInterrupt:
        break
