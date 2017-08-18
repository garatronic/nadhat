
# -*- coding: utf-8 -*-
#
#           nadhat_pw_on.py
# Programme destiné à mettre en service le SIM800C
# de la carte NadHAT en envoyant un pulse de 1 seconde
# sur la patte PWRKEY du circuit
#

import wiringpi
import time

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
