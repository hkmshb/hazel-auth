"""The default password hashing implementation using Argon 2.

Argon 2 is the winner algorithm of Password Hashing Competition 2012-2015
  * https://password-hashing.net/
"""
import argon2
from zope.interface import implementer
from .interfaces import IPasswordHasher



@implementer(IPasswordHasher)
class Argon2Hasher:
    """The default password hashing implementation using Argon 2.
    """

    def __init__(self):
        self._hasher = argon2.PasswordHasher()

    def hash_password(self, plain_text):
        """Generate a hash presentation for the provided plain text password.
        """
        return self._hasher.hash(plain_text)

    def verify_password(self, plain_text, hashed_password):
        """Verify a password. Hashes provided plain_text and compares it to
        the persisted hash.
        """
        try:
            self._hasher.verify(hashed_password, plain_text)
            return True
        except (
            argon2.exceptions.VerifyMismatchError,
            argon2.exceptions.VerificationError
        ):
            return False
