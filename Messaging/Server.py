import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from MessageEncryption.AES_Implementation import Decrypt
from KeyExchange.RSA import generate_keypair, decrypt_key
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class Message(BaseModel):
    sender: str
    content: str

class AES_Key(BaseModel):
    AES_Key: list[int]  # Ensure this matches the client-side data type

last_message = {"sender": "", "content": ""}

last_message = {"sender": "", "content": ""}  # Initialize last message storage

@app.post("/send")
def receive_message(msg: Message):
    global last_message
    last_message = {"sender": msg.sender, "content": msg.content}
    response_content = f"Server received: {msg.content} from {msg.sender}"
    return {"response": response_content}

@app.get("/send")
def printmessages():
    if not last_message["sender"]:
        return {"error": "No message has been sent yet."}
    
    try:
        load_dotenv()
        
        decrypted_content = Decrypt(last_message["content"], (os.getenv("AES_KEY")))
        decrypted_sender = Decrypt(last_message["sender"], (os.getenv("AES_KEY")))
    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}
    
    return {
        "header": "Decrypted at Server:",
        "Content": decrypted_content,
        "from": decrypted_sender
    }

def get_keys():
    p, q = 61, 53  # Prime numbers for RSA
    public_key, private_key = generate_keypair(p, q)
    
    env_file = ".env"
    if not os.path.exists(env_file):
        open(env_file, "w").close()

    # Write keys to .env file
    with open(env_file, "w") as f:
        f.write(f"PUBLIC_KEY={public_key[0]},{public_key[1]}\n")
        f.write(f"PRIVATE_KEY={private_key[0]},{private_key[1]}\n")

    print("Keys successfully written to .env file.")

@app.post("/sendkeys")
def send_public_key():
    load_dotenv()
    public_key_str = os.getenv("PUBLIC_KEY")

    if not public_key_str:
        return {"error": "Public key not found."}

    try:
        public_key = tuple(map(int, public_key_str.split(",")))
        return {"public_key": public_key}
    except ValueError:
        return {"error": "Invalid public key format."}

@app.post('/decrypt-Key')
def Decrypt_AES_Key(aes_key: AES_Key):
    print(f"Received AES_Key: {aes_key.AES_Key}")  # Debugging

    if not aes_key.AES_Key:
        return {"error": "AES Key received is empty!"}

    private_key_str = os.getenv("PRIVATE_KEY")

    if not private_key_str:
        return {"error": "Private key not found."}

    try:
        private_key = tuple(map(int, private_key_str.split(",")))

        decrypted_aes_key = decrypt_key(private_key, aes_key.AES_Key)

        with open(".env", "a") as f:  # Append instead of overwrite
            f.write(f'AES_KEY="{decrypted_aes_key}"\n')  # Ensure it is written inside quotes


        return {"response": "Server received and stored AES Key successfully."}
    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}


@app.get("/")
def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    get_keys()
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
