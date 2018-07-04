#!/bin/bash

service irqbalance stop
service postgresql stop
service apache2 stop
service docker stop
ipsec stop

echo 03f > /sys/devices/virtual/workqueue/cpumask

