import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
from KeyExchange.RSA import generate_keypair, encrypt_key, decrypt_key

class TestRSAImplementation(unittest.TestCase):

    def setUp(self):
        # Set up fixed prime numbers for deterministic testing
        self.p = 61
        self.q = 53
        self.public_key, self.private_key = generate_keypair(self.p, self.q)

    def test_key_generation(self):
        # Ensure that the public and private keys are generated correctly
        self.assertEqual(len(self.public_key), 2)
        self.assertEqual(len(self.private_key), 2)
        self.assertNotEqual(self.public_key, self.private_key)

    def test_encryption_decryption(self):
        message = "HelloRSA"
        encrypted_message = encrypt_key(self.public_key, message)
        decrypted_message = decrypt_key(self.private_key, encrypted_message)

        self.assertEqual(decrypted_message, message)

    def test_single_character(self):
        message = "A"
        encrypted_message = encrypt_key(self.public_key, message)
        decrypted_message = decrypt_key(self.private_key, encrypted_message)

        self.assertEqual(decrypted_message, message)

    def test_empty_string(self):
        message = ""
        encrypted_message = encrypt_key(self.public_key, message)
        decrypted_message = decrypt_key(self.private_key, encrypted_message)

        self.assertEqual(decrypted_message, message)

if __name__ == "__main__":
    unittest.main()
