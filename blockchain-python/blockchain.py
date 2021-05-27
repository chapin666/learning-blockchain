
class BlockChain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def get_balance(self, user):
        balance = 0
        for block in self.blocks:
            for t in block.transactions:
                if t.sender == user.address.decode():
                    balance -= t.amount
                elif t.recipient == user.address.decode():
                    balance += t.amount
        return balance
