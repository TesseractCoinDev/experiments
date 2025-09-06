from termcolor import colored
from mining import linear
from wallet import xtsp
from wallet import gen

def menu():
  print(colored("MENU", "blue", attrs=["bold"]))
  print(colored("---", "white", attrs=["bold"]))
  print(colored("[GEN] - Mainnet Wallet Generation Test", "green", attrs=["bold"]))
  print(colored("[XTSP] - pnet Wallet & Transaction Test", "green", attrs=["bold"]))
  print(colored("---", "white", attrs=["bold"]))
  print(colored("[LM] - Linear Mining Test", "red", attrs=["bold"]))
  time.sleep(1)
  choose = input(">> ")
  if choose.upper() == "[GEN]":
    gen.display()
    time.sleep(1)
    menu()
  elif choose.upper() == "[XTSP]":
    xtsp.display()
    time.sleep(1)
    menu()
  elif choose.upper() == "[LM]":
    linear.display()
    time.sleep(1)
    menu()
  else:
    print("ERR - FUNCTION DOSENT EXIST")
    time.sleep(1)
    menu()
    
menu()
