Welcome to NadHat.
==================

### Introduction

NadHat is a GSM/GPRS modem extension hat for raspberry pi. It's pi zero hat format compatible (30x65mm). It uses the well known SIM800C module to offer a low cost M2M communication interface.

You'll find in this deposit [schematics], [datasheets and application notes], some [pieces of software] written in python and more in the future.

You can also follow nadhat google+ collection : https://plus.google.com/collection/o2lZRE

Have fun.

The garatronic team.

www.garatronic.fr


Don't want to read the manual, here a quickstart guide :

### Serial port setup

default setup for serial port /dev/ttyAMA0 is 115200,8,N,1


### Some usefull at command for SIM800C :
 - at _: answer OK is serial setup is OK_
 - atz _: reset default configuration_
 - ati _: display product indentification information_
 - at+cgmi _: display product manufacturer_
 - at+cgmm _: display model identification_
 - at+cpin? _: check if pin number is required_
 - at+cpin=xxxx _: enter pin code_
 - at+cbc _: battery voltage (around 67% or 3940mV)_
 - at&v _: display current configuration_
 - at+csq _: report quality of signal (first nb between 0-31, 2nd nb between 0-7, bigger is better)_
 - at+gsn _: request TA serial Number Identification (IMEI)_
 - at+cimi _: request international subscriber identity_
 - at+cops=? _: report list of present operators_
 - at+cspn? _: get service provider name from sim_
 - at+cadc? _: read adc input (0-2.8V range, pin 7 of CN2)_
 - at+cpowd=1 _: normal poweroff_

### Send an SMS :
 - at+cmgf=1 _: sms in text mode_
 - at+csca="+33695000695" _: service provider sms center number (french provider FREE for me)_
 - at+cmgs="+3363054xxxx" _: start SMS edition to "receiver number"_
   _prompt become '>'_
 - input your SMS + <CR>
 - send hexadecimal chars '0x1A,0x0D' (<SUB><CR> in fact) _: to send your SMS_

### Receive an SMS :
 - _answer the SMS you've received on your phone by NadHat._
 - _should receive 'CMTI:"SM",x' meaning you have receive a SMS in slot x_
 - at+cmgr=x _: read sms in slot 1_
 - at+cmgd=x _: delete sms to free slot x for next SMS_

[schematics]: https://github.com/garatronic/nadhat/tree/master/hardware
[datasheets and application notes]: https://github.com/garatronic/nadhat/tree/master/datasheet
[pieces of software]: https://github.com/garatronic/nadhat/tree/master/datasheet
