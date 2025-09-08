from bip32utils import BIP32Key
from mnemonic import Mnemonic
from termcolor import colored
from eth_utils import keccak
import base58
import random
import ecdsa
import time
import os

subdifficulty = 100000 * 0.028
subtarget = 2**256 // round(subdifficulty)
mnemonics = Mnemonic("english")

def genadd():
  global signing
  entropy = os.urandom(16)
  seedphrase = mnemonics.to_mnemonic(entropy)
  seed = mnemonics.to_seed(seedphrase, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey()
  public = master.PublicKey()
  signing = ecdsa.SigningKey.from_string(private, curve=ecdsa.SECP256k1)

  testnet = bytes([ord('T')])
  pubhash = keccak(public)[:20]
  checksum = keccak(keccak(testnet + pubhash))[:4]
  pre = base58.b58encode(testnet + pubhash + checksum).decode()

  extraction = base58.b58decode(pre)
  version = extraction[0:1]
  pubHash = extraction[1:21]
  checkSum = extraction[21:25]
  if keccak(keccak(version + pubHash))[:4] == checkSum:
    wallet = "X" + pre + "TST"
    return wallet, private
  else:
    return "Invalid"

def transaction():
  toAddress = genadd()[0]
  fromAddress = genadd()[0]
  amount = random.getrandbits(round(time.time())
  timestamp = str(time.time())
  fee = (len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp)) * 0.0001
  signature = signing.sign_digest(keccak(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + str(fee).encode("utf-8")))
  txid = keccak(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + str(fee).encode("utf-8") + signature)
  weight = len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp) + len(str(fee)) + len(signature.hex()) + len(txid.hex())
  return {"to": toAddress, "from": fromAddress, "amount": amount, "timestamp": timestamp, "fee": fee, "signature": signature.hex(), "txid": txid.hex()}, txid, weight

def genisispartition():
  version = 1
  timestamp = str(time.time())
  nonce = random.getrandbits(80)
  sub_target = subtarget.to_bytes((subtarget.bit_length() + 7) // 8, "big")
  transactioneq = 35951 // 768
  txids = [transaction()[1] for _ in range(transactioneq)]
  while len(txids) > 1:
      if len(txids) % 2 == 1:
          txids.append(txids[-1])
      merklep = []
      for p in range(0, len(txids), 2):
          merklep.append(keccak(txids[p] + txids[p+1]))
      txids = merklep
  merkleRoot = txids[0]  
  partitionHash = keccak(keccak(version.to_bytes(4, "big") + timestamp.encode("utf-8") + nonce.to_bytes(10, "big") + sub_target + merkleRoot))
  weight = len(str(version)) + len(merkleRoot.hex()) + len(sub_target.hex()) + len(str(nonce)) + len(partitionHash.hex())
  return {"version": version, "merkleRoot": merkleRoot.hex(), "difficultyTarget": sub_target.hex(), "nonce": nonce, "partitionHash": partitionHash.hex()}, partitionHash, weight

def hex():
  version = 1
  timestamp = str(time.time())
  height = 1
  prevHash = "0"*64
  partitions = [genisispartition()[1] for _ in range(10)]
  while len(partitions) > 1:
      if len(partitions) % 2 == 1:
          partitions.append(partitions[-1])
      merkleh = []
      for h in range(0, len(partitions), 2):
          merkleh.append(keccak(partitions[h] + partitions[h+1]))
      partitions = merkleh
  merkleRoot = partitions[0]
  hexHash = keccak(keccak(version.to_bytes((version.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + merkleRoot + height.to_bytes((height.bit_length() + 7) // 8, "big") + bytes.fromhex(prevHash)))
  weight = len(str(version)) + len(prevHash) + len(str(height)) + len(merkleRoot.hex()) + len(timestamp) + len(hexHash)
  return {"version": version, "prevHash": prevHash, "height": height, "merkleRoot": merkleRoot.hex(), "timestamp": timestamp, "hexHash": hexHash.hex()}, weight

print(colored(f"HEX HEADER ({str(hex()[1])} BITS): ", "white", attrs=["bold"]))
print(colored(hex()[0], "green", attrs=["bold"]))
print("")
print(colored(f"PARTITION HEADER ({str(genisispartition()[2])} BITS):", "white", attrs=["bold"]))
print(colored(genisispartition()[0], "green", attrs=["bold"]))
print("")
print(colored(f"TRANSACTION METADATA ({str(transaction()[2])} BITS):", "white", attrs=["bold"]))
print(colored(transaction()[0], "green", attrs=["bold"]))
print("")
print(colored("STATS:", "white", attrs=["bold"]))
equ = ((hex()[1]) + (genisispartition()[2] * 768) + (transaction()[2] * 35951)) / 8
print(colored(f"TOTAL SIZE: {str(equ)} OF 1,500,000 BYTES", "white", attrs=["bold"]))
