#!/bin/bash

#while [ 1 -eq 1 ] ; do vmstat 1 2 | awk -v ts=$(date +%s) '(NR == 4){print ts"\t"$0}'; done;

while [ 1 -eq 1 ] ; do

./cputest.sh 0.5;
#mpstat 1 2 -P ALL -u | awk 'BEGIN{print_f=1}{if (print_f) print $0; if (length($0)<5) {if (print_f) print_f=0; else print_f=1}; }' | grep "," | sed "s/,/./g" | awk -v ts=$(date +%s) '{print ts"\t"$0}'; 

done;

