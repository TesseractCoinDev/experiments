from termcolor import colored
from eth_utils import keccak
import random
import time
import os

difficulty = 2**20
target = 2**256 // difficulty

def mine():
  while True:
    version = "1.0.0"
    prevHashes = [keccak(os.urandom(2)).hex() for _ in range(6)]
    merkle = keccak(os.urandom(2)).hex()
    timestamp = str(time.time())
    tar = target
    nonce = random.getrandbits(80)
    s = (version.encode() + "".join(prevHashes).encode() + merkle.encode() + timestamp.encode())
    sf = s + tar.to_bytes(32, "big") + nonce.to_bytes(16, "big")
    hexHash = keccak(keccak(sf)).hex()
    hexHeader = [{"verison": version, "prevHashes": prevHashes, "merkleRoot": merkle, "timestamp": timestamp, "target": str(tar), "nonce": str(nonce), "hexHash": hexHash}]
    print(colored(f"Mining - Current Hash: {hexHash}", "red", attrs=["bold"]))
  
    if int(hexHash, 16) <= target:
      print(colored("Hex Has Been Mined!", "red", attrs=["bold"]))
      time.sleep(2)
      break
