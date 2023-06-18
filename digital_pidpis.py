import random
from hashlib import sha1

# Генеруємо випадкові числа
def generate_numbers(nbits):
    p = 1
    while len(bin(p)) != nbits + 2:
        p = random.randint(2**(nbits-1), 2**nbits - 1)
        while not is_simple(p):
            p += 1
    return p

# Перевірямо чи прості числа 
def is_simple(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

# Знаходимо обренені елементи у скінченному колі 
def modinv(a, m):
    g, x, y = gcd_extended(a, m)
    if g != 1:
        raise Exception('Неможливо знайти обернений елемент')
    return x % m

# алгоритм Евкліда
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Генерація ключів
def generate_keys(nbits):
    p = generate_numbers(nbits)
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)
    y = pow(g, x, p)
    return p, g, x, y

# Функція гешування повідомлення
def hash_message(message):
    return int(sha1(message.encode()).hexdigest(), 16)

# Функція зашифрування повідомлення
def encrypt_message(message, p, g, y):
    h = hash_message(message)
    k = random.randint(1, p - 1)
    a = pow(g, k, p)
    b = (pow(y, k, p) * h) % p
    return a, b

# Функція розшифрування повідомлення
def decrypt_message(a, b, x, p):
    h = (b * modinv(pow(a, x, p), p)) % p
    return h

# Функція створення цифрового підпису
def sign_message(message, p, g, x):
    h = hash_message(message)
    k = random.randint(1, p - 1)
    r = pow(g, k, p)
    s = (modinv(k, p - 1) * (h - x * r)) % (p - 1)
    return r, s

# Функція перевірки цифрового підпису
def verify_signature(message, r, s, p, g, y):
    h = hash_message(message)
    if r < 1 or r > p - 1 or s < 1 or s > p - 2:
        return False
    v1 = pow(g, h, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p
    return v1 == v2

# викликаємо реалізовані функції
if __name__ == '__main__':
    nbits =256

    # Генеруємо ключі
    p, g, x, y = generate_keys(nbits)
    print('Параметри ElGamal:')
    print('p =', p)
    print('g =', g)
    print('x =', x)
    print('y =', y)

    # Зашифрувуємо та розшифровуємо повідомлення
    message = 'Hello, world!'
    print('\nПовідомлення для зашифрування:', message)
    a, b = encrypt_message(message, p, g, y)
    print('Зашифроване повідомлення:', (a, b))
    decrypted_message = decrypt_message(a, b, x, p)
    print('Розшифроване повідомлення:', decrypted_message)

    # Створюємо та перевіряємо цифровий підпис
    signature = sign_message(message, p, g, x)
    print('\nЦифровий підпис:', signature)
    is_valid = verify_signature(message, signature[0], signature[1], p, g, y)
    print('Перевірка підпису:', is_valid)