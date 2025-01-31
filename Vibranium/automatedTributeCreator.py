import requests
from uuid import uuid4
from hashlib import sha256
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from web3 import Web3
from random import randint
import json
import hashlib
import time
import random

# Load ABIs
with open('VBToken.json', 'r') as abi_file:
    token_abi = json.load(abi_file)

with open('TimelockFactory.json', 'r') as abi_file:
    factory_abi = json.load(abi_file)

# Hardcoded values
time_lock_factory_contract_address = Web3.to_checksum_address('0x0013E32EFB4083B0fD4d21A3B1774C6A387F37e7')
token_contract_address = Web3.to_checksum_address('0x5Ac0a114c2D9507E0f3Dd1dd7Ba0a4c12434ec34')
user_wallet_address = Web3.to_checksum_address('0x0872163FB0BCf3aBe4EFd957149AB07dD3707080')
private_key = '3574c2ea1ff187f7f6f61fa00fd9023b940336050a6cf5421c88484238779382'
user_id = 'did:privy:clq5ul2t20052jj0f21sg350a'
bounty_amount_range = (100, 1000)
target_count = 200
expiration_date = (datetime.now() + timedelta(days=7)).isoformat()
used_articles = set()

# Initialize Web3
web3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/pTS-PJgj5o9qYmVErQltBp0GJNdbPbCI'))

# Function to scrape articles from CNN
def get_next_article():
    response = requests.get('https://www.cnn.com')
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', href=True)

    found_articles = [
        f"https://www.cnn.com{link['href']}" for link in articles
        if link['href'].startswith('/') and '/202' in link['href']
    ]

    for article_url in found_articles:
        if article_url not in used_articles:
            used_articles.add(article_url)
            return article_url

    return None

# Function to extract article details
def scrape_article_details(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1').text if soup.find('h1') else 'No Title'
    description = soup.find('meta', {'name': 'description'})
    description = description['content'] if description else 'No Description'
    image = soup.find('meta', {'property': 'og:image'})
    image = image['content'] if image else None

    return {'title': title, 'description': description, 'image': image}

# Function to create bounty
def create_bounty():
    try:
        article_url = get_next_article()
        if not article_url:
            print("No new articles available.")
            return

        article_details = scrape_article_details(article_url)
        unique_id = str(uuid4())
        bounty_amount = randint(*bounty_amount_range)

        post = {
            'uniqueId': unique_id,
            'title': article_details['title'],
            'description': article_details['description'],
            'creator': "Ahmad",
            'expirationDate': expiration_date,
            'tags': ['news', 'article'],
            'target': target_count,
            'bounty': bounty_amount,
            'vFluencer': 'Some vFluencer Name',
            'originalUrl': article_url,
            'image': article_details['image'],
            'iFrameData': None,
            'uniqueIdentifier': user_id
        }

        response = requests.post('https://vfluencealphaone-vbndev-vbndev-s-team.vercel.app/api/bounty/createBounty', json=post)

        if response.status_code == 200:
            print('Bounty created successfully:', response.json())
            interact_with_blockchain(post, response.json())
        else:
            print('Failed to create bounty:', response.text)

    except Exception as e:
        print('Error:', str(e))

def generate_unique_id_hash():
    unique_id_hash = hashlib.sha256(f"{time.time()}{random.randint(0, int(1e18))}".encode()).hexdigest()
    print(f"uniqueIdHash: 0x{unique_id_hash}")
    return f"0x{unique_id_hash}"

# Function to approve token spending
def approve_tokens(amount):
    balance = web3.eth.get_balance(user_wallet_address)
    print(f"Wallet Balance: {web3.from_wei(balance, 'ether')} ETH")
    print("Connected to Sepolia:", web3.is_connected())
    print("Connected to Sepolia:", user_wallet_address)

    token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)
    approve_txn = token_contract.functions.approve(
        time_lock_factory_contract_address,
        amount
    ).build_transaction({
        'from': user_wallet_address,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(user_wallet_address),
    })

    signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_approve_txn.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approval Transaction Hash: {tx_hash.hex()}")

def send_transaction(bounty_details, create_bounty_response):
    try:
        balance = web3.eth.get_balance(user_wallet_address)
        print(f"Wallet Balance: {web3.from_wei(balance, 'ether')} ETH")

        factory_contract = web3.eth.contract(address=time_lock_factory_contract_address, abi=factory_abi)
        unique_id_hash = generate_unique_id_hash()

        # ✅ Step 1: Approve Tokens Before Funding
        approve_tokens(bounty_details['bounty'])

        # ✅ Step 2: Build Transaction
        bounty_txn = factory_contract.functions.createBountyAndFund(
            token_contract_address,
            bounty_details['originalUrl'],
            bounty_details['title'],
            bounty_details['description'],
            user_wallet_address,
            bounty_details['bounty'],
            bounty_details['image'],
            bounty_details['target'],
            int(datetime.fromisoformat(bounty_details['expirationDate'].replace('Z', '')).timestamp()),
            bounty_details['bounty'],
            unique_id_hash
        ).build_transaction({
            'from': user_wallet_address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(user_wallet_address),
        })

        print("Generated Transaction:", bounty_txn)

        # ✅ Step 3: Sign & Send Transaction
        signed_bounty_txn = web3.eth.account.sign_transaction(bounty_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_bounty_txn.raw_transaction)

        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Bounty Transaction Hash: {tx_hash.hex()}")

        # ✅ Step 4: Send Transaction Hash to Backend
        tx_hash_hex = f"0x{tx_hash.hex()}"  # Ensure the hash starts with '0x'

        tracker_response = requests.post(
            'https://vfluence-blockchain-server.onrender.com/transactionTracker',
            json={'txHash': tx_hash_hex, 'uniqueId': unique_id_hash}
        )

        print(f"Sent Transaction Hash to Backend: {tx_hash_hex}")


        if tracker_response.status_code == 200:
            print("Transaction hash logged successfully.")
        else:
            print("Failed to log transaction hash:", tracker_response.text)

    except Exception as error:
        print(f"Error in transaction: {error}")

# Call send_transaction after create_bounty
def interact_with_blockchain(bounty_details, create_bounty_response):
    send_transaction(bounty_details, create_bounty_response)

if __name__ == '__main__':
    create_bounty()
