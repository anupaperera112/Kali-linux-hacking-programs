#!/usr/bin/env python
import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answered_list= scapy.srp(arp_request_broadcast, timeout = 1)[0] #use srp because the custom ether
    for element in answered_list:
        print(element[1].psrc)
        print(element[1].hwsrc)
    # print(answered_list.summary())


    # arp_request_broadcast.show()
    # print(arp_request_broadcast.summary())
    # print(broadcast.summary())
    # scapy.ls(scapy.Ether())

scan("192.168.175.2/24")
