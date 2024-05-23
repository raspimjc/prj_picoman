#==========================================#
# Seances                                  #
#==========================================#
# JANVIER:
# ========
#    - Codage complet des boutons et des leds
#
#    ==> Un appui sur un bouton allume ou eteint la led correspondante
#
# FEVRIER:
# =======
#    - Atelier soudure
#    - Utilisation du code de la matrice (deja ecrit)
#    - Creation et codage du labyrinthe
#
#    ==> Le pixel "Joueur1" se déplace dans un labyrinthe 

#==========================================#
# Program                                  #
#==========================================#
from machine import Pin, SPI
import time
from time import sleep
import max7219

#==========================================#
# Declarations                             #
#==========================================#

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

#== Declaration de la matrice 8x8 MAX7219
cs_pin = 9 
spi = SPI(1) # Pins 9,10,11

#==========================================#
# Initialisations                          #
#==========================================#

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

#== Initialisation de la matrice
MAX7219_NUM = 4
MAX7219_INVERT = False
if (MAX7219_INVERT == False):
    ACTIVE_PIXEL = 1
else:
    ACTIVE_PIXEL = 0
MAX7219_SCROLL_DELAY = 0.05
display = max7219.Matrix8x8(spi=spi, cs=Pin(cs_pin), num=MAX7219_NUM)
display.brightness(2)
p = MAX7219_NUM * 8
x_pos = [0, 0] # Position horizontale du ou des joueurs
y_pos = [0, 0] # Position verticale du ou des joueurs

#==========================================#
# Fonctions                                #
#==========================================#

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
    
#== Fonctions qui vont gerer les deplacements des joueurs    
def deplacement_haut(joueur_id):
    global x_pos, y_pos
    if (y_pos[joueur_id] == 7):
        y_pos[joueur_id] = 0
    else:
        y_pos[joueur_id] = y_pos[joueur_id]+1
    
def deplacement_bas(joueur_id):
    global x_pos, y_pos
    if (y_pos[joueur_id] == 0):
        y_pos[joueur_id] = 7
    else:
        y_pos[joueur_id] = y_pos[joueur_id]-1
 
def deplacement_gauche(joueur_id):
    if (x_pos[joueur_id] == 31):
        x_pos[joueur_id] = 0
    else:
        x_pos[joueur_id]=x_pos[joueur_id]+1 
    
def deplacement_droite(joueur_id):
    if (x_pos[joueur_id] == 0):
        x_pos[joueur_id] = 31
    else:
        x_pos[joueur_id]=x_pos[joueur_id]-1 

#== Fonction qui va dessiner le labyrinthe sur la matrice de leds
def display_labyrinthe():
    offset = 0
    display.hline(4+offset, 2, 5, ACTIVE_PIXEL)  #Draw a line
    display.vline(4+offset, 2, 6, ACTIVE_PIXEL)  #Draw a column
    #************************************
    #* A FAIRE : Dessiner le labyrinthe sur une feuille
    #* et le coder
    #************************************
    display.hline(0,3,3,ACTIVE_PIXEL)
    display.vline(11,0,5,ACTIVE_PIXEL)
    display.hline(9,4,2,ACTIVE_PIXEL)
    display.vline(7,5,2,ACTIVE_PIXEL)
    display.hline(8,6,5,ACTIVE_PIXEL)
    display.hline(18,0,5,ACTIVE_PIXEL)
    display.hline(13,1,3,ACTIVE_PIXEL)
    display.vline(13,2,3,ACTIVE_PIXEL)
    display.vline(14,6,2,ACTIVE_PIXEL)
    display.hline(16,6,3,ACTIVE_PIXEL)
    display.vline(15,3,2,ACTIVE_PIXEL)
    display.hline(16,4,3,ACTIVE_PIXEL)
    display.hline(17,2,4,ACTIVE_PIXEL)
    display.vline(20,3,4,ACTIVE_PIXEL)
    display.hline(22,2,1,ACTIVE_PIXEL)
    display.hline(24,2,4,ACTIVE_PIXEL)
    display.vline(27,3,4,ACTIVE_PIXEL)
    display.hline(24,1,1,ACTIVE_PIXEL)
    
#==========================================#
# Programme principal                      #
#==========================================#

while True:
    #==== Joueur 1 = Boutons + LEDs (pour ameliorer le visuel)
    if bouton_haut_actif:
        bouton_haut_actif = False
        deplacement_haut(0)
        led_haut.toggle() 
    if bouton_bas_actif:
        bouton_bas_actif = False
        deplacement_bas(0)
        led_bas.toggle()
    if bouton_droite_actif:
        bouton_droite_actif = False
        deplacement_droite(0)
        led_droite.toggle()
    if bouton_gauche_actif:
        bouton_gauche_actif = False
        deplacement_gauche(0)
        led_gauche.toggle()
    #==== Affichage du plateau de jeu sur la matrice de leds
    display.fill(MAX7219_INVERT)
    display.pixel(x_pos[0],y_pos[0],ACTIVE_PIXEL) #Joueur1
    display_labyrinthe()  
    display.show()
    sleep(MAX7219_SCROLL_DELAY)

