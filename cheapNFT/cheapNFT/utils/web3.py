
from django.conf import settings
from web3 import Web3
from web3.eth import Contract
from eth_account.messages import defunct_hash_message
from web3.middleware import geth_poa_middleware

from cheapNFT.abis.ERC721 import abi as ERC721Abi
from cheapNFT.abis.ERC20 import abi as ERC20Abi
from cheapNFT.abis.MarketPlace import abi as MarketPlace

w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def check_nft_ownable(collection: str, token_id: int, owner: str) -> (bool):
  collection_contract: Contract = w3.eth.contract(address=collection, abi=ERC721Abi)
  token_owner: str = collection_contract.functions.ownerOf(token_id).call()
  
  return token_owner.lower() == owner.lower()

def check_nft_approvement(collection: str, token_id: int, owner: str) -> (bool):
  collection_contract: Contract = w3.eth.contract(address=collection, abi=ERC721Abi)
  is_approved_for_all: bool = collection_contract.functions.isApprovedForAll(owner, settings.MARKETPLACE_ADDRESS).call()

  if is_approved_for_all:
    return True;

  approved: str = collection_contract.functions.getApproved(token_id).call()
  return approved.lower() == settings.MARKETPLACE_ADDRESS.lower()

def check_token_allowance(token: str, amount: int, owner: str) -> (bool):
  token_contract: Contract = w3.eth.contract(address=token, abi=ERC20Abi)
  allowance: int = token_contract.functions.allowance(owner, settings.MARKETPLACE_ADDRESS).call()
  balance: int = token_contract.functions.balanceOf(owner).call()

  return balance >= amount and allowance >= amount

def check_bidder_sig(collection: str, token: str, token_id: int, amount: int, bidder_sig: str) -> (str):
  bidder_message: bytes = Web3.solidity_keccak(["address", "address", "uint256", "uint256"], [collection, token, token_id, amount])
  message_hash = defunct_hash_message(primitive=bidder_message)
  
  bidder = w3.eth.account._recover_hash(message_hash, signature=bidder_sig)

  return bidder

def finish_auction(marketplace: str, collection: str, token: str, token_id: int, bid: str, bidder_sig: str, owner_approved_sig: str) -> (str):
  marketplace_contract: Contract = w3.eth.contract(address=marketplace, abi=MarketPlace)
  result = marketplace_contract.functions.finishAuction((collection, token, token_id, bid), bidder_sig, owner_approved_sig)

  return result