
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError
import binascii
import base64
from hashlib import sha256


class Wallet:
    def __init__(self):
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._public_key = self._private_key.get_verifying_key()

    def sign(self, message):
        h = sha256(message.encode('utf8'))
        return binascii.hexlify(self._private_key.sign(h.digest()))

    @property
    def address(self):
        h = sha256(self._public_key.to_pem())
        return base64.b64encode(h.digest())

    @property
    def pubkey(self):
        return self._public_key.to_pem()


def verify_sign(pubkey, message, signature):
    verifier = VerifyingKey.from_pem(pubkey)
    h = sha256(message.encode("utf8"))
    return verifier.verify(binascii.unhexlify(signature), h.digest())
