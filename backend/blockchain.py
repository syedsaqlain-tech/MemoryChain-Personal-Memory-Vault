import json
from web3 import Web3

GANACHE_URL = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

print("Connected:", web3.is_connected())

contract_address = "0x73F46112B95E8769Abc0FfF9Fcb3e482860A1d2f"

with open("abi.json", "r") as file:
    contract_abi = json.load(file)

contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

print("Contract Address:", contract_address)
print("Total Memories:", contract.functions.totalMemories().call())