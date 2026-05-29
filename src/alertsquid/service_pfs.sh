#!/usr/local/bin/bash
clear

# ===============================================
# VARIABLES
# ===============================================

work_dir=$(dirname "$0")
script_py="$work_dir/alertsquid.py"
pid_file="$work_dir/alertsquid.pid"

# ===============================================
# RUN
# ===============================================

# Check if exist 'pid_file'
if [ -f "$pid_file" ]; then
    code="$(cat "$pid_file")"
#    code="$(ps -q "$code" > /dev/null 2>&1; echo $?)"
    code="$(ps -p "$code" > /dev/null 2>&1; echo $?)"
    
	# If 'alertsquid.py' is not running
    if [[ $code -gt 0 ]]; then
        rm -f "$pid_file"
        /usr/local/bin/phyton3.11 "$script_py" > /dev/null 2>&1 &
        echo "Service 'alertsquid.py' is starting"
        exit
    else
		echo -e "Service 'alertsquid.py' is running"
		echo -e "PID: $(cat "$pid_file")"
		echo -e "Run: 'kill -9 $(cat "$pid_file")' to stopping"
        exit
    fi
else
    /usr/local/bin/python3.11 "$script_py" > /dev/null 2>&1 &
	echo -e "Service 'alertsquid.py' is running"
	echo -e "PID: $(cat "$pid_file")"
	echo -e "Run: 'kill -9 $(cat "$pid_file")' to stopping"
fi

exit 0