import time

from models.transaction import Transaction
from hashlib import sha256

class Block:

    def __init__(self, previous_hash: str, nonce: int, transactions: list[bytes] = []):
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.transactions: list[bytes] = transactions
        self.timestamp: int = time.time()

    @property
    def hash(self):
        content_to_hash = f"{self.previous_hash}{self.transactions}{self.nonce}"
        return sha256(content_to_hash.encode()).hexdigest()

    def add_transaction(self, transaction: bytes):
        self.transactions.append(transaction)

    def add_transactions(self, transactions: bytes):
        self.transactions.extend(transactions)
