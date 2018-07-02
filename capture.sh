#!/bin/bash
killtree() {
    local _pid=$1
    local _sig=${2:--TERM}
    kill -stop ${_pid} # needed to stop quickly forking parent from producing children between child killing and parent killing
    for _child in $(ps -o pid --no-headers --ppid ${_pid}); do
        killtree ${_child} ${_sig}
    done
    kill -${_sig} ${_pid}
}
trap "{ killtree($$) ; wait ; exit 255; }" SIGINT
echo '' > log
for intf in "$@"
do
    output=traces/$intf".pcap"
    echo $output >> log
    tcpdump -i $intf -w $output -s 200 & >> log
done
wait
