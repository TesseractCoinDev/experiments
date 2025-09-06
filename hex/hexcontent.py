from termcolor import colored
from eth_utils import keccak
import random
import base58
import ecdsa
import time
import os

def transaction():
    to = "X" + base58.b58encode(keccak(os.urandom(2))).decode() + "TST"
    From = "X" + base58.b58encode(keccak(os.urandom(2))).decode() + "TST"
    amount = random.randint(1, 100)
    timestamp = str(time.time())
    s = ecdsa.SigningKey.from_string(os.urandom(32), curve=ecdsa.SECP256K1)
    v = s.verifying_key
    b = v.to_string()
    signature = b.hex()
    lens = len(to) + len(From) + len(amount) + len(timestamp) + len(signature)
    fee = 0.0001 * lens
    txid = keccak(to.encode("utf-8") + From.encode("utf-8") + str(amount).encode("utf-8") + timestamp.encode("utf-8") + signature.encode("utf-8") + fee.encode("utf-8"))
    return txid

def partition():
  version = "1.0.0"
  timestamp = str(time.time())
  transactions = [transaction() for _ in range(8)]
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

  
