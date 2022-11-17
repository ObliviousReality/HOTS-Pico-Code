from Servo import Servo
from LED import LED
from Motor import Motor
import network
import utime
import socket
#from machine import Pin
import _thread
import json

import sys
sys.path.insert(1, "/HOTS-Pico-Code")

#ssid = "LUSUINTERNET647"
#password = "341Minimum*?@021"

ssid = "Tom's Hotspot"
password = "thisisaverysecurepassword"

head = LED(0)
chest = LED(1)
# Ports are wrong and TODO: Need changing, especially port #3 as that's a ground pin.
legs = [Servo(2), Servo(3)]
arm = Servo(4)
motor = Motor(5)


def loopLED():
    print("In thread")
    while True:
        utime.sleep(0.1)
        head.update()
        chest.update()
        for l in legs:
            l.update()
        arm.update()
        motor.update()


html = """
<!DOCTYPE html>
<html>
<body>
<h1>This is a server running on a raspberry pi</h1>
<p>Isn't that cool?</p>
</body>
</html>

"""


def handleInput(data):
    j = json.loads(data)

    if "allOff" in j:
        print("allOff")
        chest.off()
        # just going to
        head.off()
        arm.maxRight()  # May be left, need to test!
        for l in legs:
            l.center()
        motor.off()
        # LED off
        return

    if "reset" in j:
        print("reset")
        chest.off()
        chest.setPulseRate(0)
        head.off()
        head.setPulseRate(0)
        arm.maxRight()
        for l in legs:
            l.setRandomMove("False")
            l.center()
        motor.off()
        motor.setRate(0)
        # LED ON
        utime.sleep(0.5)
        # LED OFF
        utime.sleep(0.5)
        # LED ON
        utime.sleep(0.5)
        # LED OFF
        return

    if "raiseArm" in j:
        print("raiseArm")
        b = j["raiseArm"]
        if b == "True":
            arm.maxLeft()  # could be the wrong way around
        else:
            arm.maxRight()

    if "toggleLegs" in j:
        print("toggleLegs")
        for l in legs:
            l.setRandomMove(j["toggleLegs"])

    if "toggleHead" in j:
        print(j["toggleHead"])
        head.setStatus(j["toggleHead"])
    if "headColour" in j:
        print(j["headColour"])
        head.setColour(j["headColour"])
    if "headPulseRate" in j:
        print(j["headPulseRate"])
        head.setPulseRate(j["headPulseRate"])

    if "toggleChest" in j:
        print(j["toggleChest"])
        chest.setStatus(j["toggleChest"])
    if "chestColour" in j:
        print(j["chestColour"])
        chest.setColour(j["chestColour"])
    if "chestPulseRate" in j:
        print(j["chestPulseRate"])
        chest.setPulseRate(j["chestPulseRate"])

    if "toggleVibration" in j:
        print(j["toggleVibration"])
        motor.setVibration(j["toggleVibration"])
    if "setVibration" in j:
        print(j["setVibration"])
        motor.setRate(j["setVibration"])


def connectWIFI():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, password)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        utime.sleep(1)
    print(wlan.isconnected())
    ipaddr = wlan.ifconfig()[0]
    print("IP: " + ipaddr)


def handleConn(c, addr):
    print("A Client has connected from address: ", addr)
    req = c.recv(1024)
    req = str(req)
    # length = int(
    header = req.split("\\r\\n")
    contentSize = 0
    for item in header:
        if "Content-Length" in item:
            contentSize = item.split(" ")[1]

    data = c.read(int(contentSize))

    handleInput(data)

    resp = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
    c.send(resp)
    # c.send(html)
    c.close()
    # Turn off LED


def initServer():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)
    print("Server initialised and listening")
    # Turn off LED
    while True:
        try:
            print("waiting for accept:")
            client, address = sock.accept()
            print("client accepted")
            # Turn on LED
            handleConn(client, address)
        except OSError as e:
            client.close()
            print("Error, connection closed.")
            break


if __name__ == "__main__":

    # TODO: create some sort of start up procedure here.

    # Turn on basic LED.

    _thread.start_new_thread(loopLED, ())
    connectWIFI()

    initServer()
