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

  sk = ecdsa.SigningKey.from_string(prkb, curve=ecdsa.SECP256k1)
  vk = sk.verifying_key
  pkb = b'\x04' + vk.to_string()
  pk = pkb.hex()

  salty = os.urandom(10)
  she = hashlib.sha256(pkb + salty).digest()
  b58 = base58.b58encode(she).decode()
  wallet = "X" + b58 + "TST"

  print("PRIVATE KEY: " + prk)
  print("PUBLIC KEY: " + pk)
  print("YOUR WALLET (TESTNET): " + wallet)

def priv():
  global pk, prk, wallet
  prkb = os.urandom(32)
  prk = prkb.hex()

  sk = ecdsa.SigningKey.from_string(prkb, curve=ecdsa.SECP256k1)
  vk = sk.verifying_key
  pkb = b'\x04' + vk.to_string()
  pk = pkb.hex()

  salty = os.urandom(10)
  she = hashlib.sha256(pkb + salty).digest()
  b58 = base58.b58encode(she).decode()
  wallet = "X" + b58 + "TSP"

  print("PRIVATE KEY: " + prk)
  print("PUBLIC KEY: " + pk)
  print("YOUR WALLET (PRIVATE): " + wallet)
  
