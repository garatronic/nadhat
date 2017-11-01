# -*- coding: utf-8 -*-
#
# sms.py
# Script to send a SMS
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

##############Begin process command line ###########
parser = argparse.ArgumentParser(description='Configure and send your sms. command line could be: python sms.py "+336XXXXXXXX" "my text" -o ORANGE -cp 0000 -p "/dev/ttyAMA0"')

parser.add_argument('RN', type=str, help='Receiver number. ex: "+336XXXXXXXX"')

parser.add_argument('sms', type=str, help='Message. ex: "my text"')

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

args = parser.parse_args()
operator_sms = operator_sms_dict[args.operator]
receiver_nb = args.RN
serial_port = args.port
code_pin = args.cpin
text_sms = args.sms

print "operator_sms="+args.operator+", receiver_nb="+receiver_nb+", serial_port="+serial_port+", code_pin="+code_pin+", sms="+text_sms
#print operator_sms
##############End process command line ###########

# Wait for the nadhat answer
def wait_Answer(code):
    time.sleep(3)
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

# Start the SIM800C
nadhat_pwr_on.pwr_on()
time.sleep(5)

# Check the communication with the nadhat board
ser.write("AT\r") # Send AT command
print "AT\r"
wait_Answer("OK")

# Send the pin code
ser.write("AT+CPIN="+code_pin+"\r")
print "AT+CPIN="+code_pin+"\r"
print "Code PIN sent... wait 10 secondes."
time.sleep(5)
print "Wait for 5 more seconds..."
time.sleep(5)
print "Check the slow blinking LED rate..."
wait_Answer("OK")

# Send text mode
ser.write("AT+CMGF=1\r")
print "AT+CMGF=1\r"
wait_Answer("OK")

# Send the operator number
ser.write('AT+CSCA="'+operator_sms+'"\r')
print 'AT+CSCA="'+operator_sms+'"\r'
wait_Answer("OK")

# Send recipient number
ser.write('AT+CMGS="'+receiver_nb+'"\r')
rep = ser.read(ser.inWaiting())
print rep
time.sleep(3)

# Send the SMS
ser.write(text_sms+chr(26))
rep = ser.read(ser.inWaiting())
print rep

time.sleep(3)
rep = ser.read(ser.inWaiting())
print rep

# Stop the SIM800C
nadhat_pwr_off.pwr_off()
