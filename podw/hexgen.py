from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Hash import RIPEMD160
import sys, os, json, time, copy
from bip32utils import BIP32Key
from eth_utils import keccak
from pathlib import Path

with open(f"{Path(__file__).parent.parent}/formats/hex.json", "r") as r:
  hex = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/tx.json", "r") as r:
  tx = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/input.json", "r") as r:
  inp = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/output.json", "r") as r:
  out = json.load(r)
hex = copy.deepcopy(hex)
tx = copy.deepcopy(tx)
inp = copy.deepcopy(inp)
out = copy.deepcopy(out)

def keygen(network):
  seed = BIP32Key.fromEntropy(os.urandom(64))
  if network == "mainnet":
    # Wait
