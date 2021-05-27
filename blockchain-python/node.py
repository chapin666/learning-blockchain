import socket
import pickle
import json
import hashlib
import threading
from wallet import Wallet, verify_sign
from block import Block
from pow import ProofOfWork
from blockchain import BlockChain
from transaction import Transaction


DIFFICULTY = 5
NODE_LIST = []
PER_BYTE = 1024


class Node(threading.Thread):

    def __init__(self, name, port, host="localhost"):
        threading.Thread.__init__(self, name=name)
        self.host = host
        self.port = port
        self.name = name
        self.wallet = Wallet()
        self.blockchain = None

    def run(self):
        self.init_blockchain()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        NODE_LIST.append({
            "name": self.name,
            "host": self.host,
            "port": self.port
        })
        sock.listen(10)
        print(self.name, "run...")
        while True:
            connection, address = sock.accept()
            try:
                print(self.name, "processing...")
                self.handle_request(connection)
            except socket.timeout:
                print("timeout")
            except Exception as e:
                print(e)
            connection.close()

    def handle_request(self, connection):
        data = []
        while True:
            buf = connection.recv(PER_BYTE)
            if not buf:
                break
            data.append(buf)
            if len(buf) < PER_BYTE:
                break
        t = pickle.loads(b''.join(data))
        if isinstance(t, Transaction):
            print("process transaction request...")
            if verify_sign(t.pubkey, str(t), t.signature):
                print(self.name, " transaction check success")
                new_block = Block(transactions=[t], prev_hash="")
                print(self.name, " generate new block...")
                w = ProofOfWork(new_block, self.wallet)
                block = w.mine()
                print(self.name, " add new_block to blockchain")
                self.blockchain.add_block(block)
                print(self.name, " broadcast")
                self.broadcast_new_block(block)
            else:
                print(self.name, " transaction check failed")
        elif isinstance(t, Block):
            print("process block request...")
            if self.verify_block(t):
                print(self.name, " block check success")
                self.blockchain.add_block(t)
                print(self.name, " add block success")
            else:
                print(self.name, " block check failed")
        else:
            print("init request")
            connection.send(pickle.dumps(self.blockchain))

    def init_blockchain(self):
        if NODE_LIST:
            host = NODE_LIST[0]['host']
            port = NODE_LIST[0]['port']
            name = NODE_LIST[0]['name']
            print(self.name, "send init requests %s" % name)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.send(pickle.dumps('INIT'))
            data = []
            while True:
                buf = sock.recv(PER_BYTE)
                if not buf:
                    break
                data.append(buf)
                if len(buf) < PER_BYTE:
                    break
            sock.close()

            self.blockchain = pickle.loads(b''.join(data))
            print(self.name, "init finished")
        else:
            block = Block(transactions=[], prev_hash="")
            w = ProofOfWork(block, self.wallet)
            genesis_block = w.mine()
            self.blockchain = BlockChain()
            self.blockchain.add_block(genesis_block)
            print("genesis created")

    def broadcast_new_block(self, block):
        for node in NODE_LIST:
            host = node['host']
            port = node['port']
            if host != self.host or port != self.port:
                print(self.name, "broadcast to %s" % node['name'])
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                sock.send(pickle.dumps(block))
                sock.close()

    def submit_transaction(self, transaction):
        for node in NODE_LIST:
            host = node['host']
            port = node['port']
            if host != self.host or port != self.port:
                print(self.name, "broadcast to %s:%s" % (self.host, self.port))
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((node["host"], node["port"]))
                sock.send(pickle.dumps(transaction))
                sock.close()

    def get_balance(self):
        balance = 0
        for block in self.blockchain.blocks:
            for t in block.transactions:
                if t.sender == self.wallet.address.decode():
                    balance -= t.amount
                elif t.recipient == self.wallet.address.decode():
                    balance += t.amount
        print(self.name, "当前拥有%.1f个加密货币" % balance)

    def print_blockchain(self):
        if self.blockchain:
            print("blockchain size ：%d\n" % len(self.blockchain.blocks))
            for block in self.blockchain.blocks:
                print("prev hash: %s" % block.prev_hash)
                print("data: %s" % block.transactions)
                print("hash: %s" % block.hash)
                print("\n")

    @staticmethod
    def verify_block(block):
        message = hashlib.sha256()
        message.update(str(block.prev_hash).encode("utf-8"))
        message.update(str(block.transactions).encode("utf-8"))
        message.update(str(block.timestamp).encode("utf-8"))
        message.update(str(block.nonce).encode("utf-8"))
        digest = message.hexdigest()
        prefix = '0' * DIFFICULTY
        return digest.startswith(prefix)
