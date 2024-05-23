
# SEANCE 1:
# =========
#    - Codage complet des boutons et des leds
#    ==> Un appui sur un bouton allume ou eteint la led correspondante
#
# SEANCE 2:
# ========
#    - Atelier soudure
#    - Utilisation du code de la matrice (deja ecrit)
#    - Creation et codage du labyrinthe
#
#    ==> Le pixel "Joueur1" se déplace dans un labyrinthe 
#
# SEANCE 3:
# ========
#    - Ajout du Buzzer 
#    - Codage musique theme "mission impossible"
#
# AJOUTS HORS SEANCE:
# ===================
#    - Ajout des fantomes (joueurs 3 et 4): Deplacements aléatoires
#    - Code pour rendre les murs infranchissables
#    - Ajout du joystick


#==========================================#
# Program                                  #
#==========================================#
from machine import Pin, SPI, PWM, ADC
import time
from time import sleep
import max7219
import random

#==========================================#
# Configuration du jeu                     #
#==========================================#

CFG_SILENCE = True

CFG_VITESSE_FANTOMES = 200#400#800

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

#== Declaration du buzzer
buzzer = PWM(Pin(8)) 

#== Declaration du joystick
xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))

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

#== Initialisation des joueurs et fantomes = Positions de départ
# 0 = Joueur 1 (boutons)
# 1 = Joueur 2 (joystick)
# 3 et 4 = Fantomes
x_pos = [0,0, 8, 24] 
y_pos = [0,0, 4,  7]

#== Initialisation des fantomes
date_dernier_selection_fantomes = time.ticks_ms()

#== Initialisation du joystick
date_dernier_selection_joystick = time.ticks_ms()

#==========================================#
# Fonctions                                #
#==========================================#
#== Fonction buzzer_note: il va jouer une mélodie note par note a chaque appui
index_note = 0
def buzzer_note():
    global buzzer, index_note
    do = 523  
    do_d = 554
    re_b = 554
    re = 587  
    re_d = 622
    mi_b = 622
    mi = 659
    fa = 698
    fa_d = 740
    so_b = 740
    so = 784
    so_d = 830
    la_b = 830
    la = 880
    la_d = 932
    si_b = 932
    si = 988
    notes = [la,la,do,re,la,la,so,la_b,  
             la,la,do,re,la,la,so,la_b,
             do,la,mi,
             do,la,re_d,
             do,la,re,do,re] #mission impossible: liste des notes   
    duree = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,  
             0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,
             0.125,0.125,1.5,
             0.125,0.125,1.5,
             0.125,0.125,1.5,0.125,0.25] #mission impossible: duree de chaque note
    if CFG_SILENCE == False:
        buzzer.freq(notes[index_note]) 
        buzzer.duty_u16(400) #niveau sonore
        sleep(duree[index_note])
        buzzer.duty_u16(0) #close
        #sleep(0.01)
        if (index_note < (len(notes)-1)):    
            index_note = index_note + 1
        else:
          index_note = 0

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
    
#== Fonctions qui vont gerer les deplacements de TOUS LES joueurs et des fantomes   
def deplacement_haut(joueur_id):
    global x_pos, y_pos
    if (y_pos[joueur_id] == 7):
        y_new = 0
    else:
        y_new = y_pos[joueur_id]+1
    if ((x_pos[joueur_id],y_new) not in liste_coordonnees_murs):
        y_pos[joueur_id] = y_new
    
def deplacement_bas(joueur_id):
    global x_pos, y_pos
    if (y_pos[joueur_id] == 0):
        y_new = 7
    else:
        y_new = y_pos[joueur_id]-1
    if ((x_pos[joueur_id],y_new) not in liste_coordonnees_murs):
        y_pos[joueur_id] = y_new
        
def deplacement_gauche(joueur_id):
    if (x_pos[joueur_id] == 31):
        x_new = 0
    else:
        x_new=x_pos[joueur_id]+1 
    if ((x_new,y_pos[joueur_id]) not in liste_coordonnees_murs):
        x_pos[joueur_id] = x_new
        
def deplacement_droite(joueur_id):
    if (x_pos[joueur_id] == 0):
        x_new = 31
    else:
        x_new=x_pos[joueur_id]-1 
    if ((x_new,y_pos[joueur_id]) not in liste_coordonnees_murs):
        x_pos[joueur_id] = x_new
        
#== Fonction qui va dessiner le labyrinthe sur la matrice de leds
liste_coordonnees_murs=[]

def display_hline(x, y, h):
    global liste_coordonnees_murs
    for i in range (x,x+h):        
        if ((i,y) not in liste_coordonnees_murs):        
            liste_coordonnees_murs.append((i,y))
    display.hline(x, y, h, ACTIVE_PIXEL)
    #print ("...")
    #print (liste_coordonnees_murs)

def display_vline(x, y, h):
    global liste_coordonnees_murs
    for j in range (y,y+h):        
        if ((x,j) not in liste_coordonnees_murs):        
            liste_coordonnees_murs.append((x,j))
    display.vline(x, y, h, ACTIVE_PIXEL)
    #print ("...")
    #print (liste_coordonnees_murs)
                  
def display_labyrinthe():
    display_hline(4, 2, 5)  #Draw a line
    display_vline(4, 2, 6)  #Draw a column
    #************************************
    #* A FAIRE : Dessiner le labyrinthe sur une feuille
    #* et le coder
    #************************************
    display_hline(0,3,3)
    ##display_vline(11,0,5)
    #display_hline(9,4,2)
    display_vline(7,5,2)
    ##display_hline(8,6,5)
    #display_hline(18,0,5)
    display_hline(13,1,3)
    display_vline(13,2,3)
    #display_vline(14,6,2)
    display_hline(16,6,3)
    ##display_vline(15,3,2)
    display_hline(16,4,3)
    #display_hline(17,2,4)
    ##display_vline(20,3,4)
    display_hline(22,2,3)
    #display_hline(24,2,4)
    ##display_vline(27,3,4)
    #display_hline(24,1,1)
    
#==========================================#
# Programme principal                      #
#==========================================#

while True:
    #==== Joue une musique pendant le jeu
    buzzer_note()
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
    #==== Joueur 2 = Joystick
    if time.ticks_diff(time.ticks_ms(), date_dernier_selection_joystick) > CFG_VITESSE_FANTOMES: 
        date_dernier_selection_joystick = time.ticks_ms() # "remise a zero"
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()            
        if (xValue > 60000):
            deplacement_gauche(1)
        elif (xValue < 1500):
            deplacement_droite(1)
        elif (yValue > 60000):
            deplacement_haut(1)
        if (yValue < 1500):
            deplacement_bas(1)        
    #==== Fantomes
    if time.ticks_diff(time.ticks_ms(), date_dernier_selection_fantomes) > CFG_VITESSE_FANTOMES: 
        date_dernier_selection_fantomes = time.ticks_ms() # "remise a zero"
        xValue = random.randint(0, 80000)
        yValue = random.randint(0, 80000)            
        if (xValue > 60000):
            deplacement_bas(2)
            deplacement_droite(3)
        elif (xValue < 1500):
            deplacement_haut(2)
            deplacement_gauche(3)
        elif (yValue > 60000):
            deplacement_droite(2)
            deplacement_bas(3)
        if (yValue < 1500):
            deplacement_gauche(2)
            deplacement_haut(3)        
    #==== Affichage du plateau de jeu sur la matrice de leds
    display.fill(MAX7219_INVERT)
    display.pixel(x_pos[0],y_pos[0],ACTIVE_PIXEL) #Joueur1
    display.pixel(x_pos[1],y_pos[1],ACTIVE_PIXEL) #Joueur2    
    display.pixel(x_pos[2],y_pos[2],ACTIVE_PIXEL) #Fantome1
    display.pixel(x_pos[3],y_pos[3],ACTIVE_PIXEL) #Fantome2
    display_labyrinthe()  
    display.show()
    sleep(MAX7219_SCROLL_DELAY)
    #==== Evaluation du jeu: Echec si position joueurs == position fantomes
    if ((x_pos[0] == x_pos[2]) & (y_pos[0] == y_pos[2])) | ((x_pos[0] == x_pos[3]) & (y_pos[0] == y_pos[3])):
        #Affichage du message d'erreur
        while True:
            display.fill(MAX7219_INVERT)
            display.text('1-ko',0,0,1)
            display.show()
    if ((x_pos[1] == x_pos[2]) & (y_pos[1] == y_pos[2])) | ((x_pos[1] == x_pos[3]) & (y_pos[1] == y_pos[3])):
        #Affichage du message d'erreur
        while True:
            display.fill(MAX7219_INVERT)
            display.text('2-ko',0,0,1)
            display.show()



