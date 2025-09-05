from sha3 import keccak_256
import random
import os

coefficient = 65535
exponent = 29
target = coefficient * 2**8*(exponent - 3)

def hex():
  version = "1.0.0"
  prevHashes = [sha3.keccak_256(os.urandom(2)).hexdigest(), sha3.keccak_256(os.urandom(2)).hexdigest(), sha3.keccak_256(os.urandom(2)).hexdigest(), sha3.keccak_256(os.urandom(2)).hexdigest(), sha3.keccak_256(os.urandom(2)).hexdigest(), sha3.keccak_256(os.urandom(2)).hexdigest()]
  merkle = sha3.keccak_256(os.urandom(2)).hexdigest()
  timestamp = str(time.time())
  tar = target
  nonce = random.getrandbits(32)
  s = version.encode("utf-8") + prevHashes.encode("utf-8") + merkle.encode("utf-8") + timestamp.encode("utf-8")
  sf = s + tar.to_bytes(32, "big") + nonce.to_bytes(4, "big")
  hexHash = sha3.keccak_256(sf).hexdigest()
  hexHeader = [{"verison": version, "prevHashes": prevHashes, "merkleRoot": merkle, "timestamp": timestamp, "target": str(tar), "nonce": str(nonce), "hexHash": hexHash}]
  print("Mining - Current Hash:" + hexHash)
  
  if int(hexHash, 16) <= target:
    print("Mined")
  else:
    hex()

while True:
  hex()
  
  
