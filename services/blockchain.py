from services.block import Block
from models.transaction import Transaction


class BlockChain:

    def __init__(self):
        self.blocks: list[Block] = [self.create_genesis_block()]

    @property
    def most_recent_block(self):
        return self.blocks[-1]

    def create_genesis_block(self) -> Block:
        return Block(0, "0")

    def add_new_block(self, block: Block):
        self.blocks.append(
            block
        )
