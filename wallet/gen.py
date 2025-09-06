from bip32utils import BIP32Key
from mnemonic import Mnemonic
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
  print("YOUR testnet WALLET IS: " + wallet)
  print("YOUR PUBLIC KEY IS: " + public)
  print("YOUR PRIVATE KEY IS: " + private)
  print("YOUR SEED PHRASE IS: " + seed.hex())
  
