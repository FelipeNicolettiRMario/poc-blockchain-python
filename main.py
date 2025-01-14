from services.wallet import Wallet
from models.transaction import Transaction

## Criação de carteiras, gerando uma chave privada para cada carteira
wallet1, private_key1 = Wallet.create_wallet()
wallet2, private_key2 = Wallet.create_wallet()

wallet1.add_credit(100.0)
wallet2.add_credit(500.0)

## Criação de uma transação simulada
transaction = Transaction(
    origin_address=wallet1,
    destination_address=wallet2,
    amount=60.0
)

## Carteiras assinando a transação para garantir a autenticidade da mesma
signature_wallet1 = wallet1.sign_transaction(transaction, private_key1)
signature_wallet2 = wallet2.sign_transaction(transaction, private_key2)
transaction.signatures = (signature_wallet1, signature_wallet2)

# Criação de dois nodes que serão utilizados para simular uma blockchain descentralizada
# O node 2 vai ser um dos peers para o Node 1

from services.mempool import Mempool
from services.node import Node

node = Node(0, 1, Mempool(), peers_transactions=["127.0.0.1:70"], peers_blocks=["127.0.0.1:90"])
node2 = Node(1, 1, Mempool(), transactions_port=70)

import threading

# Essas duas primeiras threads ouvirão todas as transações que chegarem a algum dos nodes
t0 = threading.Thread(target=node2.listen_to_transactions)
t0.start()
t1 = threading.Thread(target=node.listen_to_transactions)
t1.start()

## Essa threads ficará responsável por minerar utilizando o node 1
t2 = threading.Thread(target=node.mine_block)
t2.start()

## Essa thread vai ficar ouvindo os novos blocos que serão propagados através de um node
t3 = threading.Thread(target=node2.listen_to_new_blocks)
t3.start()

## Esse método vai enviar uma transação via rede para o node 1 (o endereço do node é parametrizável)
Wallet.send_transaction(origin_wallet=wallet1, destination_wallet=wallet2, amount=transaction.amount)
