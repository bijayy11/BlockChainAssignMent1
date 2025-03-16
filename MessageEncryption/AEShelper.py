import numpy as np

### Conversion of Hex to Ascii
def hex_to_ascii(hex_string):
    """
    Convert a hexadecimal string to an ASCII string character by character.
    
    :param hex_string: A string containing hexadecimal values
    :return: The corresponding ASCII string
    """
    if len(hex_string) % 2 != 0:
        return "Invalid hex input: Length should be even"

    try:
        ascii_string = ""
        for i in range(0, len(hex_string), 2):
            hex_pair = hex_string[i:i+2]  # Take two hex characters
            ascii_char = chr(int(hex_pair, 16))  # Convert to integer, then to ASCII char
            ascii_string += ascii_char  # Append to result
        
        return ascii_string
    except ValueError:
        return "Invalid hex input: Contains non-hex characters"


### Conversion of Ascii String to Hex string
def ascii_to_hex(ascii_string):
    # Convert each character to its hexadecimal representation
    hex_string = ''.join(format(ord(c), '02x') for c in ascii_string)
    return hex_string

## Break Ascii/Hex String in byte chunks
def break_string_into_chunks(ascii_string, chunk_size=16):
    # Pad the string with spaces if its length is not a perfect multiple of chunk_size
    if len(ascii_string) % chunk_size != 0:
        ascii_string = ascii_string.ljust((len(ascii_string) // chunk_size + 1) * chunk_size)

    # Break the string into chunks of the specified size
    chunks = [ascii_string[i:i+chunk_size] for i in range(0, len(ascii_string), chunk_size)]
    
    return chunks

### Conversion from hexadecimal string to decimal square 2 dimenstional array
def hex_to_decimal_array(hex_string):
    # Split the hex string into pairs of two characters
    hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    # Convert each hex pair to a decimal number
    decimal_array = [int(pair, 16) for pair in hex_pairs]
    return decimal_array


### Conversion from square 2 dimensional array to flat hexadecimal string

def decimal_array_to_hex(decimal_array):
    # Flatten the 2D array to a 1D array
    flat_array = np.array(decimal_array).flatten()
    # Convert each decimal number to a 2-character hexadecimal string
    hex_array = [format(decimal, '02x') for decimal in flat_array]
    # Join all hexadecimal strings into a single string
    hex_string = ''.join(hex_array)
    return hex_string

#### Define a predefined array for Mix Column Operation during each iteration of encryption in AES encryption process

predefined_array = np.array([[2,3,1,1],
                              [1,2,3,1],
                              [1,1,2,3],
                              [3,1,1,2]])
predefined_array.shape


#### Define byte Substitute matrix for lookup and substitution

s_box = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

## Convert the s_box list to a 2D array for easy lookup
s_box_2d = np.array(s_box).reshape(16, 16)

### Substitution operation based on Rijndael S-Box Mapping

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            row = state[i][j] // 16
            col = state[i][j] % 16
            state[i][j] = s_box_2d[row][col]
    return state

### Shift Rows
def shift_rows(state):
    for i in range(4):
        state[i] = np.roll(state[i], -i)
    return state

### Mix Columns

def gf_mult(a, b):
    """Multiply two numbers in GF(2^8) using the AES irreducible polynomial."""
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11b  # AES irreducible polynomial (x^8 + x^4 + x^3 + x + 1)
        b >>= 1
    return result

def mix_column(col):
    """Apply the MixColumns transformation on a single column."""
    # AES MixColumns matrix
    mix_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]
    
    # To hold the result of the mix
    result = [0] * 4
    
    # Matrix multiplication in GF(2^8)
    for i in range(4):
        result[i] = 0
        for j in range(4):
            result[i] ^= gf_mult(mix_matrix[i][j], col[j])
    
    return result

def mix_columns(state):
    """Apply the MixColumns operation to a 4x4 state matrix in decimal."""
    mixed_state = []
    
    # For each column, apply the MixColumns transformation
    for col in range(4):
        column = [state[row][col] for row in range(4)]  # Extract the column
        mixed_column = mix_column(column)  # Mix the column
        mixed_state.append(mixed_column)  # Store the mixed column
    
    # Return the 4x4 mixed state
    return [[mixed_state[row][col] for row in range(4)] for col in range(4)]


### ADD ( bit wise ( each byte) X-OR)
def AddRoundKey(state, round_key):
    return state ^ round_key

