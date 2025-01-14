from dataclasses import dataclass
from typing import Type, Tuple, Optional


@dataclass
class Transaction:
    origin_address: Type
    destination_address: Type
    amount: float
    signatures: Optional[Tuple[bytes, bytes]] = None

    def get_simplified_transaction(self):
        return {
            "origin_address": self.origin_address.wallet_id,
            "destination_address": self.destination_address.wallet_id,
            "amount": self.amount,
        }
