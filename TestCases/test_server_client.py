import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import requests
import secrets
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from Messaging.Server import app
from MessageEncryption.AES_Implementation import Encrypt, Decrypt
from KeyExchange.RSA import encrypt_key, decrypt_key

# Load environment variables
load_dotenv()

# Constants
SERVER_URL = "http://127.0.0.1:8000"

# Initialize test client
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_env_keys():
    """Generate and set up RSA keys before running tests."""
    os.system("python server.py")  # Ensure keys are generated

@pytest.fixture
def generate_aes_key():
    """Generate a random AES key for testing."""
    return secrets.token_hex(16)

@pytest.fixture
def get_public_key():
    """Fetch the public key from the server."""
    response = client.post("/sendkeys")
    assert response.status_code == 200
    json_data = response.json()
    assert "public_key" in json_data
    return tuple(json_data["public_key"])

def test_encrypt_decrypt_message(generate_aes_key):
    """Test AES encryption and decryption."""
    aes_key = generate_aes_key
    message = "Hello! World!!!!"

    encrypted_message = Encrypt(message, aes_key)
    decrypted_message = Decrypt(encrypted_message, aes_key)

    assert decrypted_message == message

def test_rsa_encryption_decryption(get_public_key):
    """Test RSA encryption and decryption of AES key."""
    public_key = get_public_key
    aes_key = secrets.token_hex(16)

    encrypted_aes_key = encrypt_key(public_key, aes_key)
    private_key = tuple(map(int, os.getenv("PRIVATE_KEY").split(",")))

    decrypted_aes_key = decrypt_key(private_key, encrypted_aes_key)

    assert decrypted_aes_key == aes_key

def test_send_encrypted_aes_key(generate_aes_key, get_public_key):
    """Test sending the encrypted AES key to the server."""
    public_key = get_public_key  
    aes_key = generate_aes_key
    encrypted_aes_key = encrypt_key(public_key, aes_key)
    
    response = client.post("/decrypt-Key", json={"AES_Key": encrypted_aes_key})
    assert response.status_code == 200
    assert "response" in response.json()
    assert "Server received and stored AES Key successfully." in response.json()["response"]



def test_send_message(generate_aes_key):
    """Test sending an encrypted message to the server."""
    load_dotenv()
    aes_key = os.getenv("AES_KEY")

    if not aes_key or len(aes_key) != 32:
        pytest.fail(f"AES key is missing or has an incorrect format: {aes_key}")

    encrypted_sender = Encrypt("Alice", aes_key)
    encrypted_content = Encrypt("Hello, Bob!", aes_key)

    response = client.post("/send", json={
        "sender": encrypted_sender,
        "content": encrypted_content
    })

    assert response.status_code == 200
    assert "response" in response.json()



def test_receive_decrypted_message():
    """Test receiving and decrypting the last sent message."""
    test_send_message(secrets.token_hex(16))

    response = client.get("/send")
    
    assert response.status_code == 200
    json_data = response.json()

    assert "header" in json_data
    assert "Content" in json_data
    assert "from" in json_data
    assert json_data["header"] == "Decrypted at Server:"
