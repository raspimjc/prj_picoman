from machine import Pin, PWM
import time
from time import sleep

led_haut = Pin(0,Pin.OUT)
led_haut.value(0)
led_bas = Pin(3,Pin.OUT)
led_bas.value(0)
led_droite = Pin(2,Pin.OUT)
led_droite.value(0)
led_gauche = Pin(1,Pin.OUT)
led_gauche.value(0)

boutton_haut = Pin(19,Pin.IN,Pin.PULL_UP)
boutton_bas = Pin(16,Pin.IN,Pin.PULL_UP)
boutton_droite = Pin(17,Pin.IN,Pin.PULL_UP)
boutton_gauche = Pin(18,Pin.IN,Pin.PULL_UP)

#pwm = PWM(Pin(27))

def boutton_haut_handler(pin):
    global led_haut
    led_haut.toggle()
def boutton_bas_handler(pin):
    global led_bas
    led_bas.toggle()
def boutton_droite_handler(pin):
    global led_droite
    led_droite.toggle()
def boutton_gauche_handler(pin):
    global led_gauche
    led_gauche.toggle()

boutton_haut.irq(trigger = machine.Pin.IRQ_RISING, handler = boutton_haut_handler)
boutton_bas.irq(trigger = machine.Pin.IRQ_RISING, handler = boutton_bas_handler)
boutton_droite.irq(trigger = machine.Pin.IRQ_RISING, handler = boutton_droite_handler)
boutton_gauche.irq(trigger = machine.Pin.IRQ_RISING, handler = boutton_gauche_handler)

'''
while True :
    led_bas.toggle()
    led_haut.toggle()
    led_droite.toggle()
    led_gauche.toggle()
    time.sleep(1)
'''

