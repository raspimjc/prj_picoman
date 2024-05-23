#==========================================#
# Seances                                  #
#==========================================#
# JANVIER:
# ========
#    - Codage complet des boutons et des leds
#
#    ==> Un appui sur un bouton allume ou eteint la led correspondante
#
    
#==========================================#
# Program                                  #
#==========================================#
from machine import Pin
import time
from time import sleep

#== Definition des boutons
bouton_haut = Pin(19, Pin.IN, Pin.PULL_UP)
bouton_bas = Pin(16, Pin.IN, Pin.PULL_UP) 
bouton_droite = Pin(17, Pin.IN, Pin.PULL_UP) 
bouton_gauche = Pin(18, Pin.IN, Pin.PULL_UP) 

#== Definition des leds
led_haut = Pin(0, Pin.OUT) 
led_bas = Pin(3, Pin.OUT) 
led_droite = Pin(2, Pin.OUT) 
led_gauche = Pin(1, Pin.OUT) 


#== Initialisation de la partie boutons
date_dernier_appui_haut = time.ticks_ms()
date_dernier_appui_bas = time.ticks_ms()
date_dernier_appui_droite = time.ticks_ms()
date_dernier_appui_gauche = time.ticks_ms()
bouton_haut_actif = False
bouton_bas_actif = False
bouton_droite_actif = False
bouton_gauche_actif = False

#== Initialisation des leds: eteintes
led_haut.value(0)
led_bas.value(0)
led_droite.value(0)
led_gauche.value(0)

#== Fonctions des boutons a associer aux handlers (Interruptions)
def bouton_haut_handler(pin):
    global bouton_haut_actif
    global date_dernier_appui_haut
    if time.ticks_diff(time.ticks_ms(), date_dernier_appui_haut) > 500: # evite les rebonds
        bouton_haut_actif = True
        date_dernier_appui_haut = time.ticks_ms() # "remise a zero"
def bouton_bas_handler(pin):
    global bouton_bas_actif
    global date_dernier_appui_bas
    if time.ticks_diff(time.ticks_ms(), date_dernier_appui_bas) > 500:
        bouton_bas_actif = True
        date_dernier_appui_bas = time.ticks_ms()
def bouton_droite_handler(pin):
    global bouton_droite_actif
    global date_dernier_appui_droite
    if time.ticks_diff(time.ticks_ms(), date_dernier_appui_droite) > 500:
        bouton_droite_actif = True
        date_dernier_appui_droite = time.ticks_ms()
def bouton_gauche_handler(pin):
    global bouton_gauche_actif
    global date_dernier_appui_gauche
    if time.ticks_diff(time.ticks_ms(), date_dernier_appui_gauche) > 500:
        bouton_gauche_actif = True
        date_dernier_appui_gauche = time.ticks_ms()
#== Association des fonctions ci dessus avec les interruptions
bouton_bas.irq(trigger = machine.Pin.IRQ_RISING, handler = bouton_bas_handler)
bouton_haut.irq(trigger = machine.Pin.IRQ_RISING, handler = bouton_haut_handler)
bouton_droite.irq(trigger = machine.Pin.IRQ_RISING, handler = bouton_droite_handler)
bouton_gauche.irq(trigger = machine.Pin.IRQ_RISING, handler = bouton_gauche_handler)

    
#==========================================#
# Programme principal                      #
#==========================================#

while True:
    #==== Joueur 1 = Boutons + LEDs pour ameliorer le visuel
    if bouton_haut_actif:
        bouton_haut_actif = False
        led_haut.toggle() 
    if bouton_bas_actif:
        bouton_bas_actif = False
        led_bas.toggle()
    if bouton_droite_actif:
        bouton_droite_actif = False
        led_droite.toggle()
    if bouton_gauche_actif:
        bouton_gauche_actif = False
        led_gauche.toggle()

