import socket, json
from rsa_1705034 import decryption as rsa_decryption
from aes_1705034 import decryption as aes_decryption, generate_roundkey
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")
port = 9090
serverSocket.bind(("", port))
print ("Socket binded to %s" %(port))
serverSocket.listen()
print ("Socket is listening")
while(True):
    (clientConnected, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
    dataFromClient = clientConnected.recv(1024)
    dataFromClient = json.loads(dataFromClient.decode())
    #print(dataFromClient.decode())
    cipher_text = dataFromClient.get("CT")   #hex
    encrypted_key = dataFromClient.get("EK") #decimal
    public_key = dataFromClient.get("PK")    #decimal

    private_key = []  #decimal
    with open("Don\'t Open this/private_key.txt", "r") as file:
        readlines = file.read().splitlines()
        private_key = readlines.copy()

    decrypted_key = rsa_decryption(encrypted_key, int(private_key[0]), int(private_key[1]))
    roundkeys = generate_roundkey(decrypted_key)
    decrypted_plain_text = aes_decryption(cipher_text, roundkeys)
    print(decrypted_plain_text)


    with open('Don\'t Open this/decrypted_plain_text.txt', 'w') as f:
        f.write("".join(decrypted_plain_text))
    clientConnected.send("Decypted plain text is written in the file. Please check!".encode());
    clientConnected.close()
    break
