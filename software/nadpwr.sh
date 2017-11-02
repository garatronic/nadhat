#! /bin/bash
#
# A small script to pulse 1s on SIM800 powerkey to power-up it
# 

POWER_KEY_GPIO=26

gpio -g mode $POWER_KEY_GPIO out
gpio -g write $POWER_KEY_GPIO 1
echo pulse low PWRKEY pin  on GPIO$POWER_KEY_GPIO for 1s to startup SIM800...
sleep 1
gpio -g write $POWER_KEY_GPIO 0
echo end
