import socket
from aes_1705034 import encryption as aes_encryption
from aes_1705034 import generate_roundkey
from rsa_1705034 import encryption as rsa_encryption, key_generation
import json

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9090
clientSocket.connect(("127.0.0.1", port))
print("Conneted to server!")

plain_text = input("Enter the plain text : ")
key = input("Enter the key : ")
k = input("Enter the value of k (for RSA) : ")

#aes_encryption
pad_count = 0
if (len(plain_text) % 16) != 0:
    pad_count = 16 - (len(plain_text) % 16)
plain_text = plain_text + " " * pad_count
roundkeys = generate_roundkey(key)
cipher_text = aes_encryption(plain_text, roundkeys, 0)

#key_encryption by rsa
keys = key_generation(k)
public_key = (keys[0], keys[2])
private_key = (keys[1], keys[2])

encrypted_key = rsa_encryption(key, public_key[0], public_key[1], 0)

jsonFile = {"CT" : cipher_text, "EK" : encrypted_key, "PUK" : public_key}
jsonFile = json.dumps(jsonFile)
clientSocket.send(jsonFile.encode())

with open('Don\'t Open this/private_key.txt', 'w') as f:
    f.write(str(private_key[0]))
    f.write("\n")
    f.write(str(private_key[1]))

dataFromServer = clientSocket.recv(1024)
dataFromServer = dataFromServer.decode()

decrypted_plain_text = []  #decimal
with open("Don\'t Open this/decrypted_plain_text.txt", "r") as file:
    readlines = file.read().splitlines()
    decrypted_plain_text = readlines.copy()
if decrypted_plain_text[0] == plain_text:
    print("Success!! Decrypted plain text matched with original plain text!")
