import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt_key(public_key, plaintext):
    e, n = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in plaintext]
    return encrypted_msg

def decrypt_key(private_key, ciphertext):
    d, n = private_key
    decrypted_msg = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(decrypted_msg)

    # Example
if __name__ == '__main__':
    p = 61
    q = 53
    public_key, private_key = generate_keypair(p, q)
    plaintext = [2755, 2869, 1092, 629, 2932, 3006, 629, 2932, 2056, 629]
    #encrypted_msg = encrypt_key(public_key, plaintext)
    decrypted_msg = decrypt_key(private_key, plaintext)

    print("Public Key:", public_key)
    print("Private Key:", private_key)
    #print("Encrypted Message:", encrypted_msg)
    print("Decrypted Message:", decrypted_msg)