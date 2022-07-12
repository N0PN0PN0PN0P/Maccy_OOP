# NETUTILS.PY
# SUPPORT NET OPERATIONS CLASS
import subprocess as sp
from utils import debby as d
from colors import Bcol as c
import random as rnd
import requests
import re

class NetOp:

    # THIS STATIC METHOD ENUMERATES AND RETRIEVES ALL THE MAC INTERFACES IN YOUR SYSTEM, IT DOESN'T RETRIEVE THE LOOPBACK (LO)
    @staticmethod
    def get_interfaces(debug):
        print(c.OKCYAN + '[+] These are the available interfaces in your system:'+ c.ENDC)
        availInterfaces = sp.check_output("ip link | awk -F: '$0 !~ \"lo|vir|^[^0-9]\"{print $2;getline}' 2>/dev/null ", shell=True)
        if debug == True:
            d.debby("Getting available interfaces: " + str(availInterfaces))
        availInterfaces = availInterfaces.decode("utf-8")
        if debug == True:
            d.debby("Decoding available interfaces: " + str(availInterfaces))
        netInterfaces = []
        for lan in availInterfaces.split("\n"):
            netInterfaces.append(lan.strip())
            if debug == True:
                d.debby("Append " + lan + " in the netInterfaces Array.")
        if debug == True:
            d.debby("Strip empty entries in netInterfaces array")
        netInterfaces = list(filter(str.strip, netInterfaces))
        i = 0
        for choice in netInterfaces:
            print(c.HEADER + "[+] " + str(i) + ") :  " + choice + c.ENDC)
            i += 1
        return netInterfaces

    @staticmethod
    def getMacaddress(sel_interface, debug):
        mac = sp.check_output(
            "ip link show " + sel_interface + " | grep link/ether | awk '{print $2}' 2>/dev/null ",
            shell=True).decode("utf-8").strip()
        if debug == True:
            d.debby(c.FAIL + "getMacaddress function : Previous MAC address " + mac + c.ENDC)
        return mac

    @staticmethod
    def getMacaddressRegex(selected_interface, debug):
        ifconfig_result = sp.check_output(["ifconfig", selected_interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
        if mac_address_search_result:
            if debug == True:
                d.debby(
                    c.FAIL + "getMacaddressRegex function : Previous MAC address " + mac_address_search_result.group(
                        0) + c.ENDC)
            return str(mac_address_search_result)
        else:
            print(c.WARNING + "[!] Can't find a valid MAC address for: " + selected_interface + c.ENDC)
            return 0

    @staticmethod
    def setMacaddress(mac_tochange, interface, previous_mac, debug):
        print(c.WARNING + "[+] Setting NEW MAC address..." + c.ENDC)
        if debug == True:
            d.debby("New Mac: " + mac_tochange + " - Interface: " + interface + " - Previous Mac: " + previous_mac)
        print(c.WARNING + "[+] Shutting OFF: " + c.FAIL + interface + c.ENDC + ".")
        sp.check_output(["ifconfig", interface, "down"])
        print(
            c.WARNING + "[+] Setting " + c.FAIL + interface + " MAC address to " + c.FAIL + mac_tochange + c.ENDC + ".")
        sp.check_output(["ifconfig", interface, "hw", "ether", mac_tochange])
        print(c.WARNING + "[+] Turnin ON: " + c.FAIL + interface + c.ENDC + ".\n")
        sp.check_output(["ifconfig", interface, "up"])

        check_mac = NetOp.getMacaddress(interface, debug)
        if check_mac != previous_mac:
            print(
                c.OKCYAN + "[!] " + interface + " MAC address successfully changed : Old MAC: " + previous_mac + " - New MAC: " + check_mac + "\n" + c.ENDC)
            return True
        else:
            print(c.FAIL + "[!] COULD NOT CHANGE THE MAC PLEASE REPORT TO GITHUB.\n")
            return False

    # THIS BLOCK DOES AN API REQUEST TO THE WEBSITE https://api.macaddress.io TO POST THE OUI MAC
    # AND RETRIEVE THE VENDOR ID
    # PLEASE REGISTER TO https://api.macaddress.io TO OBTAIN YOUR API QUERY KEY TO GET THE NAME OF THE MAC PRODUCER(OUI
    @staticmethod
    def getMacProducer(oui, apy_key, debug):
        macaddress_io_url_request = "https://api.macaddress.io/v1?apiKey=" + apy_key + "&output=vendor&search=" + oui
        response = requests.get(macaddress_io_url_request)
        if debug:
            d.debby(str(response.text))
        return response.text

    @staticmethod
    def createRandomMac(macs_in_file, hex_converter, apy_key, debug):
        rnd.seed()
        print(c.OKCYAN + "[+] Creating the REAL MAC address..." + c.ENDC)
        rnd_producer = rnd.sample(macs_in_file, 1)
        rnd_hex_num = rnd.sample(hex_converter, 6)
        temp_mac = (rnd_producer + rnd_hex_num)
        temp_mac = ''.join(temp_mac)
        final_mac = ':'.join(temp_mac[i:i + 2] for i in range(0, len(temp_mac), 2))
        print(c.OKGREEN + "[+] Getting name of the MAC address producer..." + c.ENDC)
        macProducer = NetOp.getMacProducer(str(final_mac),apy_key,debug)
        if debug == True:
            d.debby(str(macProducer) + " : " + str(final_mac))
        print(c.OKGREEN + "[+] MAC address producer: " + c.FAIL + macProducer + c.ENDC)
        return final_mac