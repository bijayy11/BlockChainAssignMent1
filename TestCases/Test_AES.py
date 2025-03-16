
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from MessageEncryption.AES_Implementation import Encrypt, Decrypt

class TestAESImplementation(unittest.TestCase):

    def test_encryption_decryption(self):
        # Test with a sample message and key
        message = "Hello! World!!!!"
        key = "9dd7b1882e3c10e7e4b586adbad03fc1"  # Example 16-byte hex key
        
        # Encrypt the message
        encrypted_message = Encrypt(message, key)
        
        # Decrypt the message
        decrypted_message = Decrypt(encrypted_message, key)
        
        # Check if the decrypted message matches the original
        self.assertEqual(decrypted_message, message)

    def test_empty_string(self):
        # Test with an empty message
        message = ""
        key = "aabbccddeeff00112233445566778899"  # Example hex key

        encrypted_message = Encrypt(message, key)
        decrypted_message = Decrypt(encrypted_message, key)

        self.assertEqual(decrypted_message, message)


    

if __name__ == "__main__":
    unittest.main()
