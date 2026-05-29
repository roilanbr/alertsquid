#!/usr/bin/bash

red="\033[91m"; green="\033[92m"; yellow="\033[93m"; blue="\033[94m"; nc="\033[0m"
export coloransi="$red $green $yellow $blue $nc"

name="alertsquid"
pidfile="./var/run/alertsquid.pid"

rc_start () {
	if [ -f ${pidfile} ]; then
		echo -e "${name} is ${green}running${nc} PID ${green}$(cat ${pidfile})${nc}"
	else
		python ./${name}.py > dev/null 2>&1 & echo $! > ${pidfile}
		echo -e "${green}●${nc} ${name} is ${green}running${nc} PID ${green}$(cat ${pidfile})${nc}"
	fi
}

rc_stop () {
	if [ -f ${pidfile} ]; then
		kill -9 "$(cat ${pidfile})"
		rm ${pidfile} 2>&1 /dev/null
	elif [ ! -f ${pidfile} ]; then
		echo -e "○ ${name} is ${red}dead${nc}"
	fi
}

rc_status () {
	if [ ! -f ${pidfile} ]; then
		echo -e "○ ${name} is ${red}dead${nc}"
	else
		echo -e "${green}●${nc} ${name} is ${green}running${nc} PID ${green}$(cat ${pidfile})${nc}"
	fi
}

case "$1" in

	start)
		rc_"$1"
		;;
	stop)
		rc_"$1"
		;;
	restart)
		rc_stop
		rc_start
		;;
	status)
		rc_status
		;;
	*)
		echo "Uso: /usr/local/etc/rc.d/${name} {start|stop|restart}"
		echo "Uso: /etc/init.d/${name} {start|stop|restart}"
		echo "Uso: service ${name} {start|stop|restart}"
		exit 1
		;;

esac
exit 0