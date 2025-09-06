from bip32utils import BIP32Key
from mnemonic import Mnemonic
from termcolor import colored
from eth_utils import keccak
import base58
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
  wallet = "X" + b58 + "TST"

begin()

def display():
  print(colored(f"YOUR testnet WALLET IS: {wallet}", "green", attrs=["bold"]))
  print(colored(f"YOUR PUBLIC KEY IS: {public}", "green", attrs=["bold"]))
  print(colored(f"YOUR PRIVATE KEY IS: {private}", "green", attrs=["bold"]))
  print(colored(f"YOUR SEED IS: {seed.hex()}", "green", attrs=["bold"]))
  
