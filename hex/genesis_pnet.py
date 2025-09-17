from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from bip32utils import BIP32Key
from Crypto.Hash import RIPEMD
from termcolor import colored
from mnemonic import Mnemonic
from eth_utils import keccak
import random
import base58
import ecdsa
import time
import os

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
nonce = int(keccak(keccak(publicKey2 + str(time.time()).encode("utf-8"))), 12)
pnet = AESGCM(publicKey2)

def ptransaction():
  timestamp = str(time.time())
  amount = random.randint(1, 10000)
  toAddress = wallet
  fromAddress = wallet2
  fee = (len(timestamp) + len(str(amount)) + len(toAddress) + len(fromAddress)) * 0.001
  sig = (fee.to_bytes((fee.bit_length() + 7) // 8, "big") + toAddress.encode("utf-8") + fromAddress.encode("utf-8") + timestamp.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big"))
  signature = Signature.sign_digest(sig)
  txid = keccak(keccak(sig + signature)).hex()
  
  timestampE = pnet.encrypt(timestamp.encode("utf-8"), nonce, None).hex()
  amountE = pnet.encrypt(amount.to_bytes((amount.bit_length() + 7) // 8, "big"), nonce, None).hex()
  toAddressE = pnet.encrypt(toAddress.encode("utf-8"), nonce, None).hex()
  fromAddressE = pnet.encrypt(fromAddress.encode("utf-8"), nonce, None).hex()
  signatureE = pnet.encrypt(signature, nonce, None).hex()

  return {"timestamp": timestampE, "amount": amountE, "to": toAddressE, "from": fromAddressE, "signature": signatureE, "txid": txid}

def display():
  print(colored(ptransaction(), "green", attrs=["bold"]))
