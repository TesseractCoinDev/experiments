# import cryptography
import os
# import random
import sha3
import time
import ecdsa
import base58

private2key = ""
public2key = ""
walletp = ""

def pgen():
  private2byte = os.urandom(32)
  private2key = private2byte.hex()
  
  sk = private2byte.SigningKey.to_string(private2byte, curve=ecdsa.SECP256k1)
  vk = sk.verifying_key

  public2byte = vk.to_string()
  public2key = public2byte.hex()

  return private2byte

def pwalletgen():
  privatebytewallet = pgen()
  salt = os.urandom(10)
  times = round(time.time())
  timestamp = times.to_bytes(8, byteorder="big")
  keccak = sha3.keccak_256(privatebytewallet + salt + timestamp).digest()
  b58 = base58.b58encode(keccak).decode()
  walletp = "X" + b58 + "TSP"
  
  return walletp



