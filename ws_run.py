#
# web socket run module
#

from ws_connection import ClientClosedError as CCE
from ws_server import WebSocketServer as WSS, WebSocketClient as WSC
import network as net# type: ignore
import utime as utm# type: ignore
from bd_access import *

# global varuables
Ackf = False
#   input value
Din = 0  # digital input data
Ain = 0  # analog input data
Rns = 0  # range sensor input data
Tmp = 0  # temp sensor
Hum = 0  # hum sensor
chgflg = 0  # data change flag
ANPIN = const(0x01)  # analog input flag mask
DIPIN = const(0x02)  # digital input flag mask
RNSCK = const(0x04)  # range sensor check flag mask
TMPCK = const(0x08)  # temperature input flag mask
HUMCK = const(0x10)  # humidity input flag mask
ODNum = const(5)  # output data count


# websocket client
class TestClient(WSC):
    def __init__(self, conn):
        super().__init__(conn)
        self._mstick = 0
        self._odcnt = 0
        # print("TestClient")

    def process(self):
        global Ackf
        global chgflg
        # message check
        try:
            msg = self.connection.read()
            if not msg:
                # check board pin and sensor status change
                if (utm.ticks_ms() - self._mstick) > 50:
                    self._mstick = utm.ticks_ms()
                    if chgflg != 0:
                        omsg = [""]
                        if self._odcnt == 0 and (chgflg & DIPIN):
                            omsg = "diread=" + ("LOW" if Din == 0 else "High")
                            chgflg &= ~DIPIN
                        elif self._odcnt == 1 and (chgflg & ANPIN):
                            omsg = "anread=" + str(Ain) + " (0 to 1024)"
                            chgflg &= ~ANPIN
                        elif self._odcnt == 2 and (chgflg & RNSCK):
                            if Rns < 0:
                                omsg = "rnread=No response"
                            else:
                                omsg = "rnread=" + str(Rns) + " (cm)"
                            chgflg &= ~RNSCK
                        elif self._odcnt == 3 and (chgflg & TMPCK):
                            if Hum < 0:
                                omsg = "tmread=No response"
                            else:
                                omsg = "tmread=" + str(Tmp) + " (degree)"
                            chgflg &= ~TMPCK
                        elif self._odcnt == 4 and (chgflg & HUMCK):
                            if Hum < 0:
                                omsg = "hmread=No response"
                            else:
                                omsg = "hmread=" + str(Hum) + " (%)"
                            chgflg &= ~HUMCK
                        if len(omsg) > 7:
                            self.connection.write(omsg)
                        self._odcnt += 1
                        self._odcnt %= ODNum
                return
            # check received message
            msg = msg.decode("utf-8")
            items = msg.split(" ")
            # command check
            cmd = items[0]
            if cmd[:7] == "Connect":  # check "connect"
                self.connection.write("C-chk")
                print("Client connected")
            else:  # check input command
                while len(cmd) >= 5:
                    nump = 6 if len(cmd) > 5 and cmd[5] == ":" else 5
                    #
                    prme = -1
                    for i in range(5, len(cmd), 1):
                        if cmd[i] == "#":
                            prme = i
                            break
                    if cmd[:5] == "#C-OK":
                        Ackf = True
                        if boardled.value() is 0:
                            rledon_off(0)
                            self.connection.write("but1onn")
                        elif boardled.value() is 1:
                            self.connection.write("but1off")
                            rledon_off(1)
                        gledctrl(0)
                        srvctrl(0)
                        # msgdisp("")
                    elif cmd[:6] == "#RLED:":
                        if cmd[6:9] == "ONN":
                            if boardled.value() is not 0:
                                rledon_off(0)
                                self.connection.write("but1onn")
                        elif cmd[6:9] == "OFF":
                            if boardled.value() is not 1:
                                rledon_off(1)
                                self.connection.write("but1off")
                    elif cmd[:6] == "#GLED:":
                        val = int(cmd[6:] if prme < 0 else cmd[6:prme])
                        gledctrl(val)
                    elif cmd[:6] == "#SVCT:":
                        rotv = int(cmd[6:] if prme < 0 else cmd[6:prme])
                        srvctrl(rotv)
                    elif cmd[:6] == "#MSAG:":
                        print(f"Message received: {msg[6:]}")
                        # msgdisp(msg[6:])
                    if prme > 0:
                        cmd = cmd[prme:]
                    else:
                        break
        # connection close
        except CCE:
            self.connection.close()


# websocket server
class TestServer(WSS):
    def __init__(self, page):
        super().__init__(page, 1)

    def _make_client(self, conn):
        return TestClient(conn)


# wifi connection
def wificonn(SSID, password):
    wlan = net.WLAN(net.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, password)
        while not wlan.isconnected():
            utm.sleep(10)
            pass
    print("network config:", wlan.ifconfig())
    return wlan.ifconfig()[0]
