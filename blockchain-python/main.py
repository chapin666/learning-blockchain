
from block import Block
from blockchain import BlockChain
from pow import ProofOfWork
from wallet import Wallet, verify_sign
from transaction import Transaction

if __name__ == '__main__':

    blockchain = BlockChain()

    alice = Wallet()
    tom = Wallet()
    bob = Wallet()

    # genesis
    new_block1 = Block(transactions=[], prev_hash="")
    w1 = ProofOfWork(new_block1, alice)
    new_block = w1.mine()
    blockchain.add_block(new_block)

    # transfer
    new_transaction = Transaction(
        sender=alice.address,
        recipient=tom.address,
        amount=0.3
    )
    sig = tom.sign(str(new_transaction))
    new_transaction.set_sign(sig, tom.pubkey)

    # mine
    if verify_sign(new_transaction.pubkey, str(new_transaction), new_transaction.signature):
        new_block2 = Block(transactions=[new_transaction], prev_hash="")
        w2 = ProofOfWork(new_block2, bob)
        block = w2.mine()
        blockchain.add_block(block)
    else:
        print("transaction failed!!!")

    # print
    print(blockchain.get_balance(alice))
    print(blockchain.get_balance(tom))
    print(blockchain.get_balance(bob))




