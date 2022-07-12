# UTILS.PY
# SUPPORT CLASS FOR EVERY PROGRAM
# CLASS TO IMPLEMENT COLORING LINES IN TERMINAL
from colors import Bcol as c


class debby:
    @staticmethod
    def debby(debug_string):
        print(c.FAIL + "\n[Debug]: " + str(debug_string) + c.ENDC)

class Menu:


    @staticmethod
    def info(program_name, version, explanation, mail, github, quote, extra_info, copyright, licence):

        print(f"Welcome in {program_name} - V.{version}.")
        print(explanation)
        print(f"You can contact me at {mail}.")
        print(f"Source repository: {github}.")
        print(f"Favourite quote: {quote}.")
        if extra_info is not None:
            print(extra_info)
        print(f"Copyright: {copyright}.")
        print(f"Licence: {licence}")

    @staticmethod
    def asterix():
        print(c.OKCYAN + "*" * 100 + c.ENDC)

    @staticmethod
    def thank_you(program_name, mail):
        print("\r")
        print(c.OKCYAN + "[*] THANK YOU FOR USING " + program_name + " ;) : " + c.ENDC)
        print(c.OKCYAN + f"[*] please send any comments to {mail} ;) : " + c.ENDC)
        print("\r")

