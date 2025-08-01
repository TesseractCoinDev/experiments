import time
from wallet import gen
from wallet import priv

def menu():
  print("MENU")
  print("---")
  print("[GEN] - Wallet Generation Test")
  print("[XTSP] - Private Transaction Test")
  time.sleep(1)
  choose = input(">> ")
  if choose.upper() == "[GEN]":
    gen.begin()
    time.sleep(1)
    menu()
  elif choose.upper() == "[XTSP]":
    priv.display()
    time.sleep(1)
    menu()
  else:
    print("ERR - FUNCTION DOSENT EXIST")
    time.sleep(1)
    menu()
    
menu()
