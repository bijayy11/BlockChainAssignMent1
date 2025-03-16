import sys
import os

sys.path.append(os.path.dirname(__file__)) 

from AEShelper import *


### Single Iteration cycle for AES round operation

def encryption_round(state, round_key):
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = AddRoundKey(state, round_key)
    return state


### Last Round without Mixing Columns
def last_round(state, round_key):
    state = sub_bytes(state)
    state = shift_rows(state)
    state = AddRoundKey(state, round_key)
    return state


### AES Encryption
def AES_Encryption(Ascii_String, key):
    hex_string = ascii_to_hex(Ascii_String)
    hex_array=hex_to_decimal_array(hex_string)
    hex_array=np.array(hex_array).reshape(4,4)
    state = hex_array
    round_key = key
    for i in range(9):
        state = encryption_round(state, round_key)
    state1 = last_round(state, round_key)
    #print("Encrypted Message: ", state1.flatten())
    return decimal_array_to_hex(state1)