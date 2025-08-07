import sha3
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
  pkb = vk.to_string()
  pk = pkb.hex()

  salty = os.urandom(10)
  she = sha3.keccak_256(pkb + salty).digest()
  b58 = base58.b58encode(she).decode()
  wallet = "X" + b58 + "TST"
  
