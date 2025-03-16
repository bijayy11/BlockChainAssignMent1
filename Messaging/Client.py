import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from MessageEncryption.AES_Implementation import Encrypt
from KeyExchange.RSA import encrypt_key
import secrets
from dotenv import load_dotenv


SERVER_URL = "http://127.0.0.1:8000"
load_dotenv()

def send_message(sender, content):
    load_dotenv()
    aes_key = os.getenv("AES_KEY")

    if not aes_key:
        print("Error: AES_KEY is not set in the environment.")
        return

    encrypted_sender = Encrypt(sender, aes_key)
    encrypted_content = Encrypt(content, aes_key)

    response = requests.post(f"{SERVER_URL}/send", json={
        "sender": encrypted_sender,
        "content": encrypted_content
    })

    print("Server Response:", response.json())

def get_public_key():
    try:
        response = requests.post(f"{SERVER_URL}/sendkeys")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")  

        if response.status_code == 200 and "public_key" in response.json():
            return tuple(response.json()["public_key"])
        else:
            print("Error: 'public_key' not found in response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def encrypt_aes_key(aes_key, public_key):
    encrypted_key = encrypt_key(public_key,aes_key)

    if not encrypted_key:
        print("Error: Encryption failed, AES key is empty!")
        return None

    # encrypted_key_str = ",".join(map(str, encrypted_key))  # Convert list to string
    print(f"Encrypted AES Key (Before Sending): {encrypted_key}")
    
    return encrypted_key

def send_aes_key(aes_key):
    public_key = get_public_key()
    if not public_key:
        print("Error: Public key retrieval failed.")
        return None

    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)
    if not encrypted_aes_key:
        return None

    response = requests.post(f"{SERVER_URL}/decrypt-Key", json={"AES_Key": encrypted_aes_key})
    
    try:
        response_json = response.json()
        print("Server Response:", response_json)
        return response_json.get("AES_Key")
    except requests.exceptions.JSONDecodeError:
        print("Error: Failed to decode JSON response.")
        return None

def main():
    aes_key = secrets.token_hex(16)
    print("AES Key Before Encryption: ",aes_key)
    send_aes_key(aes_key)
    send_message(input("Enter your name: "), input("Enter your message: "))

if __name__ == "__main__":
    main()
