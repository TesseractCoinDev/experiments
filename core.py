import time
from wallet import gen

def menu():
  print("MENU")
  print("---")
  print("[GEN] - Wallet Generation Test")
  time.sleep(1)
  choose = input(">> ")
  if choose.upper() == "[GEN]":
    gen.begin()
  else:
    print("ERR - FUNCTION DOSENT EXIST")
    time.sleep(1)
    menu()
    
menu()
