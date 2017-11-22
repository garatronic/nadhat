#! /bin/bash
#
# A small script to pulse 1s on SIM800 powerkey to power-up it
# 

POWER_KEY_GPIO=26
NADHAT_PWR=0

# Just check if NadHAT is not already powered
gpio mode 15 in
NADHAT_PWR=`gpio read 15`
gpio mode 15 alt0

if [ $NADHAT_PWR -eq 0 ]; then
	gpio -g mode $POWER_KEY_GPIO out
	gpio -g write $POWER_KEY_GPIO 1
	echo pulse low PWRKEY pin on GPIO$POWER_KEY_GPIO for 1s to startup SIM800...
	sleep 1
	gpio -g write $POWER_KEY_GPIO 0
else
	echo SIM800C is already powered.
fi
echo end
