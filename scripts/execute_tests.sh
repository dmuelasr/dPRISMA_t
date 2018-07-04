
#!/bin/bash
rm -rf /var/log/openvswitch/*

echo_log () {

	echo "[ $1: $(date) ] - $2"

}

if [ $# -ne 3 ] ; then

	echo_log "ERROR" "$0 <Number of repetitions> <Output path> <Monitor resources: 1 (yes) | 0 (no)>"
	exit 1
fi

N_REP=$1
output_p=$2
mon_resources=$3

echo_log "INFO" "Preparing testbed for clean execution of tests"
./prepare_test.sh

echo_log "INFO" "Starting execution, $N_REP repetitions, saving output files into $output_p, monitor resources $mon_resources"

l=1; 
while [ $l -le $N_REP ]; do


	output_file=$output_p"/n"$l"/"

	mkdir -p $output_file/
	echo_log "INFO" "Executing repetition $l, saving output in $output_file"
	mn -c;

	service openvswitch-switch stop
	rm /etc/openvswitch/*
	ovs-appctl -t ovs-vswitchd exit
	ovs-appctl -t ovsdb-server exit
	ovs-dpctl del-dp system@ovs-system
	rmmod openvswitch
	service openvswitch-switch start

	if [ $mon_resources -eq 1 ] ; then
		taskset -c 5 ./cpu.sh > $output_file/cpu.txt &
		taskset -c 5 ./mem.sh > $output_file/mem.txt &
		taskset -c 5 ./monitorService.sh tcpdump > $output_file/activity.txt &
		sleep 5
	fi

	taskset -c 4 python test_jackson.py

	# Kill subprocesses
	echo_log "INFO" "Cleaning subprocesses..."
	mn -c;

	sleep 5
	killall -9 cpu.sh
	killall -9 mem.sh
	killall -9 monitorService.sh
	echo "3" > /proc/sys/vm/drop_caches 
	
	l=$((l+1))
done
