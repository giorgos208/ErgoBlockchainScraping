# Import packages

import json
import logging
import requests
import time
from ergpy import helper_functions, appkit

# Logging utility
LOGGING_FORMAT = '[%(asctime)s] - [%(levelname)-8s] -  %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create connection to the blockchain
node_url = "http://213.239.193.208:9053/"  # MainNet or TestNet
ergo = appkit.ErgoAppKit(node_url=node_url)

wallet_mnemonic = ""

receiver_addresses = [
    "",
    ""
]
amounts = [0.1, 0.15]


def process_txs(array):
    receiver_addresses = []
    amounts = []
    for i in range(len(array)):
        print(f"{array[i]['sender']} has sent {array[i]['value']} ergo to us.")
        receiver_addresses.append(array[i]['sender'])
        amounts.append(int(array[i]['value']) / 5 / 1e9)
    print(receiver_addresses)
    print()
    print(amounts)
    print()
    print(helper_functions.simple_send(ergo=ergo, amount=amounts, wallet_mnemonic=wallet_mnemonic, receiver_addresses=receiver_addresses))
    helper_functions.exit()


def check_for_transactions():
    address = ''
    file_path = 'index.txt'
    
    with open(file_path, 'r') as file:
        content = file.read().strip()
        index = int(content)

    url = f'https://api.ergoplatform.com/api/v1/addresses/{address}/transactions'
    response = requests.get(url)

    if response.status_code == 200:
        transactions = response.json()['items']
        print(f"Searching for transactions after Global Index: {index}")
        filtered_transactions = [t for t in transactions if t['globalIndex'] > index]
        
        if filtered_transactions:
            print(f"Found new transactions: {len(filtered_transactions)}")
            last_index = filtered_transactions[0]['globalIndex']
            
            with open(file_path, 'w') as file:
                file.write(str(last_index))
                
            valid_txs = [tx for tx in filtered_transactions if tx['inputs'][0]['address'] != address and tx['outputs'][0]['address'] == address]
            
            if valid_txs:
                print(f"Found {len(valid_txs)} legit transactions. Processing!")
                process_txs(valid_txs)
    else:
        print(f"Error: Unable to retrieve transactions (HTTP {response.status_code}).")


if __name__ == "__main__":
    check_for_transactions()
    exit()
