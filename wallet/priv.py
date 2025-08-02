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
  feepost = (feepre + len(str(feepre))) * float(0.00001)
  fee = str(feepost) + "XTS"
  txe = timestamp + froma + to + amount + fee
  txh = hashlib.sha256(txe.encode()).digest()
  txid = hashlib.sha256(txe.encode()).hexdigest()
  sig = gen.sk.sign(txh).hex()
  return {
    "timestamp": timestamp,
    "to": to,
    "from": froma,
    "amount": amount,
    "fee": fee,
    "signature": sig,
    "txid": txid
  }

def private():
  
