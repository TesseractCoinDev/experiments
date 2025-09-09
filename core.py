from mining import genesis_no_progpow
from termcolor import colored
from hex import genesis
from wallet import xtsp
from wallet import gen

def menu():
  print(colored("MENU", "blue", attrs=["bold"]))
  print(colored("---", "white", attrs=["bold"]))
  print(colored("[GEN] - Mainnet Wallet Generation Test", "green", attrs=["bold"]))
  print(colored("[XTSP] - pnet Wallet & Transaction Test", "green", attrs=["bold"]))
  print(colored("---", "white", attrs=["bold"]))
  print(colored("[GMN] - Genesis Mining (No ProgPoW)", "red", attrs=["bold"]))
  print(colored("---", "white", attrs=["bold"]))
  print(colored("[GENESIS] - Genesis Hex Generation", "yellow", attrs=["bold"]))
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
  elif choose.upper() == "[GMN]":
    genesis_no_progpow.mine()
    time.sleep(1)
    menu()
  elif choose.upper() == "[GENESIS]":
    genesis.display()
    time.sleep(1)
    menu()
  else:
    print("ERR - FUNCTION DOSENT EXIST")
    time.sleep(1)
    menu()
    
menu()
