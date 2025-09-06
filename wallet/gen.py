from cryptography.hazmat.primitives.ciphers.aead import AESGCM as pNET
from bip32utils import BIP32Key
from mnemonic import Mnemonic
from termcolor import colored
from eth_utils import keccak
import random
import base58
import time
import json
import os

private = ""
public = ""
master = ""
wallet = ""
seed = ""
init = Mnemonic("english")

def begin():
  global private, public, wallet, seed
  entropy = os.urandom(24)
  mn = init.to_mnemonic(entropy)
  seed = init.to_seed(mn, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey().hex()
  public = master.PublicKey().hex()

  kek = keccak(master.PublicKey())
  b58 = base58.b58encode(kek).decode()
  wallet = "X" + b58 + "TSP"

begin()

def hex():
  timestamp = str(time.time())
  merkle = [keccak(os.urandom(2)).hex() for _ in range(6)]
  to = "X" + base58.b58encode(keccak(os.urandom(32))).decode() + "TSP"
  froms = "X" + base58.b58encode(keccak(os.urandom(32))).decode() + "TSP"
  nonce = random.getrandbits(128)
  difficulty = 2**20
  target = 2**256 // difficulty
  prevHash = keccak(os.urandom(32))
  s = (timestamp.encode("utf-8") + to.encode("utf-8") + froms.encode("utf-8") + prevHash)
  final = s + target.to_bytes(32, "big") + nonce.to_bytes(16, "big")
  hexHash = keccak(final).hex()
  return {
    "timestamp": timestamp,
    "merkleRoot": merkle,
    "to": to,
    "from": froms,
    "prevHash": prevHash.hex(),
    "nonce": nonce,
    "target": target,
    "hexHash": hexHash
  }

def privatenet():
  encryptionk = pNET(keccak(bytes.fromhex(public)))
  transaction = json.dumps(hex()).encode()
  nunce = os.urandom(12)

  ctxt = encryptionk.encrypt(nunce, transaction, None)
  return ctxt

begin()

def display():
  print(colored(f"YOUR pnet WALLET IS: {wallet}", "green", attrs=["bold"]))
  print(colored(f"YOUR PUBLIC KEY IS: {public}", "green", attrs=["bold"]))
  print(colored(f"YOUR PRIVATE KEY IS: {private}", "green", attrs=["bold"]))
  print(colored(f"YOUR SEED IS: {seed.hex()}", "green", attrs=["bold"]))
  print(colored(f"YOUR ENCRYPTED TRANSACTION IS: {privatenet().hex()}", "green", attrs=["bold"]))
