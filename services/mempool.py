from models.transaction import Transaction
from services.wallet import Wallet

class Mempool:

    def __init__(self):
        self._pending_transactions: list[bytes] = []

    def validate_transaction(self, transaction: Transaction) -> bool:
        is_signature_valid = (
            Wallet.verify_signature(
                transaction.origin_address.public_key,
                transaction.signatures[0],
                transaction
            ) and Wallet.verify_signature(
                transaction.destination_address.public_key,
                transaction.signatures[-1],
                transaction
            )
        )

        has_sufficient_funds = transaction.origin_address.amount >= transaction.amount

        return is_signature_valid and has_sufficient_funds

    def add_transaction(self, transaction: bytes) -> None:
        self._pending_transactions.append(str(transaction).encode())

    def get_pending_transactions(self) -> list[bytes]:
        return self._pending_transactions

    def clear_pending_transactions(self) -> None:
        self._pending_transactions.clear()
