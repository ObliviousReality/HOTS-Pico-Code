from Servo import Servo
from LED import LED
from Motor import Motor
import network
import utime
import socket
from machine import Pin
import _thread
import json

import sys
sys.path.insert(1, "/HOTS-Pico-Code")

#ssid = "LUSUINTERNET647"
#password = "341Minimum*?@021"

ssid = "HOTS"
password = "healthontheshelf"

lights = LED(6,2)
HEAD = 1
CHEST = 0
legs = [Servo(1), Servo(2)]
arm = Servo(11)
arm.maxLeft()
motor = Motor(13)


def loopLED():
    print("In thread")
    while True:
        try:
            utime.sleep(0.01)
            lights.update()
            for l in legs:
                l.update()
            arm.update()
            motor.update()
        except KeyboardInterrupt:
            print("End")
            handleInput("allOff")
            break
    quit()


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
    print(j)
    if "allOff" in j:
        print("allOff")
        lights.allOff()
        arm.maxLeft() 
        for l in legs:
            l.center()
            l.off()
        motor.setVibration(0)
        # LED off
        return

    if "reset" in j:
        print("reset")
        lights.allOff()
        arm.maxLeft()
        for l in legs:
            l.setRandomMove("False",0)
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

    if "toggleArm" in j:
        print("toggleArm")
        b = j["toggleArm"]
        if b == "True":
            print("True")
            arm.maxRight()  # could be the wrong way around
        elif b == "False":
            print("False")
            arm.maxLeft()
        else:
            print("else")
            arm.center()
        print(j["toggleArm"])

    if "toggleLegs" in j:
        print("toggleLegs")
        legs[0].setRandomMove(j["toggleLegs"], 0)
        legs[1].setRandomMove(j["toggleLegs"], 0)

    if "toggleHead" in j:
        print(j["toggleHead"])
        lights.setStatus(HEAD, j["toggleHead"])
    if "headColour" in j:
        print(j["headColour"])
        lights.setColour(HEAD, j["headColour"])
    if "headPulseRate" in j:
        print(j["headPulseRate"])
        lights.setPulseRate(HEAD, j["headPulseRate"])

    if "toggleChest" in j:
        print(j["toggleChest"])
        lights.setStatus(CHEST, j["toggleChest"])
    if "chestColour" in j:
        print(j["chestColour"])
        lights.setColour(CHEST, j["chestColour"])
    if "chestPulseRate" in j:
        print(j["chestPulseRate"])
        lights.setPulseRate(CHEST, j["chestPulseRate"])

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
    return wlan.isconnected()


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
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)
    print("Server initialised and listening")
    
    while True:
        try:
            print("waiting for accept:")
            client, address = sock.accept()
            print("client accepted")
            # Turn on LED
            
            handleConn(client, address)
        except Exception as e:
            lights.setColour(HEAD, "FF0000")
            lights.setPulseRate(HEAD, "0")
            print("End")
            client.close()
            try:
                handleInput("allOff")
            except:
                print("Network error, did not shut down correctly.")
            file = open("err/" + str(utime.gmtime()[0:5]) + ".txt", "w")
            file.write("Exception occured at: " + str(utime.gmtime()[0:5]))
            file.write(str(e))
            file.close()
            break
    print("Shutting Down...")

if __name__ == "__main__":

    # TODO: create some sort of start up procedure here.

    # Turn on basic LED.
    lights.setColour(HEAD, "0000FF")
    lights.setPulseRate(HEAD, "60")
    _thread.start_new_thread(loopLED, ())
    status = connectWIFI()
    if status == False:
        lights.setColour(HEAD, "FF0000")
        lights.setPulseRate(HEAD, "60")
    else:
        lights.setColour(HEAD, "000000")
        lights.setPulseRate(HEAD, "0")
        initServer()
