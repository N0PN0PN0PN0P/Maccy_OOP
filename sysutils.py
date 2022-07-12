import subprocess as sp
from utils import debby as d
from colors import Bcol as c

class SysUtils:

    @staticmethod
    def check_root_privs(debug):
        print("[+] Remember to run the program as sudo: change the MAC address require sudoers privileges")
        print("[+] Checking if you have root permissions...")
        isRoot = sp.check_output("id -u", shell=True)
        if debug == True:
            d.debby("Checking Uid: " + str(isRoot))
        isRoot = isRoot.decode("utf-8").strip()
        if debug == True:
            d.debby("Decoding Utf-8 the Uid: " + str(isRoot))
        if isRoot != "0":
            return False
        else:
            return True