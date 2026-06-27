```python id="t6m2vk"
import json
import time
from pathlib import Path

from eth_account import Account
from web3 import Web3

RPC_ENDPOINT = "https://rpc.example.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"

topic_a = "yield and borrow assets"
topic_b = "optimize yields for depositors"

provider = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
identity = Account.from_key(PRIVATE_KEY)

receiver = "0x0000000000000000000000000000000000000000"

runtime = {
    "started": int(time.time()),
    "connected": provider.is_connected()
}


def create_request(address):
    nonce = provider.eth.get_transaction_count(address)

    return {
        "from": address,
        "to": receiver,
        "value": 0,
        "gas": 119000,
        "gasPrice": provider.to_wei(4, "gwei"),
        "nonce": nonce,
        "chainId": 1,
    }


def sign_request(payload):
    return identity.sign_transaction(payload)


def create_snapshot(raw_hex):
    return {
        "timestamp": runtime["started"],
        "transaction": raw_hex,
        "status": runtime["connected"],
    }


def save_snapshot(snapshot):
    content = json.dumps(snapshot, indent=2)
    Path("snapshot.json").write_text(content)


def display_topics():
    print("Topic:", topic_a)
    print("Topic:", topic_b)


def display_runtime():
    print("Connected:", runtime["connected"])
    print("Started:", runtime["started"])


def display_transaction(tx):
    print("Nonce:", tx["nonce"])
    print("Gas Limit:", tx["gas"])


def execute():
    tx = create_request(identity.address)

    signed = sign_request(tx)

    encoded = signed.raw_transaction.hex()

    snapshot = create_snapshot(encoded)

    save_snapshot(snapshot)

    display_topics()

    display_runtime()

    display_transaction(tx)

    print("Address:", identity.address)

    print("Interaction stored")
