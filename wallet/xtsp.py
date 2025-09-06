from cryptography.hazmat.primitives.ciphers.aead import AESGCM as pNET
from bip32utils import BIP32Key
from mnemonic import Mnemonic
from eth_utils import keccak
import base58
import time
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
  timestamp = round(time.time()).to_bytes(8, byteorder="big")
  merkle = [keccak(os.urandom(2)).hex() for _ in range(6)]
  tostr = "X" + base58.b58encode(keccak(os.urandom(32)).digest()).decode() + "TSP"
  fromstr = "X" + base58.b58encode(keccak(os.urandom(32)).digest()).decode() + "TSP"
  to = tostr.to_bytes(16, byteorder="big")
  froms = fromstr.to_bytes(16, byteorder="big")
  nonce = keccak(os.urandom(32)).digest()
  target = keccak(os.urandom(32)).digest()
  difficulty = keccak(os.urandom(32)).digest()
  prevHash = keccak(os.urandom(32)).digest()
  hexHash = keccak(timestamp + merkle + to + froms + nonce + target + difficulty + prevHash).digest()
  return {
    "timestamp": timestamp,
    "merkleRoot": merkle,
    "to": to,
    "from": froms,
    "prevHash": prevHash,
    "nonce": nonce,
    "difficulty": difficulty,
    "target": target,
    "hexHash": hexHash
  }

def privatenet():
  encryptionk = pNET(public2key)
  nunce = os.urandom(12)
  hexdata = hex().to_bytes(32, byteorder="big")

  ctxt = encryptionk.encrypt(nunce, hexdata, None)
  return ctxt

begin()

def display():
  print("YOUR PRIVATE KEY ON pnet: " + private)
  print("YOUR PUBLIC KEY ON pnet: " + public)
  print("YOUR pnet BURNER WALLET: " + wallet)
  print("YOUR ENCRYPTED HEX DATA: " + privatenet())

