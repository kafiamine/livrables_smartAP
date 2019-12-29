#!/bin/bash 
tc qdisc add dev wlp2s0 root handle 1: htb 
tc class add dev wlp2s0 parent 1: classid 1:1 htb rate 150mbit ceil 150mbit 

tc class add dev wlp2s0 parent 1:1 classid 1:2 htb rate 48.00mbit ceil 48.00mbit 
tc filter add dev wlp2s0 parent 1:0 prio 1 protocol ip u32 match u16 0x0800 0xffff at -2 match u32 0x14f0dc14 0xffffffff at -12 match u16 0x6c88 0xffff at -14 classid 1:2 
tc qdisc add dev wlp2s0 parent 1:2 handle 102: pfifo limit 1000 

tc class add dev wlp2s0 parent 1:1 classid 1:3 htb rate 16.67mbit ceil 16.67mbit 
tc filter add dev wlp2s0 parent 1:0 prio 1 protocol ip u32 match u16 0x0800 0xffff at -2 match u32 0x14f0dc15 0xffffffff at -12 match u16 0x6c88 0xffff at -14 classid 1:3 
tc qdisc add dev wlp2s0 parent 1:3 handle 103: pfifo limit 1000 

tc class add dev wlp2s0 parent 1:1 classid 1:4 htb rate 8.33mbit ceil 8.33mbit 
tc filter add dev wlp2s0 parent 1:0 prio 1 protocol ip u32 match u16 0x0800 0xffff at -2 match u32 0x14f0dc13 0xffffffff at -12 match u16 0x6c88 0xffff at -14 classid 1:4 
tc qdisc add dev wlp2s0 parent 1:4 handle 104: pfifo limit 1000 

