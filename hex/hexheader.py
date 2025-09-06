from termcolor import colored
from eth_utils import keccak
import random
import json
import time
import os

def header():
  version = "1.0.0"
  prevHashes = [keccak(os.urandom(2)) for _ in range(6)]
  merkle = keccak(os.urandom(2))
  timestamp = str(time.time())
  op = 2**256 // 2**20
  subtargets = [random.getrandbits(op) for _ in range(768)]
  finalized = False
  static = version.encode("utf-8") + prevHashes + merkle + timestamp.encode("utf-8") + subtargets.to_bytes(30, "big") + str(finalized).encode("utf-8")
  hexHash = keccak(keccak(static)).hex()
  return {
    "version": version,
    "prevHashes": prevHashes.hex(),
    "merkleRoot": merkle.hex(),
    "finalized": finalized,
    "timestamp": timestamp,
    "subtargets": subtargets,
    "hexHash": hexHash
  }
  
  
