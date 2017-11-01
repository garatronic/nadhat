# -*- coding: utf-8 -*-
#
# mms.py
# Script to send a MMS
#
import nadhat_pwr_on
import nadhat_pwr_off
import wiringpi
import serial
import time, sys
import datetime
import os, signal
import argparse

operator_sms_dict = {'ORANGE': '+33689004000', 'SFR': '+33609001390', 'FREE': '+33695000695', 'BOUYGUES': '+33660660001', 'ORANGE_CARAIBES': '+590690350012'}
operator_mms_url_dict = {'ORANGE': 'http://mms.orange.fr', 'SFR': 'http://mms.sfr.fr', 'FREE': 'http://mms1', 'BOUYGUES': 'http://mms.bouyguestelecom.fr/mms/wapenc', 'ORANGE_CARAIBES': ''}
operator_mms_proxy_dict = {'ORANGE': '192.168.10.200', 'SFR': '10.151.0.1', 'FREE': '212.27.40.225', 'BOUYGUES': '62.201.129.226', 'ORANGE_CARAIBES': ''}
operator_mms_port_dict = {'ORANGE': '8080', 'SFR': '8080', 'FREE': '80', 'BOUYGUES': '8080', 'ORANGE_CARAIBES': ''}
operator_mms_apn_dict = {'ORANGE': 'orange.acte', 'SFR': 'mmssfr', 'FREE': 'mmsfree', 'BOUYGUES': 'mmsbouygtel.com', 'ORANGE_CARAIBES': ''}

# Contenu MMS 
PIC = 1
TITLE = 0
TEXT = 0

#MAILFROM = "ihoratius@garatronic.fr"

##############Begin process command line ###########
parser = argparse.ArgumentParser(description='Configure and send your mms. command line could be: python mms.py "+336XXXXXXXX" "pic.jpg" -o ORANGE -cp 0000 -p "/dev/ttyAMA0"')

parser.add_argument('RN', type=str, help='Receiver number. ex: "+336XXXXXXXX"')

parser.add_argument('pic', type=str, help='picture path. ex: "pic.jpg"')

parser.add_argument('--title', '-t',
                    help='title file text. ex "title.txt"', 
                    type=str)

parser.add_argument('--text', '-txt',
                    help='text file text. ex "text.txt"', 
                    type=str)

parser.add_argument('--operator', '-o',
                    help='Service provider',
                    choices=['ORANGE', 'SFR', 'FREE', 'BOUYGUES', 'ORANGE_CARAIBES'],
                    default='ORANGE')
					
parser.add_argument('--cpin', '-cp',
                    help='Pin code',
                    type=str,
                    default='0000')

parser.add_argument('--port', '-p',
                    help='Serial port',
                    type=str,
                    default='/dev/ttyAMA0')

title = ""
text = ""

args = parser.parse_args()
operator_sms = operator_sms_dict[args.operator]
receiver_nb = args.RN
serial_port = args.port
code_pin = args.cpin
pic = args.pic
title = args.title
text = args.text
operator_mms_url = operator_mms_url_dict[args.operator]
operator_mms_proxy = operator_mms_proxy_dict[args.operator]
operator_mms_port = operator_mms_port_dict[args.operator]
operator_mms_apn = operator_mms_apn_dict[args.operator]

if title:
    TITLE = 1
if text:
    TEXT = 1
    
print "center_sms="+args.operator+", receiver_nb="+receiver_nb+", serial_port="+serial_port+", code_pin="+code_pin+", pic="+pic+", operator_mms_url="+operator_mms_url+", operator_mms_proxy="+operator_mms_proxy+", operator_mms_port="+operator_mms_port+", operator_mms_apn="+operator_mms_apn
#print center_sms
##############End process command line ###########

# Wait for the nadhat answer
def wait_Answer(code):
    time.sleep(2)
    rep = ser.read(ser.inWaiting()) # Check if the nadhat answers 
    if rep != "":
        if code in rep:
            print "Answers : "+code
        else :
            print code+" not received : No communication with the nadhat board"
            sys.exit(0)
    else :
        print "No response from the board"
        sys.exit(1)
		
# Serial port init
ser = serial.Serial(
    port = serial_port,
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)

# Read file size
def taille_fichier(nom_fichier):
    taille = os.stat(nom_fichier)
    return taille.st_size

# Start the SIM800C
nadhat_pwr_on.pwr_on()
time.sleep(5)

# Check the communication with the nadhat board
ser.write("AT\r") # Send AT command
wait_Answer("OK")

# Send the pin code
ser.write("AT+CPIN="+code_pin+"\r")
print "Code PIN sent... wait 10 secondes."
time.sleep(5)
print "Wait for 5 more seconds..."
time.sleep(5)
print "Check the slow blinking LED rate..."
wait_Answer("OK")

# Set MMS mode
ser.write('AT+CMMSINIT\r')
print "AT+CMMSINIT\r"
wait_Answer("OK")

# The URL to be sending the MMS
ser.write('AT+CMMSCURL="'+operator_mms_url+'"\r')
print 'AT+CMMSCURL="'+operator_mms_url+'"\r'
wait_Answer("OK")

# Define the bearer ID
ser.write('AT+CMMSCID=1\r')
print "AT+CMMSCID=1\r"
wait_Answer("OK")

# MMS Proxy
ser.write('AT+CMMSPROTO="'+operator_mms_proxy+'",'+operator_mms_port+'\r')
print 'AT+CMMSPROTO="'+operator_mms_proxy+'",'+operator_mms_port+'\r'
wait_Answer("OK")

# MMS Send configration
ser.write('AT+CMMSSENDCFG=1,1,0,0,1,4,2,0\r')
print "AT+CMMSSENDCFG=1,1,0,0,1,4,2,0\r"
wait_Answer("OK")
# MMS Send configration -> save
ser.write('AT+CMMSSCONT\r')
print "AT+CMMSSCONT\r"
wait_Answer("OK")

# Define the bearer settings
ser.write('AT+SAPBR=3,1,"Contype","GPRS"\r')
print 'AT+SAPBR=3,1,"Contype","GPRS"\r'
wait_Answer("OK")

# Define bearer context
ser.write('AT+SAPBR=3,1,"APN","'+operator_mms_apn+'"\r')
print 'AT+SAPBR=3,1,"APN","'+operator_mms_apn+'"\r'
wait_Answer("OK")

# Active bearer context
ser.write('AT+SAPBR=1,1\r')
print "AT+SAPBR=1,1\r"
wait_Answer("OK")

# Display the context for checking
ser.write('AT+SAPBR=2,1\r')
print "AT+SAPBR=2,1\r"
time.sleep(2)
rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
if rep != "":
    print "Response : "+ rep + "\r"
else :
    print "No response for the bearer settings AT+SAPBR=2,1\r"
    sys.exit(0)
# On vérifie également que la carte a répondu OK	
if not ("OK" in rep):
    print "Communication problem with the NadHAT board: OK not received"
    sys.exit(0)

# Start the mms editing mode 
ser.write('AT+CMMSEDIT=1\r')
print "AT+CMMSEDIT=1\r"
wait_Answer("OK")

# ============= ENVOI DU MMS : IMAGE ================
if (PIC):
	
	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille de l'image
	taille = taille_fichier(pic)
	print "Taille de l'image à envoyer : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="PIC",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="PIC",' + str(taille) +',' +str(timeout) + '\r'
	wait_Answer("CONNECT")

	# Envoi du fichier sur le port série
	with open(pic, "rb") as f:
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
	wait_Answer("OK")

# ============= ENVOI DU MMS : TITRE ================

if (TITLE):

	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille de l'image
	taille = taille_fichier("title.txt")
	print "Size of the title file to send : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="TITLE",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="TITLE",' + str(taille) +',' +str(timeout) + '\r'
	wait_Answer("CONNECT")

	# Envoi du fichier sur le port série
	with open("title.txt", "rb") as f:
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
	wait_Answer("OK")

# ============= ENVOI DU MMS : TEXTE ================

if (TEXT):
	
	# Temps d'envoi du fichier dans le MMS
	timeout = 60000
	# Trouver la taille du texte
	taille = taille_fichier("text.txt")
	print "Size of the text file to send : " + str(taille) + "\r"

	# Envoyer le fichier
	ser.write('AT+CMMSDOWN="TEXT",' + str(taille) + ',' + str(timeout) + '\r')
	print 'AT+CMMSDOWN="TEXT",' + str(taille) +',' +str(timeout) + '\r'
	wait_Answer("CONNECT")

	# Envoi du fichier sur le port série
	with open("text.txt", "rb") as f:
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
	wait_Answer("OK")

# Recipient number
ser.write('AT+CMMSRECP="' + receiver_nb + '"\r')
print 'AT+CMMSRECP="' + receiver_nb + '"\r'
wait_Answer("OK")

# Sender mail adress
#ser.write('AT+CMMSBCC=' + MAILFROM + '\r')
#print 'AT+CMMSBCC=' + MAILFROM + '\r'
#wait_Answer("OK")
	
# Checking the MMS before sending
ser.write('AT+CMMSVIEW\r')
print "AT+CMMSVIEW\r"
time.sleep(2)
rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
if rep != "":
    print "Response : "+ rep + "\r"
else :
    print "No response for the MMS checking\r"
    sys.exit(0)
# On vérifie également que la carte a répondu OK	
if not ("OK" in rep):
    print "Communication problem with the NadHAT board: OK not received"
    sys.exit(0)

# Send the MMS
ser.write("AT+CMMSSEND\r")
print "AT+CMMSSEND\r"

# Wait for the reponded code (can take a long time)
time.sleep(1)
rep = ser.read(ser.inWaiting()) # vide le buffer
print "Wait for the SIM800C feedback(can take a long time)\r"
rep = ""
while rep == "":
	rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
	time.sleep(1)
print "Response : "+ rep + "\r"

# Exit the MMS mode and remove the MMS from the buffer
ser.write('AT+CMMSEDIT=0\r')
print "AT+CMMSEDIT=0\r"
wait_Answer("OK")

# Stop the SIM800C
nadhat_pwr_off.pwr_off()

