from bip32utils import BIP32Key
from mnemonic import Mnemonic
from termcolor import colored
from eth_utils import keccak
import random
import base58
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

  extract = base58.b58decode(b58)
  versione = extract[0:1]
  pubhash = extract[1:21]
  checksume = extract[21:25]

  if keccak(keccak(versione + pubhash))[:4] == checksume:
    wallet = "X" + b58 + "TST"
  else:
    print(colored("[!] - Invalid Checksum, wallet is invalid.", "red", attrs=["bold"]))

begin()

def display():
  print(colored(f"YOUR TESTNET WALLET IS: {wallet}", "green", attrs=["bold"]))
  print(colored(f"YOUR PUBLIC KEY IS: {public}", "green", attrs=["bold"]))
  print(colored(f"YOUR PRIVATE KEY IS: {private}", "green", attrs=["bold"]))
  print(colored(f"YOUR SEED PHRASE IS: {mn}", "green", attrs=["bold"]))

display()
