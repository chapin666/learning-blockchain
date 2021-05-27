import hashlib
import json
from transaction import Transaction, TransactionEncoder


class ProofOfWork:
    def __init__(self, block, miner, difficult=5):
        self.block = block
        self.difficulty = difficult
        self.miner = miner
        self.reward_amount = 1

    def mine(self):
        i = 0
        prefix = '0' * self.difficulty

        t = Transaction(
            sender="",
            recipient=self.miner.address,
            amount=self.reward_amount,
        )
        sig = self.miner.sign(json.dumps(t, cls=TransactionEncoder))
        t.set_sign(sig, self.miner.pubkey)
        self.block.transactions.append(t)

        while True:
            message = hashlib.sha256()
            message.update(str(self.block.prev_hash).encode("utf-8"))
            message.update(str(self.block.transactions).encode('utf-8'))
            message.update(str(self.block.timestamp).encode("utf-8"))
            message.update(str(i).encode("utf-8"))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                self.block.nonce = i
                self.block.hash = digest
                return self.block
            i += 1
