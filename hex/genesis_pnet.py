from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from bip32utils import BIP32Key
from Crypto.Hash import RIPEMD
from termcolor import colored
from mnemonic import Mnemonic
from eth_utils import keccak
import random
import base58
import json
import ecdsa
import time
import os

subdifficulty = 100000 * 0.028
subtarget = (2**224) * ((2**32) - 1) // round(subdifficulty)
lang = Mnemonic("english")

def gen():
  global signing, wallet, public
  entropy = os.urandom(24)
  seedphrase = lang.to_mnemonic(entropy)
  seed = lang.to_seed(seedphrase, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey()
  public = master.PublicKey()
  signing = ecdsa.SigningKey.from_string(private, curve=ecdsa.SECP256k1)

  version = bytes([0x54])
  pub = RIPEMD.new(public).digest()
  checksum = keccak(keccak(version + pub))[:4]
  raw = base58.b58encode(version + pub + checksum).decode()

  extraction = base58.b58decode(raw)
  version = extraction[0:1]
  puB = extraction[1:21]
  checkSum = extraction[21:25]
  if keccak(keccak(version + pub))[:4] == checkSum:
    wallet = "X" + raw + "TST"
    return wallet
  else:
    wallet = "Invalid"

gen()
Signature = signing
Wallet = wallet

gen()
Wallet2 = wallet
publicKey2 = public
nonce = os.urandom(12)
pnet = AESGCM(keccak(publicKey2))

def ptransaction():
  timestamp = str(time.time())
  amount = random.randint(1, 10000)
  toAddress = wallet
  fromAddress = Wallet2
  fee = (len(timestamp) + len(str(amount)) + len(toAddress) + len(fromAddress)) * 0.001
  sig = keccak((str(fee).encode("utf-8") + toAddress.encode("utf-8") + fromAddress.encode("utf-8") + timestamp.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big")))
  signature = Signature.sign_digest(sig)
  txid = keccak(keccak(sig + signature + nonce))
  
  timestampE = pnet.encrypt(nonce, timestamp.encode("utf-8"), None).hex()
  amountE = pnet.encrypt(nonce, amount.to_bytes((amount.bit_length() + 7) // 8, "big"), None).hex()
  toAddressE = pnet.encrypt(nonce, toAddress.encode("utf-8"), None).hex()
  fromAddressE = pnet.encrypt(nonce, fromAddress.encode("utf-8"), None).hex()

  return {"nonce": nonce.hex(), "timestamp": timestampE, "amount": amountE, "fee": str(fee), "to": toAddressE, "from": fromAddressE, "signature": signature.hex(), "txid": txid.hex()}, txid

def partition():
  version = 1
  timestamp = str(time.time())
  nonce = random.getrandbits(80)
  extraNonce = 0
  sub_target = subtarget.to_bytes((subtarget.bit_length() + 7) // 8, "big")
  transactioneq = 35951 // 768
  txids = [ptransaction()[1] for _ in range(transactioneq)]
  while len(txids) > 1:
      if len(txids) % 2 == 1:
          txids.append(txids[-1])
      merklep = []
      for p in range(0, len(txids), 2):
          merklep.append(keccak(txids[p] + txids[p+1]))
      txids = merklep
  merkleRoot = txids[0]  
  partitionHash = keccak(keccak(version.to_bytes(4, "big") + timestamp.encode("utf-8") + nonce.to_bytes(80, "big") + extraNonce.to_bytes(32, "big") + sub_target + merkleRoot))
  partitionData =  {
    "partitionHeader": {"version": version, "merkleRoot": merkleRoot.hex(), "subTarget": sub_target.hex(), "nonce": nonce, "extraNonce": extraNonce, "partitionHash": partitionHash.hex()},
    "partitionBody": [ptransaction()[0] for _ in range(transactioneq)]
  }
  return partitionData, partitionHash

def hex():
  version = 1
  timestamp = str(time.time())
  height = 1
  prevHash = "0"*64
  partitions = [partition()[1] for _ in range(768)]
  while len(partitions) > 1:
      if len(partitions) % 2 == 1:
          partitions.append(partitions[-1])
      merkleh = []
      for h in range(0, len(partitions), 2):
          merkleh.append(keccak(partitions[h] + partitions[h+1]))
      partitions = merkleh
  merkleRoot = partitions[0]
  hexHash = keccak(keccak(version.to_bytes((version.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + merkleRoot + height.to_bytes((height.bit_length() + 7) // 8, "big") + bytes.fromhex(prevHash)))
  hexData =  {
    "header": {"version": version, "network": "xts-pnet", "prevHash": prevHash, "height": height, "merkleRoot": merkleRoot.hex(), "timestamp": timestamp, "hexHash": hexHash.hex()},
    "body": [partition()[0] for _ in range(768)]
  }
  with open("genesis_pnet.json", "w") as w:
    json.dump(hexData, w, indent=4)

hex()
