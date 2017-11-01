# -*- coding: utf-8 -*-
#
#               nadhat_halt.py
# Programme destiné à arrêter le SIM800C
#

import wiringpi
import serial
import time, sys
import datetime
import os, signal

# Port série (à adapter en fonction de votre Raspberry Pi Zero, 2 ou 3)
PORT_SERIE = "/dev/ttyAMA0"

# Initialisation du port série

ser = serial.Serial(
    port = PORT_SERIE,
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)

def pwr_off():
 # Vérifier la communication avec la carte NadHAT
 print "Stop in progress...\r\n"
 ser.write("AT\r")
 time.sleep(2)
 ser.write("AT\r")
 time.sleep(2)
 ser.write("AT\r") # envoie la commande AT
 time.sleep(3) # Laisse le temps au SIM800C de répondre

 rep = ser.read(ser.inWaiting()) # Regarde si la carte a répondu
 if rep != "":
    print "Response from the NadHAT board :"
    print rep
    if "OK" in rep:
        print "SIM800C stops"
    else :
        print "No communication with the NadHAT board"
        sys.exit(0)
 else :
    print "No response from the board"
    sys.exit(1)

 # Arrêter le SIM800C
 ser.write("AT+CPOWD=1\r")
 time.sleep(5)
 print "Check if the LED is OFF"
 return;
