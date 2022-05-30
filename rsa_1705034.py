from Crypto.Util.number import getPrime
import math, time, random

def key_generation(k):
    k = int(k)
    k = int(k/2)
    p = getPrime(k)
    q = getPrime(k)
    while p == q:
        q = getPrime(k)
    #print(p, q)
    n = p * q
    phi = (p-1) * (q-1)
    #e = phi - 1
    e = 2
    while math.gcd(phi, e) != 1:
        #e = e - 1
        e = e + 1
        #e = random.randrange(2, phi)
    i = 1
    while (((phi * i) + 1) % e) != 0:
        i = i + 1
    d = int(((phi * i) + 1) // e)
    return e, d, n

def encryption(plain_text, e, n, is_int):
    cipher_text = []
    for character in plain_text:
        if is_int == 0:
            p = ord(character)
        else:
            p = character
        c = pow(p, e, n)
        cipher_text.append(c)
    return cipher_text

def decryption(cipher_text, d, n):
    decrypted_text = []
    for c in cipher_text:
        if isinstance(c, str):
            c = int(c, 16)
        p = pow(c, d, n)
        decrypted_text.append(chr(p))
    return "".join(decrypted_text)
