from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
import uuid
import socket

from models.transaction import Transaction

class Wallet:
    
    def __init__(self, public_key: str, amount: float):
        self.public_key = public_key
        self.amount = amount
        self.wallet_id: str = str(uuid.uuid4())
    
    @staticmethod
    def create_wallet():
        private_key = ec.generate_private_key(ec.SECP256K1())
        public_key = private_key.public_key()

        return Wallet(public_key, 0.0), private_key

    @staticmethod
    def serialize_private_key(private_key):
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    @staticmethod
    def serialize_public_key(public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def verify_signature(public_key, signature, transaction: Transaction):
        transaction_encoded = str(transaction.get_simplified_transaction()).encode()
        try:
            public_key.verify(
                signature,
                transaction_encoded,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False

    def sign_transaction(self, transaction: Transaction, private_key):
        transaction_encoded = str(transaction.get_simplified_transaction()).encode()
        return private_key.sign(
            transaction_encoded,
            ec.ECDSA(hashes.SHA256())
        )
    
    def add_credit(self, value: float) -> float:
        self.amount += value
        return self.amount
    
    def add_debit(self, value: float) -> float:
        self.amount -= value
        return self.amount

    @staticmethod
    def send_transaction(origin_wallet, destination_wallet, amount: float, node_host: str = "127.0.0.1", node_port: int= 80):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((node_host, node_port))

        transaction_to_send = Transaction(
            origin_address=origin_wallet,
            destination_address=destination_wallet,
            amount=amount
        ).get_simplified_transaction()

        server.send(str(transaction_to_send).encode())

        print(f"[send_transaction] Response : {server.recv(4096)}")
