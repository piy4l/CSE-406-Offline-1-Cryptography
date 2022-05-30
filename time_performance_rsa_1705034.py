from prettytable import PrettyTable
from rsa_1705034 import *
x = PrettyTable()
x.field_names = ["K", "Key-Generation", "Encryption", "Decryption"]
k_values = [16, 32, 64, 128]
plain_text = input("Enter the plain text : ")
for k in k_values:
    time_1 = time.perf_counter()
    keys = key_generation(k)
    time_2 = time.perf_counter()
    key_generation_time = time_2 - time_1

    e = keys[0]
    d = keys[1]
    n = keys[2]

    time_1 = time.perf_counter()
    cipher_text = encryption(plain_text, e, n, 0)
    time_2 = time.perf_counter()
    encryption_time = time_2 - time_1

    time_1 = time.perf_counter()
    decrypted_text = decryption(cipher_text, d, n)
    time_2 = time.perf_counter()
    decryption_time = time_2 - time_1

    x.add_row([k, key_generation_time, encryption_time, decryption_time])
print(x)
