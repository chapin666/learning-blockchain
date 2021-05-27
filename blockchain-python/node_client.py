from node import Node
import time
from transaction import Transaction

if __name__ == '__main__':
    node1 = Node("node1", 8001)
    node1.start()
    time.sleep(10)
    print("\n")

    node2 = Node("node2", 8002)
    node2.start()
    time.sleep(10)
    print("\n")

    # node1.print_blockchain()
    # node2.print_blockchain()

    node1.get_balance()
    node2.get_balance()

    print("\n")

    new_transaction = Transaction(
        sender=node1.wallet.address,
        recipient=node2.wallet.address,
        amount=0.3
    )
    sig = node1.wallet.sign(str(new_transaction))
    new_transaction.set_sign(sig, node1.wallet.pubkey)
    node1.submit_transaction(new_transaction)
    time.sleep(20)

    print("\n")

    node1.get_balance()
    node2.get_balance()
