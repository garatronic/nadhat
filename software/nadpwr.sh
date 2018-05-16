#! /bin/bash
#
# A small script to power-[up|down] NadHAT SIM800C module
# 
# Author : fpierson@garatronic.fr
#
# ver	date 		modification
# 1.0	2017-11-27	First release
# 1.1	2017-12-02	DisplayUsage if ./nadhat.sh script is invoqued w/o argument
# 1.2   2018-05-02	Sensing RXD rather TXD pin

VERSION="1.2"
DATE_VERSION="2018-05-02"

# NB samples on BCM RXD input to check if SIM800 is up
NB_SAMPLES=3

# BCM GPIO driving SIM800 power switch button
POWER_KEY_GPIO=26

# NAD_PWR status, updated after invoquing CheckPwr()
NAD_PWR="unknow"

# NAD_REQ action requested by USER PWR status, updated after invoquing CheckPwr()
NAD_REQ="none"

# Quiet flag, requested on cmdline
QUIET="none"


function DisplayVersion()
{
	echo "$0 version $VERSION [$DATE_VERSION]"
}

function DisplayUsage()
{
	echo "usage: nadpwr [-q] [-v] [-h] [on|off|install] "
	echo " nadpwr on, nadpwr off, ./nadpwr.sh install" 
	echo "       [-q] quiet mode"
	echo "       [-v] display version of software and exit"
	echo "       [-h] display this help and exit"
	exit 0
}

function CheckPwr()
{
	NAD_PWR="unknow"
	# Just check if NadHAT is not already powered by sensing RXD
	for (( i=NB_SAMPLES; i>=1; i-- ))
	do
		if [ `gpio read 16` -eq 1 ]; then
			NAD_PWR="on"
		fi
	done
	if [ $NAD_PWR != "on" ]; then 
		NAD_PWR=off
	fi
}


function Pulse()
{
	gpio -g mode $POWER_KEY_GPIO out
	gpio -g write $POWER_KEY_GPIO 1
	if [ $QUIET = "none" ]; then
		echo "Pulse 1s on GPIO$POWER_KEY_GPIO to power $NAD_REQ SIM800C."
	fi
	sleep 1
	gpio -g mode $POWER_KEY_GPIO in
}

function Install()
{
	INSTALL="none"

	command -v gpio >/dev/null 2>&1 || {
		INSTALL="wiringpi"
		echo "gpio seens not to be installed, do you want to install it ?"
		PS3='> '   # le prompt
		LISTE=("[y]es" "[n]o")  # liste de choix disponibles
		select CHOIX in "${LISTE[@]}" ; 
		do
			case $REPLY in
				1|y)
				INST_WPI=`sudo apt-get install wiringpi`
				;;
				2|n)
				echo "you should install it by typing : sudo apt-get install wiringpi"
				echo "can't continue without wiringpi..."
				exit 1
				break
				;;
			esac
		done
	}

	command -v nadpwr >/dev/null 2>&1 || {
		INSTALL="nadpwr"
		echo "nadpwr utility does not seens to be installed, do you want to install it ?"
		PS3='> '   # le prompt
		LISTE=("[y]es" "[n]o")  # liste de choix disponibles
		select CHOIX in "${LISTE[@]}" ; 
		do
			case $REPLY in
				1|y)
				dest="/usr/local/sbin/"
				shortname="nadpwr"
				sudo cp $0 $dest$shortname
				echo $shortname has been copied in $dest
				break
				;;
				2|n)
				echo ok. next time maybe
				break
				;;
			esac
		done
	}
	if [ $INSTALL = "none" ]; then
		echo "$0 $1: nothing to install."
	fi
	exit 0
}

if [ $# = 0 ]; then
	if echo "$0" | grep '\.sh$' >/dev/null 2>&1; then 
		echo "$0 has been upgraded : version $VERSION [$DATE_VERSION]"
		DisplayUsage
		exit 0
	fi
fi

for param in "$@"
do
	case $param in
		on) NAD_REQ="on"
			;;
       	off) NAD_REQ="off"
			;;
       	install) Install
			;;
	esac
done

optstring="qhv"

while getopts $optstring opt 
do
	case $opt in
		'q')	QUIET="active"
				break
           		;;
		'v')	DisplayVersion
				exit 0
           		;;
		'h')	DisplayUsage
				exit 0
				;;
	esac
done

shift $(($OPTIND-1))

CheckPwr
#echo "NAD_REQ=$NAD_REQ, NAD_PWR=$NAD_PWR"

if [ $NAD_REQ = $NAD_PWR ]; then
	if [ $QUIET = "none" ]; then 
		echo "NadHAT board is already $NAD_PWR." 
	fi
	exit 0
elif [ $NAD_REQ = "none" ]; then
	if [ $QUIET = "none" ]; then 
		echo "NadHAT board is $NAD_PWR."
	fi
	exit 0
else
	Pulse
	sleep 1
	CheckPwr
	#echo "NAD_REQ=$NAD_REQ, NAD_PWR=$NAD_PWR"
	if [ $NAD_REQ != $NAD_PWR ]; then
		if [ $QUIET = "none" ]; then 
			echo "NadHAT power $NAD_REQ have failed."
		fi
		exit 1
	elif [ $QUIET = "none" ]; then 
		echo "NadHAT is now $NAD_REQ."
	fi
fi
