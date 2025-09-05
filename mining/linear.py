from eth_utils import keccak
import random
import time
import os

coefficient = random.randint(65535, 70000)
exponent = random.randint(1, 32)
target = coefficient * 2**(8*(exponent - 3))

while True:
  version = "1.0.0"
  prevHashes = [keccak(os.urandom(2)).hex() for _ in range(6)]
  merkle = keccak(os.urandom(2)).hex()
  timestamp = str(time.time())
  tar = target
  nonce = random.getrandbits(128)
  s = (version.encode() + "".join(prevHashes).encode() + merkle.encode() + timestamp.encode())
  sf = s + tar.to_bytes(32, "big") + nonce.to_bytes(12, "big")
  hexHash = keccak(sf).hex()
  hexHeader = [{"verison": version, "prevHashes": prevHashes, "merkleRoot": merkle, "timestamp": timestamp, "target": str(tar), "nonce": str(nonce), "hexHash": hexHash}]
  print("Mining - Current Hash:" + hexHash)
  
  if int(hexHash, 16) <= target:
    print("Mined")
    break
  
  
