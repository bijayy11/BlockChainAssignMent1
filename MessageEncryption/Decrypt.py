import sys
import os

sys.path.append(os.path.dirname(__file__)) 

from AEShelper import *

def inv_sub_bytes(state):
    inv_s_box = [s_box.index(x) for x in range(256)]
    inv_s_box_2d = np.array(inv_s_box).reshape(16, 16)
    for i in range(4):
        for j in range(4):
            row = state[i][j] // 16
            col = state[i][j] % 16
            state[i][j] = inv_s_box_2d[row][col]
    return state

def inv_shift_rows(state):
    for i in range(4):
        state[i] = np.roll(state[i], i)
    return state

def inverse_mix_column(col):
    """Apply the Inverse MixColumns transformation on a single column."""
    # AES Inverse MixColumns matrix
    inverse_mix_matrix = [
        [0x0E, 0x0B, 0x0D, 0x09],
        [0x09, 0x0E, 0x0B, 0x0D],
        [0x0D, 0x09, 0x0E, 0x0B],
        [0x0B, 0x0D, 0x09, 0x0E]
    ]
    
    # To hold the result of the mix
    result = [0] * 4
    
    # Matrix multiplication in GF(2^8)
    for i in range(4):
        result[i] = 0
        for j in range(4):
            result[i] ^= gf_mult(inverse_mix_matrix[i][j], col[j])
    
    return result

def aes_inverse_mix_columns(state):
    """Apply the Inverse MixColumns operation to a 4x4 state matrix in decimal."""
    mixed_state = []
    
    # For each column, apply the Inverse MixColumns transformation
    for col in range(4):
        column = [state[row][col] for row in range(4)]  # Extract the column
        mixed_column = inverse_mix_column(column)  # Apply inverse mix
        mixed_state.append(mixed_column)  # Store the mixed column
    
    # Return the 4x4 mixed state
    return [[mixed_state[row][col] for row in range(4)] for col in range(4)]

def inv_add_round_key(state, round_key):
    return state ^ round_key

def decryption_round(state, round_key):
    state = inv_add_round_key(state, round_key)
    state = aes_inverse_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    return state

def last_decryption_round(state, round_key):
    state = inv_add_round_key(state, round_key)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    return state

def AES_Decryption(cipher_array, key):
    state = cipher_array
    round_key = key
    state = last_decryption_round(state, round_key)
    for i in range(9):
        state = decryption_round(state, round_key)
    return decimal_array_to_hex(state)