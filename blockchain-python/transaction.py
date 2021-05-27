
import json


class Transaction:
    def __init__(self, sender, recipient, amount):
        if isinstance(sender, bytes):
            sender = sender.decode("utf-8")
        self.sender = sender
        if isinstance(recipient, bytes):
            recipient = recipient.decode("utf-8")
        self.recipient = recipient
        self.amount = amount

    def set_sign(self, signature, pubkey):
        self.signature = signature
        self.pubkey = pubkey

    def __repr__(self):
        if self.sender:
            s = "from %s transfer %d btc to %s" % (self.sender, self.amount, self.recipient)
        else:
            s = "%s get %d btc by mine" % (self.recipient, self.amount)
        return s


class TransactionEncoder(json.JSONEncoder):
    """
    定义Json的编码类，用来序列化Transaction
    """
    def default(self, obj):
        if isinstance(obj, Transaction):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)