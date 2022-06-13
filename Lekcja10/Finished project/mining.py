import time
import json
import requests
from multiprocessing import Process, Pipe
import ecdsa
import hashlib
import base64
from flask import Flask, request

from mining_config import MINER_ADDRESS, MINER_NODE_URL, PEER_NODES

node = Flask(__name__)


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

        # Example
        # index = 0
        # timestamp = time.time()
        # data = 'Alex'
        # previous_hash = '4f04cb3e61f53d4d31ddd3e64af73d88db9c1518c5a7fb3b68442c00eb4346f6'


    def hash_block(self): 
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()


def create_genesis_block():
    return Block(0, time.time(), {
        "proof-of-work": 9,
        "transactions": None},
                 "0")


# Node's blockchain copy
BLOCKCHAIN = [create_genesis_block()]
NODE_PENDING_TRANSACTIONS = []


def proof_of_work(last_proof, blockchain):
    incrementer = last_proof + 1
    start_time = time.time()
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
        if int((time.time()-start_time) % 60) == 0:
            new_blockchain = consensus(blockchain)
            if new_blockchain:
                return False, new_blockchain
    return incrementer, blockchain


def mine(a, blockchain, node_pending_transactions):
    BLOCKCHAIN = blockchain
    NODE_PENDING_TRANSACTIONS = node_pending_transactions
    while True:
        last_block = BLOCKCHAIN[len(BLOCKCHAIN) - 1]
        last_proof = last_block.data['proof-of-work']
        proof = proof_of_work(last_proof, BLOCKCHAIN)
        if not proof[0]:
            BLOCKCHAIN = proof[1]
            a.send(BLOCKCHAIN)
            continue
        else:
            NODE_PENDING_TRANSACTIONS = requests.get(MINER_NODE_URL + "/txion?update=" + MINER_ADDRESS).content
            NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)
            NODE_PENDING_TRANSACTIONS.append({
                "from": "network",
                "to": MINER_ADDRESS,
                "amount": 1})
            new_block_data = {
                "proof-of-work": proof[0],
                "transactions": list(NODE_PENDING_TRANSACTIONS)
            }
            new_block_index = last_block.index + 1
            new_block_timestamp = time.time()
            last_block_hash = last_block.hash
            NODE_PENDING_TRANSACTIONS = []
            # Now create the new block
            mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
            BLOCKCHAIN.append(mined_block)
            print(json.dumps({
              "index": new_block_index,
              "timestamp": str(new_block_timestamp),
              "data": new_block_data,
              "hash": last_block_hash
            }) + "\n")

            a.send(BLOCKCHAIN)
            requests.get(MINER_NODE_URL + "/blocks?update=" + MINER_ADDRESS)


def find_new_chains():
    other_chains = []
    for node_url in PEER_NODES:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        validated = validate_blockchain(block)
        if validated:
            other_chains.append(block)
    return other_chains


def consensus(blockchain):
    other_chains = find_new_chains()
    BLOCKCHAIN = blockchain
    longest_chain = BLOCKCHAIN
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    if longest_chain == BLOCKCHAIN:
        return False
    else:
        BLOCKCHAIN = longest_chain
        return BLOCKCHAIN


def validate_blockchain(block):
    return True


@node.route('/blocks', methods=['GET'])
def get_blocks():
    if request.args.get("update") == MINER_ADDRESS:
        global BLOCKCHAIN
        BLOCKCHAIN = b.recv()
    chain_to_send = BLOCKCHAIN
    # Converts our blocks into dictionaries so we can send them as json objects later
    chain_to_send_json = []
    for block in chain_to_send:
        block = {
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "data": str(block.data),
            "hash": block.hash
        }
        chain_to_send_json.append(block)

    chain_to_send = json.dumps(chain_to_send_json)
    return chain_to_send


@node.route('/txion', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        if validate_signature(new_txion['from'], new_txion['signature'], new_txion['message']):
            NODE_PENDING_TRANSACTIONS.append(new_txion)
            print("[INFO] New transaction" +
                  "\nFROM: {0}".format(new_txion['from']) +
                  "\nTO: {0}".format(new_txion['to']) +
                  "\nAMOUNT: {0}\n".format(new_txion['amount']))
            # Then we let the client know it worked out
            return "Transaction submission successful\n"
        else:
            return "Transaction submission failed. Wrong signature\n"
    elif request.method == 'GET' and request.args.get("update") == MINER_ADDRESS:
        pending = json.dumps(NODE_PENDING_TRANSACTIONS)
        # Empty transaction list
        NODE_PENDING_TRANSACTIONS[:] = []
        return pending


def validate_signature(public_key, signature, message):
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    verif_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    try:
        return verif_key.verify(signature, message.encode())
    except:
        return False


def welcome_msg():
    print("""       =========================================\n
                     BLOCKCHAIN SYSTEM\n
       =========================================\n\n\n""")


if __name__ == '__main__':
    welcome_msg()
    # Start mining
    a, b = Pipe()
    p1 = Process(target=mine, args=(a, BLOCKCHAIN, NODE_PENDING_TRANSACTIONS))
    p1.start()
    p2 = Process(target=node.run(), args=b)
    p2.start()
