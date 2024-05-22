#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0      run this to store packets in a queue
# pip install netfilterqueue
# after flush the iptables :- iptables --flush
import netfilterqueue
import subprocess


def process_packet(packet):
    print(packet)
    packet.drop()


subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0")

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()

subprocess.call("iptables --flush")
