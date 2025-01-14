# POC-Blockchain-Python

Este projeto é uma Prova de Conceito (POC) de uma Blockchain simplificada implementada em Python. Ele demonstra conceitos básicos de blockchain, como transações, mineração de blocos e comunicação entre nós (nodes) de forma descentralizada.

## Estrutura do Projeto

```plaintext
POC-BLOCKCHAIN-PYTHON/
├── env/                     # Ambiente virtual do Python
├── models/                  # Contém os modelos de dados
│   ├── __init__.py
│   ├── transaction.py       # Implementação do modelo de transação
├── services/                # Serviços principais do blockchain
│   ├── __init__.py
│   ├── block.py             # Implementação do modelo de bloco
│   ├── blockchain.py        # Lógica da blockchain
│   ├── mempool.py           # Gerenciamento do mempool (transações pendentes)
│   ├── node.py              # Implementação de um nó da rede
│   ├── wallet.py            # Implementação de carteiras digitais
├── main.py                  # Exemplo principal para execução do sistema
```

## Funcionalidades

- **Carteiras Digitais**: Cada carteira possui uma chave privada para assinar transações.
- **Transações**: Criação e autenticação de transações entre carteiras.
- **Nodes e Blockchain**: Simula uma rede descentralizada de blockchain com múltiplos nós.
- **Mineração**: Os nós podem minerar blocos para adicionar transações à blockchain.
- **Comunicação P2P**: Comunicação entre os nós para troca de transações e blocos.

## Exemplo de Uso

O arquivo `main.py` demonstra o uso básico do sistema. Abaixo estão os principais passos:

1. **Criação de Carteiras**:
   ```python
   wallet1, private_key1 = Wallet.create_wallet()
   wallet2, private_key2 = Wallet.create_wallet()

   wallet1.add_credit(100.0)
   wallet2.add_credit(500.0)
   ```

2. **Criação e Assinatura de Transação**:
   ```python
   transaction = Transaction(
       origin_address=wallet1,
       destination_address=wallet2,
       amount=60.0
   )

   signature_wallet1 = wallet1.sign_transaction(transaction, private_key1)
   signature_wallet2 = wallet2.sign_transaction(transaction, private_key2)
   transaction.signatures = (signature_wallet1, signature_wallet2)
   ```

3. **Configuração dos Nós**:
   ```python
   from services.node import Node
   from services.mempool import Mempool

   node = Node(0, 1, Mempool(), peers_transactions=["127.0.0.1:70"], peers_blocks=["127.0.0.1:90"])
   node2 = Node(1, 1, Mempool(), transactions_port=70)
   ```

4. **Execução em Threads**:
   ```python
   import threading

   # Inicialização de threads para os nós
   t0 = threading.Thread(target=node2.listen_to_transactions)
   t0.start()
   t1 = threading.Thread(target=node.listen_to_transactions)
   t1.start()

   t2 = threading.Thread(target=node.mine_block)
   t2.start()

   t3 = threading.Thread(target=node2.listen_to_new_blocks)
   t3.start()
   ```

5. **Envio de Transação**:
   ```python
   Wallet.send_transaction(origin_wallet=wallet1, destination_wallet=wallet2, amount=transaction.amount)
   ```

## Dependências

- Python 3.8+
- Biblioteca cryptography
- Biblioteca padrão do Python

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/poc-blockchain-python.git
   cd poc-blockchain-python
   ```

2. Configure o ambiente virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/MacOS
   env\Scripts\activate     # Windows
   ```

3. Instale as dependências (se necessário).

4. Execute o exemplo principal:
   ```bash
   python main.py
   ```

## Autor

Este projeto foi desenvolvido como uma demonstração de conceitos de blockchain. Modificações e melhorias são bem-vindas!

---

**Nota**: Este é apenas um exemplo para uso educacional e não deve ser utilizado em sistemas de produção sem ajustes e aprimoramentos.
