#!/bin/bash 



tc filter add dev eno1 parent 1:0 prio 1 protocol ip u32 match ip dst 10.42.0.240 classid 1:3 





INGRESS:
tc filter add dev eth1 parent 1: protocol ip prio 5 u32 match u16 0x0800 0xffff at -2 match u16 0x4455 0xffff at -4 match u32 0x00112233
0xffffffff at -8 flowid 1:40

EGRESS:
tc filter add dev eth1 parent 1: protocol ip prio 5 u32 match u16 0x0800 0xffff at -2 match u32 0x22334455 0xffffffff at -12 match u16 0x0011
0xffff at -14 flowid 1:40





u32 match ip dst 10.42.0.240

INGRESS:   u32 match u16 0x0800 0xffff at -2 match u16 0x4455 0xffff at -4 match u32 0x00112233 0xffffffff at -8

EGRESS:    u32 match u16 0x0800 0xffff at -2 match u32 0x22334455 0xffffffff at -12 match u16 0x0011 0xffff at -14




Egress (match Dst MAC): ... match u16 0xPPPP 0xFFFF at -2 match u32 0xM2M3M4M5 0xFFFFFFFF at -12 match u16 0xM0M1 0xFFFF at -14




Decimal Offset  Description
-14:    DST MAC, 6 bytes
-8:     SRC MAC, 6 bytes
-2:     Eth PROTO, 2 bytes, eg. ETH_P_IP
0:      Protocol header (IP Header)

Where PPPP is the Eth Proto Code (from linux/include/linux/if_ether.h):
ETH_P_IP= IP = match u16 0x0800
Where your MAC = M0M1M2M3M4M5




