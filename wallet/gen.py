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
mn = ""
init = Mnemonic("english")

def begin():
  global private, public, wallet, mn
  entropy = os.urandom(24)
  mn = init.to_mnemonic(entropy)
  seed = init.to_seed(mn, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey().hex()
  public = master.PublicKey().hex()
  testnet = bytes([0x54])
  mainnet = bytes([0x58])
  pnet = bytes([0x50])
  pubkeyh = keccak(master.PublicKey())[:20]
  checksum = keccak(keccak(testnet + pubkeyh))[:4]
  b58 = base58.b58encode(testnet + pubkeyh + checksum).decode()
  wallet = "X" + b58 + "TST"

begin()

def display():
  print(colored(f"YOUR TESTNET WALLET IS: {wallet}", "green", attrs=["bold"]))
  print(colored(f"YOUR PUBLIC KEY IS: {public}", "green", attrs=["bold"]))
  print(colored(f"YOUR PRIVATE KEY IS: {private}", "green", attrs=["bold"]))
  print(colored(f"YOUR SEED PHRASE IS: {mn}", "green", attrs=["bold"]))

display()
