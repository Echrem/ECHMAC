#!/usr/bin/env python3
import subprocess
import argparse
import re
import random

print('''
      
 _____   ____  _   _  __  __     _      ____ 
| ____| / ___|| | | ||  \/  |   / \    / ___|
|  _|  | |    | |_| || |\/| |  / _ \  | |    
| |___ | |___ |  _  || |  | | / ___ \ | |___ 
|_____| \____||_| |_||_|  |_|/_/   \_\ \____|

''')

def parse_args():
    parser = argparse.ArgumentParser(description="MAC address management tool.")
    parser.add_argument("-i", "--interface", help="Specify the network interface to change the MAC address.")
    parser.add_argument("-m", "--mac", help="Specify a custom MAC address to set.")
    parser.add_argument("-cm", "--current_mac", action="store_true", help="Display the current MAC address.")
    parser.add_argument("-l", "--list", action="store_true", help="List all network interfaces.")
    return parser.parse_args()

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: f"{x:02x}", mac))

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address of {interface} to {new_mac}.")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
        mac_address_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result)
        if mac_address_result:
            return mac_address_result.group(0)
        else:
            print("[-] Could not read the MAC address.")
            return None
    except subprocess.CalledProcessError:
        print("[-] Failed to execute the ifconfig command.")
        return None

def list_interfaces():
    try:
        result = subprocess.check_output(["ip", "link", "show"]).decode('utf-8')
        print("[+] Network interfaces on the system:")
        print(result)
    except subprocess.CalledProcessError:
        print("[-] Could not list network interfaces.")

options = parse_args()

if options.list:
    list_interfaces()
elif options.current_mac:
    if not options.interface:
        print("[-] Please specify a network interface using the -i option.")
        exit(1)
    current_mac = get_current_mac(options.interface)
    if current_mac:
        print(f"[+] Current MAC address: {current_mac}")
    else:
        print("[-] Failed to retrieve the MAC address.")
else:
    if not options.interface:
        print("[-] Please specify a network interface using the -i option.")
        exit(1)

    new_mac = options.mac if options.mac else generate_random_mac()
    change_mac(options.interface, new_mac)

    current_mac = get_current_mac(options.interface)
    if current_mac:
        if current_mac == new_mac:
            print(f"[+] MAC address changed successfully to: {current_mac}")
        else:
            print(f"[-] MAC address change failed. Current MAC address: {current_mac}")
