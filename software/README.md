NadHat pieces of softwares.
===========================

### Introduction

NadHat pieces of software are some utilities to send SMS and MMS.
Don't hesitate to enrich this software

Enjoy Developping !

www.garatronic.fr

### Dependencies

Before using theses python utilities, you sound install some dependencies

 - get update
 - sudo apt-get install git minicom python-dev python-setuptools python-serial python-pip
 - sudo pip install wiringpi
 - sudo apt-get install wiringp

### Use sms.py

 - python sms.py "+336xxxxxxxxx" "Le premier SMS V1.0" -o BOUYGUES -cp 0000
 - python sms.py "+336xxxxxxxxx" "Le premier SMS V1.0" -o ORANGE -cp 0000
 - python sms.py "+336xxxxxxxxx" "Le premier SMS V1.0" -o FREE -cp 1234

### Use mms.py

 - mms.py --title title.txt --text text.txt -o BOUYGUES --cpin 0000 --port  /dev/ttyAMA0 +336xxxxxxxxx image.jpg
 - mms.py --title title.txt --text text.txt -o ORANGE --cpin 0000 --port  /dev/ttyAMA0 +336xxxxxxxxx image.jpg
 - mms.py --title title.txt --text text.txt -o FREE --cpin 1234 --port  /dev/ttyAMA0 +336xxxxxxxxx image.jpg

NOTE : image.jpg should be under 200ko


