from services.block import Block
from models.transaction import Transaction

class BlockChain:

    def __init__(self):
        self.blocks: list[Block] = [self._create_genesis_block()]

    @property
    def most_recent_block(self) -> Block:
        return self.blocks[-1]

    def _create_genesis_block(self) -> Block:
        return Block(previous_hash="0", nonce=0)

    def add_new_block(self, block: Block) -> None:
        self.blocks.append(block)
