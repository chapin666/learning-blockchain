

from datetime import datetime
import json


class Block:
    def __init__(self, transactions, prev_hash):
        self.prev_hash = prev_hash
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions = transactions
        self.nonce = None
        self.hash = None

    def __repr__(self):
        return "data: %s \n hash: %s" % (json.dumps(self.transactions), self.hash)
