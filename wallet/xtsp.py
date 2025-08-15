from cryptography.hazmat.primitives.ciphers.aead import AESGCM as pNET
import os
import random
import sha3
import time
import ecdsa
import base58

private2key = ""
public2key = ""
walletp = ""

def pgen():
  global private2key, public2key
  private2byte = os.urandom(32)
  private2key = private2byte.hex()
  
  sk = private2byte.SigningKey.from_string(private2byte, curve=ecdsa.SECP256k1)
  vk = sk.verifying_key

  public2byte = vk.to_string()
  public2key = public2byte.hex()

  return private2byte

def pwalletgen():
  global walletp
  privatebytewallet = pgen()
  salt = os.urandom(10)
  times = round(time.time())
  timestamp = times.to_bytes(8, byteorder="big")
  keccak = sha3.keccak_256(privatebytewallet + salt + timestamp).digest()
  b58 = base58.b58encode(keccak).decode()
  walletp = "X" + b58 + "TSP"
  
  return walletp

def hex():
  timestamp = round(time.time()).to_bytes(8, byteorder="big")
  merkle = sha3.keccak_256(os.urandom(32)).digest()
  tostr = "X" + base58.b58encode(sha3.keccak_256(os.urandom(32)).digest()).decode() + "TSP"
  fromstr = "X" + base58.b58encode(sha3.keccak_256(os.urandom(32)).digest()).decode() + "TSP"
  to = tostr.to_bytes(16, byteorder="big")
  froms = fromstr.to_bytes(16, byteorder="big")
  nonce = sha3.keccak_256(os.urandom(32)).digest()
  target = sha3.keccak_256(os.urandom(32)).digest()
  difficulty = sha3.keccak_256(os.urandom(32)).digest()
  prevHash = sha3.keccak_256(os.urandom(32)).digest()
  hexHash = sha3.keccak_256(timestamp + merkle + to + froms + nonce + target + difficulty + prevHash).digest()
  return {
    "timestamp": timestamp,
    "merkleRoot": merkle,
    "to": to,
    "from": froms,
    "prevHash": prevHash,
    "nonce": nonce,
    "difficulty": difficulty,
    "target": target,
    "hexHash": hexHash
  }

def privatenet():
  encryptionk = pNET(public2key)
  nunce = os.urandom(12)
  hexdata = hex().to_bytes(32, byteorder="big")

  ctxt = encryptionk.encrypt(nunce, hexdata, None)
  return ctxt

print("YOUR PRIVATE KEY ON pnet: " + private2key)
print("YOUR PUBLIC KEY ON pnet: " + public2key)
print("YOUR pnet BURNER WALLET: " + walletp)
print("YOUR ENCRYPTED HEX DATA: " + privatenet())

