#
# board input & outut access module
#

from machine import Pin, PWM, ADC, time_pulse_us  # type: ignore
import utime as utm  # type: ignore
import dht  # type: ignore
from ws_run import *
import ws_run
# import machine as mhn# type: ignore

# global variables
Rled_pin = 0
Gled_pin = 0
Din_pin = 0
Ain = ADC(0)
Serv_pin = 0
Rang_pin = 0
Dht_pin = 0
lcd = 0
Rmtick = 0
nrscnt = 0


# port initial set
def setprtini(lcdi, rled, gled, din, serv, rang, dhtp):
    global Rled_pin
    global Gled_pin
    global Din_pin
    global Serv_pin
    global Rang_pin
    global Dht_pin
    global lcd
    lcd = lcdi
    Rled_pin = Pin(rled, Pin.OUT)  # Red LED port instance
    Gled_pin = PWM(Pin(gled))  # Green LED port instance
    Gled_pin.freq(1000)  # set PWM period 1KHz
    Gled_pin.duty(0)
    Din_pin = Pin(din, Pin.IN)  # Digital input port instance
    Serv_pin = PWM(Pin(serv))  # Servo control port instance
    Serv_pin.freq(50)  # set 20ms interval
    Serv_pin.duty(0)
    Rang_pin = rang  # Range sensor pin number
    Dht_pin = dht.DHT11(Pin(dhtp))  # DHT11 port instance


# Red LED on/off
# def rledon_off(val):
#     if Rled_pin != 0: Rled_pin.value(1 if val > 0 else 0)

boardled = Pin(2, Pin.OUT)
boardled.value(1)


def rledon_off(val):
    if boardled != 0:
        boardled.value(1 if val > 0 else 0)
    if val > 0:
        print('LED OFF')
        # sock.sendall('OFF')
    else:
        print('LED ONN')
        # sock.sendall('ON')

# Green LED brightness ctrl


def gledctrl(val):
    if Gled_pin != 0:
        Gled_pin.duty(int(1023 * val / 100))


# servo angle control
def srvctrl(val):
    global Srvstbf
    SRVCENT = 1.45
    SRVSW = 0.95
    if Serv_pin != 0:
        dr = int(1024 * (SRVCENT + (float(-val) * SRVSW) / 90) / 20 + 0.5)
        Serv_pin.duty(dr)


# message display on the OLED
def msgdisp(msg):
    omsg = msg if len(msg) < 16 else msg[:15]
    lcd.fill_rect(8, 52, 120, 8, 0)
    lcd.text(omsg, 8, 52)
    lcd.show()


# range sensor working
def rngschk():
    global nrscnt
    rpi = Pin(Rang_pin, Pin.IN)
    rpi.irq(0, 0)
    rpo = Pin(Rang_pin, Pin.OUT)
    rpo.value(0)
    utm.sleep_us(10)
    rpo.value(1)
    utm.sleep_us(10)
    rpo.value(0)
    utm.sleep_us(10)
    rpi = Pin(Rang_pin, Pin.IN)
    rval = round(time_pulse_us(rpi, 1, 30000) * 34 / 2000, 2)
    if rval < 0 and nrscnt < 5:
        nrscnt += 1
    else:
        nrscnt = 0
    if rval < 150 and rval >= 0:
        ws_run.Rns = rval
    elif nrscnt >= 5:
        ws_run.Rns = -1
    ws_run.chgflg |= ws_run.RNSCK


# temp sensor working
def dhtchk():
    excptflg = False
    try:
        Dht_pin.measure()
    except OSError:
        excptflg = True
    if excptflg:
        ws_run.Hum = -1
    else:
        ws_run.Tmp = Dht_pin.temperature()
        ws_run.Hum = Dht_pin.humidity()
    ws_run.chgflg |= ws_run.TMPCK | ws_run.HUMCK


# input status tansfer
def inpsts():
    ws_run.Din = Din_pin.value()
    ws_run.Ain = Ain.read()
    ws_run.chgflg |= ws_run.ANPIN | ws_run.DIPIN


#
