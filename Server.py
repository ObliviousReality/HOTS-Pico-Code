import network
import utime
import socket
from machine import Pin
import _thread

ssid = "LUSUINTERNET647"
password = "341Minimum*?@021"

def loopLED():
    led = Pin(0, Pin.OUT)
    led.low()
    print("In thread")
    while True:
        led.high()
        utime.sleep(1)
        led.low()
        utime.sleep(1)
        print("Loop!")
        

html = """
<!DOCTYPE html>
<html>
<body>
<h1>This is a server running on a raspberry pi</h1>
<p>Isn't that cool?</p>
</body>
</html>

"""


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
    print("Handle CONN")
    print("A Client has connected from address: ", addr)
    req = c.recv(1024)
    req = str(req)
    print(req)
    
    resp = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
    c.send(resp)
    c.send(html)
    c.close()
    
def initServer():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)
    print("Server initialised and listening")
    
    while True:
        try:
            print("waiting for accept:")
            client, address = sock.accept()
            print("client accepted")
            handleConn(client, address)
        except OSError as e:
            client.close()
            print("Error, connection closed.")
            break

if __name__ == "__main__":
    _thread.start_new_thread(loopLED,())
    connectWIFI()
    
    initServer()
    
    