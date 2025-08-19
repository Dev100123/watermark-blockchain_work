import json
from web3 import Web3

# This module handles the interaction with the Ethereum smart contract for product tracking.
def load_contract():
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    web3.eth.default_account = web3.eth.accounts[0]

    with open("contract/contract_address.txt") as f:
        contract_address = f.read().strip()

    with open("contract/contract_abi.json") as f:
        abi = json.load(f)['contracts']['ProductTracker.sol']['ProductTracker']['abi']

    contract = web3.eth.contract(address=contract_address, abi=abi)
    return contract

def add_product(hash_code, name_registration):
    contract = load_contract()
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    web3.eth.default_account = web3.eth.accounts[0]
    
    tx_hash = contract.functions.addOrUpdateProduct( 
        hash_code, name_registration
    ).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)

def get_all_products():
    contract = load_contract()
    count = contract.functions.getProductCount().call()
    return [contract.functions.getProductByIndex(i).call() for i in range(count)]

