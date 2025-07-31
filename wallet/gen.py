import hashlib
import os
import base58
import ecdsa

pk = ""
prk = ""
wallet = ""

def begin():
  global pk, prk, wallet
  prkb = os.urandom(32)
  prk = prkb.hex()
  # shi i forgot how this works, brb
  
