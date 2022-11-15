from machine import Pin
import utime

led = Pin(1, Pin.OUT)
led.low()

d = 1

while True:
    try:
    	led.low()
    	#utime.sleep(d)
    	#led.low()
    	#utime.sleep(d)
    except KeyboardInterrupt:
        break
