# Client Server Encrypted Communication

## Requirements

Make sure you have Python installed. You can check by running:

```sh
python --version
```

You also need `pip` installed to manage dependencies:

```sh
pip --version
```

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/bijayy11/BlockChainAssignMent1.git
   cd NEW
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Running the Server

Run the FastAPI server using Uvicorn:

```sh
cd Messaging
run python3 Server.py
```

## Run Client Side
### Open a new Terminal
 ```sh
 cd NEW/Messaging
 run python3 client.py
```
### After sending messages, head over to
```sh
localhost:8000/send
```
### to see message encrypted on server side
## Test Cases

```sh
cd ../TestCases
python3 run Test_AES.py ## to unit test AES implementation
python3 run Test_RSA.py ## to unit test RSA implementation
pytest -v ## to test Server-Client Implementation
```

