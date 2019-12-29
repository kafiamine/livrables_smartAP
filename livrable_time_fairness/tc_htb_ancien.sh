#!/bin/bash 
tc qdisc add dev eno1 root handle 1: htb

tc class add dev eno1 parent 1: classid 1:1 htb rate 60mbit ceil 60mbit 

tc class add dev eno1 parent 1:1 classid 1:2 htb rate 30.00mbit ceil 60mbit
tc filter add dev eno1 parent 1:0 prio 1 protocol ip u32 match ip dst 10.42.0.57 classid 1:2 
tc qdisc add dev eno1 parent 1:2 handle 102: pfifo limit 1000 

tc class add dev eno1 parent 1:1 classid 1:3 htb rate 13.00mbit ceil 26mbit 
tc filter add dev eno1 parent 1:0 prio 1 protocol ip u32 match ip dst 10.42.0.240 classid 1:3 
tc qdisc add dev eno1 parent 1:3 handle 103: pfifo limit 1000 

