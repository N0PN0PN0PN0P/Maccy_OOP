import os
import subprocess as sp
import optparse
import re
import requests
from bs4 import BeautifulSoup
# MY CLASSES
from colors import Bcol as c
from utils import Menu as m
from utils import debby as d
from netutils import NetOp as Netop
from sysutils import SysUtils as Sysut
###############################################################
program_name = "Maccy"
version = "1.1"
explanation = "Over Powered MAC address changer by N0PN0PN0P"
mail = "N0PN0PN0P@proton.me"
github = "https://github.com/N0PN0PN0PN0P/maccy"
quote = "'I don't like PARSERS'"
extra_info = "With my api key you can do only 100 free queries per day, \nso please sign in to https://macaddress.io " \
             "to get your free api key "
cpright = "2022 N0PN0PN0P"
licence = "Free"

# GLOBAL VARS
api_key_macaddress_io = "at_1lsy9vcEFSDX4z8pCBMFRFKxJND3z"
macs_in_file = []
hex_converter = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
cwd = os.getcwd()
macs_file_name = "mac_addresses.txt"
parser = optparse.OptionParser()
parser.add_option("-d", "--debug", action="store_true", help="Enter in debug mode")
(options, arguments) = parser.parse_args()
debug = options.debug

# THIS BLOCK INITIALIZE THE PROGRAM, AT FIRST RUN CHECKS IF THE FILE CONTAINING THE MAC ADDRESSES EXIST,
# IF IT DOES THE PROGRAM LOADS THE 20000 OUI MAC ADDRESSES IN THE MAC'S LIST TO BE USED LATER.
# IF THE FILE DOESN'T EXIST IT USES BEAUTYFUL SOUP TO SCRAPE 25 PAGES ON https://www.netlookup.se/mac/vendors/
# AND GETS ABOUT 20000 MAC'S OUI AND SAVE IN THE FILE AND IN THE MAC'S LIST TO BE USED LATER ON
def initialize():
    pagecount = 1
    totalpages = 25
    if debug == True:
        d.debby(cwd)
    try:
        if debug == True:
            d.debby("Open file that contains prescraped real MACs")
        print(c.WARNING + "[+] Opening file to import REAL MAC addresses." + c.ENDC)
        f = open(cwd + "/" + macs_file_name, "r")
        print(c.WARNING + "[+] Populating the array with REAL MAC addresses." + c.ENDC)
        for macs in f:
            # if debug == True:
            #   debby(macs)
            macs_in_file.append(macs.strip("\n"))
            # if debug == True:
            #   print(macs_in_file)
    except FileNotFoundError as e:
        try:
            f = open(cwd + "/" + macs_file_name, "w")
            if debug == True:
                d.debby(e)
            print(c.FAIL + "[!] Can't Open the file mac_addresses.txt, file doesn't exist!" + c.ENDC)
            # CREATE THE FILE TO HOLD THE SCRAPER MAC ADDRESSES
            print(c.OKCYAN + "[+] Start Scraping the website for REAL MAC addresses." + c.ENDC)
            print(c.WARNING + "[+] Total pages to scrape: " + str(totalpages) + c.ENDC)

            while pagecount < totalpages + 1:
                print(c.WARNING + "[+] Scraping page: " + str(pagecount) + c.ENDC)
                URL = "https://www.netlookup.se/mac/vendors/?page=" + str(pagecount)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                producersMacs = soup.find_all("td", class_="d-none d-lg-block")
                for producerMac in producersMacs:
                    if debug == True:
                        print(producerMac.getText(separator="\n", strip=True))
                    temp_str = str(producerMac.getText(separator="\n", strip=True))
                    if debug == True:
                        d.debby("Len of items: " + str(len(temp_str)))
                    if len(temp_str) < 7:
                        f.write(temp_str + "\n")
                        macs_in_file.append(temp_str)
                pagecount += 1
            print(c.OKCYAN + "[+] Total REAL MAC addresses added: " + str(len(macs_in_file)) + c.ENDC)
            f.close()
            if debug == True:
                print(macs_in_file)
        except Exception as e:
            print(e)


def show_menu():
    # Menu Build
    sp.call("clear", shell=True)
    m.asterix()
    print("███    ███  █████   ██████  ██████ ██    ██")
    print("████  ████ ██   ██ ██      ██       ██  ██")
    print("██ ████ ██ ███████ ██      ██        ████")
    print("██  ██  ██ ██   ██ ██      ██         ██")
    print("██      ██ ██   ██  ██████  ██████    ██")
    m.asterix()
    print(c.HEADER)
    m.info(program_name, version, explanation, mail, github, quote, extra_info, cpright, licence)
    print(c.ENDC)
    m.asterix()


def change_MAC(choice):
    if choice == 1:
        # USING REGEX TO VALIDATE THE USER MAC INPUT
        mac_to = ""
        print((c.OKCYAN + "[!] Please remember to use hex notation, every 2 chars add a :(colon)" + c.ENDC))
        print((c.OKGREEN + "[+] Valid entries are: " + c.FAIL + ','.join(hex_converter) + c.ENDC))
        while not re.match(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_to):
            mac_to = input(c.WARNING + "[!] Please input a valid MAC address: > " + c.ENDC)
        Netop.setMacaddress(mac_to, selected_interface, previous_mac_address, debug)

    if choice == 2:
        #createRandomMac(macs_in_file, hex_converter, debug):
        realMac = Netop.createRandomMac(macs_in_file, hex_converter, api_key_macaddress_io, debug)
        print(c.OKGREEN + "[+] This will be your new MAC address: " + c.FAIL + realMac + c.ENDC)
        keep_mac = "N"
        while keep_mac != "Y" and keep_mac != "G":
            keep_mac = input(c.OKCYAN + "[?] Are you " + c.FAIL +
                             "Ok" + c.OKCYAN + " with this or you want to " +
                             c.FAIL + "Generate " + c.OKCYAN + "a new one? (" + c.FAIL + "Y" +
                             c.OKCYAN + "/" + c.FAIL + "G" + c.OKCYAN + ") " + c.ENDC).upper()
        if keep_mac == "Y":
            Netop.setMacaddress(realMac, selected_interface, previous_mac_address, debug)
        else:
            change_MAC(2)
    if choice == 3:
        return


# PROGRAM START
if debug == True:
    d.debby("Parser Options: " + str(parser.parse_args()))

show_menu()
initialize()
isRoot = Sysut.check_root_privs(debug)
if not isRoot:
    print(c.FAIL + "[!] You are not running the program as sudoer (root), please type: sudo maccy.py" + c.ENDC)
    exit(0)
print(c.WARNING + "[+] " + "You have root permissions moving on..." + c.ENDC)
netInterfaces = Netop.get_interfaces(debug)
adapterch = 10000000
# LOOP TO LET THE USER INPUT THE INTERFACE TO CHANGE THE MAC
while adapterch > len(netInterfaces) - 1 or adapterch < 0:
    try:
        adapterch = int(input(
            c.WARNING + "[?] Please type the number of the interface you want to change the MAC address: > " + c.ENDC))
        if adapterch > len(netInterfaces) - 1 or adapterch < 0:
            print(c.FAIL + "[!] Please input the correct interface number!" + c.ENDC)
    except ValueError:
        print(c.FAIL + "[!] Please input a number!" + c.ENDC)
print("\r")
m.asterix()
print(c.FAIL + "\n[!]" + c.OKGREEN + " You selected interface " + c.FAIL + netInterfaces[
    adapterch] + c.ENDC + ", current MAC address: " +
      c.FAIL + sp.check_output(
    "ip link show " + netInterfaces[adapterch] + " | grep link/ether | awk '{print $2}' 2>/dev/null ",
    shell=True).decode("utf-8").strip() +
      c.ENDC)
# ASSIGNING RETRIEVED VALUES
selected_interface = str(netInterfaces[adapterch])
previous_mac_address = str(Netop.getMacaddress(selected_interface, debug))
# previous_mac_address_regex = str(Netop.getMacaddressRegex(selected_interface),debug)
print("\r")
m.asterix()
print(c.WARNING + "\n[+] Choose an option: " + c.ENDC)
print("[+] 1) Input a MAC address.")
print("[+] 2) Impersonate a real device ( use real MAC addresses from real producers ).")
print("[+] 3) Exit program.")
macchoice = 5
while macchoice > 3 or macchoice < 1:
    try:
        macchoice = int(input(c.WARNING + "[?] Please input your choice number: > " + c.ENDC))
        if macchoice > 3 or macchoice < 1:
            print(c.FAIL + "[!] Please input a number included between 1 and 3!" + c.ENDC)
    except ValueError:
        print(c.FAIL + "[!] Please input a number!" + c.ENDC)

change_MAC(int(macchoice))
m.asterix()
m.thank_you(program_name, mail)
m.asterix()
exit(1)
