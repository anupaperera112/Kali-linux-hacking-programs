#!/user/bin/env python
import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC address")
    parser.add_option("-m", "--mac", dest="newMac", help="new MAC address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] specify an interface")
    elif not options.newMac:
        parser.error("[-] specify a mac address")
    else:
        return options.interface, options.newMac

def change_mac(interface, newMac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])


def check_mac_change():
    interface, newMac = get_args()
    change_mac(interface, newMac)
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    found_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if(found_mac[0] == newMac):
        print("[+] changing MAC address for " + interface + " to " + newMac)
    else:
        print("mac address didnt change")


check_mac_change()

