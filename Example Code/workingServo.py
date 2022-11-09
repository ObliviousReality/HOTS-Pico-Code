from machine import Pin, PWM
import utime

MID = 1500000
MIN = 750000
MAX = 2500000

pwm = PWM(Pin(0))

pwm.freq(50)
pwm.duty_ns(MID)

led = Pin(1, Pin.OUT)
led.low()

while True:
    try:
        pwm.duty_ns(MIN)
        print("MIN")
        led.low()
        utime.sleep(1)
        pwm.duty_ns(MID)
        print("MID")
        utime.sleep(1)
        pwm.duty_ns(MAX)
        led.high()
        print("MAX")
        utime.sleep(1)
    except KeyboardInterrupt:    
        pwm.deinit()
        break