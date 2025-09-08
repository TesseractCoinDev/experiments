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
subtarget = 2**256 / subdifficulty
mnemonics = Mnemonic("english")

def genadd():
  entropy = os.urandom(16)
  seedphrase = mnemonics.to_mnemonic(entropy)
  seed = mnemonics.to_seed(seedphrase, passphrase="")

  master = BIP32Key.fromEntropy(seed)
  private = master.PrivateKey()
  public = master.PublicKey()
  signing = ecdsa.SigningKey.from_string(private, curve=ecdsa.SECP256k1)

  testnet = bytess([ord('T'])
  pubhash = keccak(public)[:20]
  checksum = keccak(keccak(testnet + pubhash))
  prewallet = base58.b58encode(testnet + pubhash + checksum).decode()

  extraction = base58.b58decode(prewallet)
  version = extraction[0:1]
  pubHash = extraction[1:21]
  checkSum = extraction[21:25]
  if keccak(keccak(version + pubHash)) == checkSum:
    return "X" + pre + "TST", private, signing
  else:
    return "Invalid"

def transaction():
  toAddress = genadd()[0]
  fromAddress = genadd()[0]
  amount = random.randint(1, 1000)
  timestamp = str(time.time())
  fee = (len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp)) * 0.0001
  signature = signing.sign_digest(keccak(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + fee.to_bytes((fee.bit_length() + 7) // 8, "big")))
  txid = keccak(toAddress.encode("utf-8") + fromAddress.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + fee.to_bytes((fee.bit_length() + 7) // 8, "big") + signature)
  weight = len(toAddress) + len(fromAddress) + len(str(amount)) + len(timestamp) + len(str(fee)) + len(signature.hex()) + len(txid.hex())
  return {"to": toAddress, "from": fromAddress, "amount": amount, "timestamp": timestamp, "fee": fee, "signature": signature, "txid": txid}, txid, weight

def genisispartition():
  version = 1
  timestamp = str(time.time())
  nonce = random.getrandbits(80)
  sub_target = subtarget.to_bytes(subtarget.bit_length() + 7) // 8, "big")
  transactioneq = 35951 // 768
  txids = [transaction()[1], for _ in range(transactioneq)]
  while len(txids) > 1:
      if len(txids) % 2 == 1:
          txids.append(txids[-1])
      merklep = []
      for p in range(0, len(txids), 2):
          merklep.append(keccak(txids[h] + txids[h+1]))
      txids = merklep
  merkleRoot = txids[0]  
  prevHash = "0"*64
  partitionHash = keccak(keccak(version.to_bytes(version.bit_length() + 7) // 8, "big") + timestamp.encode("utf-8") + nonce.to_bytes(nonce.bit_length() + 7) // 8, "big") + subtarget + merkleroot + prevHash.encode("utf-8")))
  return {"version": version, "prevHash": prevHash, "merkleRoot": merkleRoot.hex(), "difficultyTarget": sub_target.hex(), "nonce": nonce, "partitionHash": partitionHash.hex()}, partitionHash
  
