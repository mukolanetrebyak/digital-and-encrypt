import random
import hashlib
import cmath
import encodings

def generate_moduls(min_bits, max_bits):
    p = 0
    g = 0
    while True:
        p = generate_bits(min_bits, max_bits)
        g = find_root(p)
        if g is not None:
            break
    return p, g

def generate_bits(min_bits, max_bits):
    while True:
        p = random.randint(2**(min_bits-1), 2**(max_bits)-1)
        if is_bit(p):
            return p

def is_bit(n, k=40):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Формула шифрування
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    #Тест k разів
    for i in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for j in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def find_root(p):
    factors = prime_factors(p-1)
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in factors):
            return g
    return None

def prime_factors(n):
    factors = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            factors.append(p)
            n //= p
        else:
            p += 1
    if n > 1:
        factors.append(n)
    return factors

def generate_keys(p, g):
    a = random.randint(1, p-1)
    b = pow(g, a, p)
    return a, b

def encrypt_block(m, p, g, b):
    k = random.randint(1, p-1)
    x = pow(g, k, p)
    y = (pow(b, k, p) * m) % p
    return x, y

def decrypt_block(x, y, p, a):
    s = pow(x, a, p)
    m = (y * modinv(s, p)) % p
    return m

def encrypt(message, p, g, b, block_size=16):
    encrypted_blocks = []
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]
        m = int.from_bytes(block.encode(), 'big')
        x, y = encrypt_block(m, p, g, b)
        encrypted_blocks.append((x, y))
    return encrypted_blocks

def decrypt(encrypted_blocks, p, a, block_size=16):
    decrypted_blocks = []
    for x, y in encrypted_blocks:
        m = decrypt_block(x, y, p, a)
        block = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
        decrypted_blocks.append(block.ljust(block_size, chr(0)))
    return ''.join(decrypted_blocks)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a