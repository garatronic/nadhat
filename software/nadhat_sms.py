# -*- coding: utf-8 -*-
#
#               sms.py
# Programme destiné à envoyer un SMS en réponse à un SMS de requête
# Le SMS reçu doit contenir Temp
# d'après http://www.python-exemplary.com
# Envoie le SMS à un N° de téléphone indiqué dans le programme
# Le SIM800C doit être éteint au lancement du programme
# car on le met en service d'abord
#
#

import wiringpi
import serial
import time, sys
import datetime
import os, signal

# Port série (à adapter en fonction de votre Raspberry Pi Zero, 2 ou 3)
PORT_SERIE = "/dev/ttyAMA0"

# Numéros de téléphone

FREE ="+33695000695"

# getCPUtemperature : lit la température du CPU
# Renvoie la température CPU
# sous forme d'une chaîne de caractères

def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

# Gestion du CTRL C
def signal_handler(signal, frame):
        print"Sortie du programme par Ctrl+C!"
        ser.write("at")
        time.sleep(2)
        ser.write("at+cpowd=1")
        print "Arrêt du SIM800C"
        time.sleep(2)
        sys.exit(0)

# Extraire le numero de l'appelant
def telephone(chaine):
        debut = chaine.find('+33')
        fin = debut + 12
        numero = chaine[debut:fin]
        print "Appelant : " + numero
        return (numero)


# Initialisation du port série

ser = serial.Serial(
    port = PORT_SERIE,
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 3
)

# Démarrer le SIM800C
# GPIO utilise pour commander le PWR du SIM800C
POWER_KEY_GPIO = 26

# Utiliser la numerotation GPIO
wiringpi.wiringPiSetupGpio()

# Mettre le GPIO en mode sortie = 1
wiringpi.pinMode(POWER_KEY_GPIO,1)

# Envoyer une impulsion au SIM800C
wiringpi.digitalWrite(POWER_KEY_GPIO,1)
time.sleep(1)
wiringpi.digitalWrite(POWER_KEY_GPIO,0)

# Avertir l'utilisateur
s = "Le SIM800C a reçu l'ordre de démarrage"
print s

time.sleep(5)

# Vérifier la communication avec la carte NadHAT

ser.write("AT\r") # envoie la commande AT
time.sleep(3) # Laisse le temps au SIM800C de répondre

rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
if rep != "":
    print "Réponse reçue de la carte NadHAT :"
    print rep
    if "OK" in rep:
        print "La liaison avec la carte NadHAT fonctionne et le SIM800C fonctionne"
    else :
        print "Pas de communication avec la carte NadHAT"
        sys.exit(0)
else :
    print "La carte ne répond pas"
    sys.exit(1)

# Entrer le code PIN
ser.write("AT+CPIN=1234\r")
print "Code PIN envoyé... Attente 10 secondes."
time.sleep(5)
print "Encore 5 secondes..."
time.sleep(5)
print "Vérifiez le clignottement lent de la LED..."

# Entrer le numéro de Free
ser.write('AT+CSCA="+33695000695"\r')

# Passer en mode texte
ser.write("AT+CMGF=1\r")
time.sleep(3)

# Détruire les SMS présents
ser.write('AT+CMGDA="DEL ALL"\r')
time.sleep(3)

# Nettoyer le buffer
reply = ser.read(ser.inWaiting())

#Mise en attente d'un SMS
print "En attente de l'arrivée d'un SMS..."
while True:
    # Sortie du programme ?
    signal.signal(signal.SIGINT, signal_handler)

    # Lire le buffer
    reply = ser.read(ser.inWaiting())

    # Si un SMS a été reçu la réponse est différente de ""
    if reply != "":
        ser.write("AT+CMGR=1\r")
        time.sleep(3)
        reply = ser.read(ser.inWaiting())

        # Lire le SMS reçu
        print "SMS reçu. Contenu :"
        print reply
        # Si le SMS contient Temp
        if "Temp" in reply:
            tel=telephone(reply)
            t = str(datetime.datetime.now())
            # Répondre au SMS
            print ('AT+CMGS="' + tel + '"\r')
            ser.write('AT+CMGS="' + tel + '"\r')
            time.sleep(3)
            # Lire la température CPU
            tempCPU = int(float(getCPUtemperature()))
            msg = "Il est " + t + "\r Temperature CPU : " + str(tempCPU) +"degres\r\n"
            print "Envoi du SMS avec la température CPU :\r\n" + msg + "\r\n à " + tel
            ser.write(msg + chr(26))
        time.sleep(3)
        ser.write('AT+CMGDA="DEL ALL"\r') # Supprime tout
        time.sleep(3)
        ser.read(ser.inWaiting()) # Vide le buffer
    time.sleep(2)
