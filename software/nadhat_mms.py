# -*- coding: utf-8 -*-
#
#               mms.py
# Programme destiné à envoyer un MMS
# Envoie le MMS à un N° de téléphone indiqué dans le programme
# Le SIM800C doit être éteint au lancement du programme
# car on le met en service d'abord
#
# D'après sim800_series_mms_application_note_v1.00

import wiringpi
import serial
import time, sys
import datetime
import os, signal

# Port série (à adapter en fonction de votre Raspberry Pi Zero, 2 ou 3)
PORT_SERIE = "/dev/ttyAMA0"


# Numéros de téléphone operateur 
#FREE ="+33695000695"
SOSH ="+33679343291"

# Destinataire MMS : à renseigner
DEST = "+336xxxxxxxx"

# Choix de l'operateur
#operator = "FREE"
operator = "ORANGE"

# Contenu MMS 
PIC = 1
TITLE = 1
TEXT = 1

# getCPUtemperature : lit la température du CPU
# Renvoie la température CPU
# sous forme d'une chaîne de caractères

# Gestion du CTRL C
def signal_handler(signal, frame):
        print"Sortie du programme par Ctrl+C!"
        ser.write("at")
        time.sleep(2)
        ser.write("at+cpowd=1")
        print "Arrêt du SIM800C"
        time.sleep(2)
        sys.exit(0)
		
# Attente de la réponse OK
# Laisse 2 secondes au SIM800C pour répondre et teste si la réponse est arrivée
def attend_OK():
    time.sleep(2)
    rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
    if rep != "":
        if "OK" in rep:
            print "Réponse : OK"
        else :
            print "OK non reçu : Pas de communication avec la carte NadHAT"
            sys.exit(0)
    else :
        print "La carte ne répond pas"
        sys.exit(1)
		
# Attente de la réponse CONNECT
# Laisse 2 secondes au SIM800C pour répondre et teste si la réponse est arrivée
def attend_CONNECT():
    time.sleep(2)
    rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
    if rep != "":
        if "CONNECT" in rep:
            print "Réponse : CONNECT"
        else :
            print "CONNECT non reçu : " + rep + " Pas de communication avec la carte NadHAT"
            sys.exit(0)
    else :
        print "attend_CONNECT : La carte ne répond pas"
        sys.exit(1)
		
# Lire la taille d'un fichier
def taille_fichier(nom_fichier):
    taille = os.stat(nom_fichier)
    return taille.st_size		

# Initialisation du port série du Raspberry Pi
ser = serial.Serial(
    port = PORT_SERIE,
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 3
)

# ============= DEMARRAGE DU SIM800C ==================
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

# Entrer le code PIN si carte non débloquée
#ser.write("AT+CPIN=1234\r")
#print "Code PIN envoyé... Attente 10 secondes."
time.sleep(5)
print "Encore 5 secondes..."
time.sleep(5)
print "Vérifiez le clignottement lent de la LED..."

# ============ ENVOIE D'UN MMS ==============================
# le contenu du MMS est une image présente dans le dossier /home/pi
# /home/pi/image0.jpg 
#
# Passer le SIM800C en mode MMS
ser.write('AT+CMMSINIT\r')
print "AT+CMMSINIT\r"
attend_OK()

# URL à laquelle envoyer le MMS
if operator == "FREE" :
	ser.write('AT+CMMSCURL="http://mms.free.fr"\r')
	print "AT+CMMSCURL='http://mms.free.fr'\r"
else :
	ser.write('AT+CMMSCURL="http://mms.orange.fr"\r')
	print "AT+CMMSCURL='http://mms.orange.fr'\r"

attend_OK()

# Définir l'ID du contexte du bearer (transporteur)
ser.write('AT+CMMSCID=1\r')
print "AT+CMMSCID=1\r"
attend_OK()

# MMS Proxy
if operator == "FREE" :
	ser.write('AT+CMMSPROTO="212.27.40.225",80\r')
	print "AT+CMMSPROTO='212.27.40.225',80\r"
else :
	ser.write('AT+CMMSPROTO="192.168.10.200",8080\r')
	print "AT+CMMSPROTO='192.168.10.200',8080\r"
attend_OK()

# MMS Send configration
ser.write('AT+CMMSSENDCFG=1,1,0,0,1,4,2,0\r')
print "AT+CMMSSENDCFG=1,1,0,0,1,4,2,0\r"
attend_OK()
# MMS Send configration -> save
ser.write('AT+CMMSSCONT\r')
print "AT+AT+CMMSSCONT\r"
attend_OK()

# Définir les paramètres du bearer
ser.write('AT+SAPBR=3,1,"Contype","GPRS"\r')
print 'AT+SAPBR=3,1,"Contype","GPRS"\r'
attend_OK()

# Définir le contexte du bearer (transporteur)
if operator == "FREE" :
	ser.write('AT+SAPBR=3,1,"APN","mmsfree"\r')
	print 'AT+SAPBR=3,1,"APN","mmsfree"\r'
else :
	ser.write('AT+SAPBR=3,1,"USER","orange"\r')
	print 'AT+SAPBR=3,1,"USER","orange"\r'
	attend_OK()
	ser.write('AT+SAPBR=3,1,"PWD","orange"\r')
	print 'AT+SAPBR=3,1,"PWD","orange"\r'
	attend_OK()
	ser.write('AT+SAPBR=3,1,"APN","orange"\r')
	print 'AT+SAPBR=3,1,"APN","orange"\r'
attend_OK()

# Activer le contexte du bearer (transporteur)
ser.write('AT+SAPBR=1,1\r')
print "AT+SAPBR=1,1\r"
attend_OK()

# Afficher le contexte pour vérification
ser.write('AT+SAPBR=2,1\r')
print "AT+SAPBR=2,1\r"
time.sleep(2)
rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
if rep != "":
    print "Réponse : "+ rep + "\r"
else :
    print "Pas de réponse pour les paramètres du bearer AT+SAPBR=2,1\r"
    sys.exit(0)
# On vérifie également que la carte a répondu OK	
if not ("OK" in rep):
    print "Problème de communication avec la carte NadHAT : pas de OK reçu"
    sys.exit(0)

# ============= ENVOI DU MMS ========================

# Entrer en mode Edition de MMS
ser.write('AT+CMMSEDIT=1\r')
print "AT+CMMSEDIT=1\r"
attend_OK()

# ============= ENVOI DU MMS : IMAGE ================

if (PIC):
	
	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille de l'image
	taille = taille_fichier("image0.jpg")
	print "Taille de l'image à envoyer : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="PIC",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="PIC",' + str(taille) +',' +str(timeout) + '\r'
	attend_CONNECT()

	# Envoi du fichier sur le port série
	with open("image0.jpg", "rb") as f:
		octet = f.read(1)
		while octet != "":
			ser.write(octet)	
			# Afficher l'octet sauf si c'est une commande (< 0x10)
			# puis l'envoyer sur le port série
			if (octet < 0x10) :
				print "-- ",
			else :
				print hex(ord(octet)) + " ",
			octet = f.read(1)

	# Attendre le retour du SIM800C
	attend_OK()

# ============= ENVOI DU MMS : TITRE ================

if (TITLE):

	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille de l'image
	taille = taille_fichier("title0.txt")
	print "Taille du fichier titre à envoyer : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="TITLE",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="TITLE",' + str(taille) +',' +str(timeout) + '\r'
	attend_CONNECT()

	# Envoi du fichier sur le port série
	with open("title0.txt", "rb") as f:
		octet = f.read(1)
		while octet != "":
			ser.write(octet)	
			# Afficher l'octet sauf si c'est une commande (< 0x10)
			# puis l'envoyer sur le port série
			if (octet < 0x10) :
				print "-- ",
			else :
				print hex(ord(octet)) + " ",
			octet = f.read(1)

	# Attendre le retour du SIM800C
	attend_OK()

# ============= ENVOI DU MMS : TEXTE ================

if (TEXT):
	
	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille du texte
	taille = taille_fichier("texte0.txt")
	print "Taille du fichier texte à envoyer : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="TEXT",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="TEXT",' + str(taille) +',' +str(timeout) + '\r'
	attend_CONNECT()

	# Envoi du fichier sur le port série
	with open("texte0.txt", "rb") as f:
		octet = f.read(1)
		while octet != "":
			ser.write(octet)	
			# Afficher l'octet sauf si c'est une commande (< 0x10)
			# puis l'envoyer sur le port série
			if (octet < 0x10) :
				print "-- ",
			else :
				print hex(ord(octet)) + " ",
			octet = f.read(1)

	# Attendre le retour du SIM800C
	attend_OK()

# Numero du premier destinataire
ser.write('AT+CMMSRECP=' + DEST + '\r')
print 'AT+CMMSRECP=' + DEST + '\r'
attend_OK()

# Adresse mail de l'expediteur
ser.write('AT+CMMSBCC=' + MAILFROM + '\r')
print 'AT+CMMSBCC=' + MAILFROM + '\r'
attend_OK()

# Vérifier ce qui va être envoyé pour vérification
ser.write('AT+CMMSVIEW\r')
print "AT+CMMSVIEW\r"
time.sleep(2)
rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
if rep != "":
    print "Réponse : "+ rep + "\r"
else :
    print "Pas de réponse pour la vérification du MMS\r"
    sys.exit(0)
# On vérifie également que la carte a répondu OK	
if not ("OK" in rep):
    print "Problème de communication avec la carte NadHAT : pas de OK reçu"
    sys.exit(0)

# Envoyer le MMS
ser.write("AT+CMMSSEND\r")
print "AT+CMMSSEND\r"

# Attente du code retour (peut être long)
time.sleep(1)
rep = ser.read(ser.inWaiting()) # vide le buffer
print "Attente du retour SIM800C (peut etre long)\r"
rep = ""
while rep == "":
	rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
	time.sleep(1)
print "Réponse : "+ rep + "\r"

# Sortir du mode MMS et enlever le MMS du buffer
ser.write('AT+CMMSEDIT=0\r')
print "AT+CMMSEDIT=0\r"
attend_OK()

# =============  ARRETER le SIM800C ==============
execfile ("nadhat_halt.py")
sys.exit(0)
