import sys
import os

sys.path.append(os.path.dirname(__file__)) 

from Encrypt import *
from Decrypt import *
from AEShelper import break_string_into_chunks,hex_to_decimal_array,hex_to_ascii


def Encrypt(Ascii_String,key):
    Cipher = ""
    chunks = break_string_into_chunks(Ascii_String)
    for chunk in chunks:
        cipher_text = AES_Encryption(chunk, np.array(hex_to_decimal_array(key)).reshape(4,4))
        Cipher = Cipher.join(cipher_text)
    return Cipher

def Decrypt(Cipher,key):
    Plain = ""
    chunks = break_string_into_chunks(Cipher,32)
    for chunk in chunks:
        hex_array=hex_to_decimal_array(chunk)
        hex_array=np.array(hex_array).reshape(4,4)
        plain_text = AES_Decryption(hex_array, np.array(hex_to_decimal_array(key)).reshape(4,4))
        Plain = Plain.join(plain_text)
    return hex_to_ascii(Plain)
    # return Plain

def main():
    print("Enter the message to be encrypted: ")
    message = input()
    cipher = Encrypt(message,input("Enter the key: "))
    print("Encrypted message: ", cipher)
    print("Decrypted message: ", Decrypt(cipher,input("Enter the key: ")))
    return


if __name__ == "__main__":
    main()