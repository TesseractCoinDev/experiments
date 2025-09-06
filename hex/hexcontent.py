from termcolor import colored
from eth_utils import keccak
import random
import time
import os

# Partion Header:
"""{
    "version": version,
    "timestamp": timestamp,
    "merkleRoot": merkle.hex(),
    "transactions": transactions.hex(),
    "target": t.hex(),
    "nonce": nonce.hex(),
    "partitionHash": partitionHash.hex()
  }"""


def partition():
  version = "1.0.0"
  timestamp = str(time.time())
  transactions = [keccak(os.urandom(2)) for _ in range(8)]
  merkle = keccak(keccak(keccak(transactions[1] + transactions[2]) + keccak(transactions[3] + transactions[4])) + keccak(keccak(transactions[5] + transactions[6]) + keccak(transactions[7] + transactions[8])))
  t = 2**256 // 2**20
  nonce = random.getrandbits(32)
  static = version.encode("utf-8") + timestamp.encode("utf-8")
  partitionHash = keccak(keccak((static + transactions + merkle + t.to_bytes(32, "big") + nonce.to_bytes(16, "big"))))
  return partitionHash

def header():
  version = "1.0.0"
  prevHashes = [keccak(os.urandom(2)) for _ in range(6)]
  merkle = keccak(os.urandom(2))
  timestamp = str(time.time())
  op = 2**256 // 2**20
  part = [partition() for _ in range(768)]
  finalized = False
  static = version.encode("utf-8") + prevHashes + merkle + timestamp.encode("utf-8") + part.encode("utf-8") + str(finalized).encode("utf-8")
  hexHash = keccak(keccak(static)).hex()
  return {
    "version": version,
    "prevHashes": prevHashes.hex(),
    "merkleRoot": merkle.hex(),
    "finalized": finalized,
    "timestamp": timestamp,
    "partitions": part.hex(),
    "hexHash": hexHash
  }

  
