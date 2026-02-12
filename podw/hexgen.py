from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from Crypto.Hash import RIPEMD160
import sys, os, json, time, copy
from bip32utils import BIP32Key
from eth_utils import keccak
from pathlib import Path

with open(f"{Path(__file__).parent.parent}/formats/testnet/hex.json", "r") as r:
  hex = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/testnet/partitions.json", "r") as r:
  partition = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/testnet/tx.json", "r") as r:
  tx = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/testnet/input.json", "r") as r:
  inp = json.load(r)
with open(f"{Path(__file__).parent.parent}/formats/testnet/output.json", "r") as r:
  out = json.load(r)
hex, partition, tx, inp, out = copy.deepcopy(hex), copy.deepcopy(partition), copy.deepcopy(tx), copy.deepcopy(inp), copy.deepcopy(out)

def keygen(network):
  if network == "test":
    seed = BIP32Key.fromEntropy(os.urandom(64))
    address = "X" + base58.b58encode(hex([0x54]) + RIPEMD160.new(seed.PublicKey()).digest() + keccak(keccak(hex([0x54]) + RIPEMD160.new(seed.PublicKey()).digest()))[:4]).decode() + "TST"
    return (seed.PrivateKey()).hex(), address

def tx(network):
  privateKey, address = keygen(network)
  
  if not os.path.exists("testnet_hex.json"):
    inp["txid"], inp["vout"], inp["scriptSig"], inp["sequence"] = "0"*64, 0, ("Sometimes I dream of saving the world. Saving everyone from the invisible hand, the one that brands us with an employee badge.".encode("utf-8")).hex(), 0

    out["value"], out["scriptPubKey"]["hex"] = 250000000, ("How do we know if we're in control? That we're not just making the best of what comes at us, and that's it? Trying to constantly pick between two shitty options?".encode("utf-8")).hex()
    out["scriptPubKey"]["addresses"].append(keygen("test")[1])
  else:
    inp["txid"], inp["vout"], inp["scriptSig"], inp["sequence"] = 
