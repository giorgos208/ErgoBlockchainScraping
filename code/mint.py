# Import standard packages
import json
import logging
import time

# Import custom packages
from ergpy import helper_functions, appkit

# Initialize logging
LOGGING_FORMAT = '[%(asctime)s] - [%(levelname)-8s] -  %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Blockchain connection parameters
NODE_URL = "http://213.239.193.208:9053/"  # MainNet or TestNet
WALLET_MNEMONIC = ""

# Initialize ErgoAppKit
ergo = appkit.ErgoAppKit(node_url=NODE_URL)

# NFT parameters
RECEIVER_ADDRESSES = [
    "",
    ""
]
AMOUNT_NFTS_TO_MINT = 2
ROYALTY = 0
NFT_NAME = "Test MINT"
DESCRIPTION = "Just a test"
IMAGE_LINK = "ipfs://"
IMAGE_HASH = appkit.sha256caster("")

# Create issuer boxes with royalties
tx = helper_functions.create_issuer_box(
    ergo=ergo,
    wallet_mnemonic=WALLET_MNEMONIC,
    royalty_amount_in_percent=ROYALTY,
    amount_of_boxes=AMOUNT_NFTS_TO_MINT,
    return_signed=True
)

# Convert issuer box outputs to inputs for chained transactions
issuer_boxes = [appkit.get_outputs_to_spend(tx, i) for i in range(AMOUNT_NFTS_TO_MINT)]

# Send the issuer box transaction and log the transaction ID
print(ergo.txId(tx))

# Mint NFTs using the issuer boxes
for i in range(AMOUNT_NFTS_TO_MINT):
    print(
        helper_functions.create_nft(
            ergo=ergo,
            nft_name=f"{NFT_NAME}{i + 1}",
            description=DESCRIPTION,
            image_link=IMAGE_LINK,
            image_hash=IMAGE_HASH,
            wallet_mnemonic=WALLET_MNEMONIC,
            input_box=issuer_boxes[i]
        )
    )

# Clean up resources
helper_functions.exit()
