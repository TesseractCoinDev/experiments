import gen
from cryptography.fernet import Fernet
import time
import hashlib
import random

gen.priv()

def trans(): # not that kinda trans >o<
  timestamp = str(time.time())
  froma = gen.wallet
  to = gen.wallet2
  amount = str(random.randint(1, 100)) + "XTS"
  feepre = len(timestamp) + len(froma) + len(to) + len(amount)
  feepost = (feepre + len(feepre)) * float(0.00001)
  fee = str(float(feepost)).encode() + "XTS"
  txid = hashlib.sha256(timestamp + froma + to + amount + fee).digest()

# tx done for now, debugging and additions later
