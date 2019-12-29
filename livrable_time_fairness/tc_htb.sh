#!/bin/bash 
tc class add dev wlp2s0 parent 1:1 classid 1:2 htb rate 7.50mbit ceil 15mbit 
tc filter add dev wlp2s0 parent 1:0 prio 1 protocol ip u32 match ip dst F0:7D:68:66:DE:C7 classid 1:2 
tc qdisc add dev wlp2s0 parent 1:2 handle 102: pfifo limit 1000 

