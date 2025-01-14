from services.block import Block
from services.mempool import Mempool
from services.blockchain import BlockChain

from hashlib import sha256
import socket
import threading
import json

class Node:

    def __init__(self, node_id, difficulty: int, mempool: Mempool, peers_transactions: dict[str] = [], peers_blocks: dict[str] = [], transactions_port: int = 80, new_blocks_port: int = 90):
        self.node_id = node_id
        self.difficulty = difficulty
        self.mempool = mempool
        self.peers_transactions = peers_transactions
        self.peers_blocks = peers_blocks

        self.blockchain = BlockChain()

        self.host = "127.0.0.1"
        self.transactions_port = transactions_port
        self.new_blocks_port = new_blocks_port

    def _propagate_data_to_peers(self, data: bytes, peers: list[str]):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for peer in peers:
            host, port = peer.split(":")
            try:
                server.connect((host, int(port)))
                server.send(data)
            except:
                print(f"[Node {self.node_id}][_propagate_data_to_peers] Data could not be propagated to peer {peer}")
    
    def _init_network_listener(self, port: int, data_callback):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, port))
        server.listen(5)

        while True:
            client, addr = server.accept()
            print(f"[Node {self.node_id}][_init_network_listener] Accepted connection from: {addr[0]}:{addr[1]}")
            client_handler  = threading.Thread(target=data_callback, args=(client,))
            client_handler.start()

    def listen_to_transactions(self):
        self._init_network_listener(self.transactions_port, self._store_transaction)

    def _store_transaction(self, client_socket):
        request = client_socket.recv(1024)
        print(f"[Node {self.node_id}][_store_transaction] Received transaction: {request}")
        
        self.mempool.add_transaction(request)
        self._propagate_transactions_to_peers(request)
        client_socket.send("Transaction received by node".encode())
        client_socket.close()

    def _propagate_transactions_to_peers(self, transaction: bytes):
        self._propagate_data_to_peers(transaction, self.peers_transactions)
        print(f"[Node {self.node_id}][_propagate_transactions_to_peers] Transaction {transaction} propagated to peers")

    def mine_block(self):
        nonce = 0
        while True:
            transactions = self.mempool.get_pending_transactions()

            if transactions:
                previous_hash = self.blockchain.most_recent_block.hash
                prefix = "0" * self.difficulty
        
                content = f"{previous_hash}{transactions}{nonce}"
                block_hash = sha256(content.encode()).hexdigest()
                
                if block_hash.startswith(prefix):
                    new_block = Block(previous_hash, nonce)
                    new_block.add_transactions(transactions)
                    self.blockchain.add_new_block(new_block)
                    self._propagate_new_block(new_block)
                    self.mempool.clear_pending_transactions()
                
                nonce += 1

    def _propagate_new_block(self, new_block: Block):
        block_data_to_send = str({"previous_hash": new_block.previous_hash, "nonce": new_block.nonce}).encode()
        self._propagate_data_to_peers(block_data_to_send, self.peers_blocks)
        print(f"[Node {self.node_id}][_propagate_new_block] Block {block_data_to_send} propagated to peers")

    def listen_to_new_blocks(self):
        self._init_network_listener(self.new_blocks_port, self._add_received_new_block)

    def _add_received_new_block(self, client_socket):
        request = client_socket.recv(1024)
        print(f"[Node {self.node_id}][_add_received_new_block] Received block: {request}")
        
        new_block_data = json.loads(
            request.decode("utf-8").replace("'", '"')
        )
        new_block = Block(
            previous_hash=new_block_data.get("previous_hash"),
            nonce=new_block_data.get("nonce"),
        )
        self.blockchain.add_new_block(new_block)

        client_socket.send("Transaction received by node".encode())
        client_socket.close()
