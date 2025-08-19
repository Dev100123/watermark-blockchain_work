import json
from solcx import compile_standard, install_solc

def compile_contract():
    # Install Solidity compiler
    install_solc("0.8.0")

    # Read the Solidity contract
    with open("contract/ProductTracker.sol", "r") as file:
        source_code = file.read()

    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                "ProductTracker.sol": {
                    "content": source_code
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        },
        solc_version="0.8.0",
    )

    # Save full compile output
    with open("contract/contract_abi.json", "w") as file:
        json.dump(compiled_sol, file)

    print("✅ Compilation complete. ABI and bytecode saved.")