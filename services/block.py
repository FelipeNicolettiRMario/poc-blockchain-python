import time
from hashlib import sha256

class Block:

    def __init__(self, previous_hash: str, nonce: int, transactions: list[bytes] = None):
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.transactions: list[bytes] = transactions if transactions is not None else []
        self.timestamp: int = int(time.time())

    @property
    def hash(self) -> str:
        content_to_hash = f"{self.previous_hash}{self.transactions}{self.nonce}"
        return sha256(content_to_hash.encode()).hexdigest()

    def add_transaction(self, transaction: bytes) -> None:
        self.transactions.append(transaction)

    def add_transactions(self, transactions: list[bytes]) -> None:
        self.transactions.extend(transactions)
