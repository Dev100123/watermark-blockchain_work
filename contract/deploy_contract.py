import json
import os
from web3 import Web3

DEPLOY_FLAG_PATH = "contract/contract_address.txt"

def is_contract_deployed():
    return os.path.exists(DEPLOY_FLAG_PATH)

def deploy_contract():
    # Load compiled contract
    with open("contract/contract_abi.json", "r") as file:
        compiled_contract = json.load(file)

    # Parse ABI and bytecode
    abi = compiled_contract['contracts']['ProductTracker.sol']['ProductTracker']['abi']
    bytecode = compiled_contract['contracts']['ProductTracker.sol']['ProductTracker']['evm']['bytecode']['object']

    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    w3.eth.default_account = w3.eth.accounts[0]

    # Deploy contract
    ProductTracker = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ProductTracker.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("✅ Contract deployed at address:", tx_receipt.contractAddress)

    # Optionally save address
    with open("contract/contract_address.txt", "w") as f:
        f.write(tx_receipt.contractAddress)