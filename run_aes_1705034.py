from aes_1705034 import *
## input ##
pad_count = 0
option = input("1. Text transfer\n2. File transfer\n")
if option == "2":
    filename = input("Enter file name from [From] folder : ")
    file = open("./From/{}".format(filename), "rb")
    file_content = file.read()
    file.close()
    plain_text = bytearray(file_content)


    #print("Plain Text: \n[In ASCII] ", plain_text)
    #print("[In HEX]", plain_text.encode('utf-8').hex())
    if (len(plain_text) % 16) != 0:
        pad_count = 16 - (len(plain_text) % 16)
    for i in range(pad_count):
        plain_text.append(ord(" "))

    key = input("Key : \n[In ASCII] ")
    print("[In HEX]", key.encode('utf-8').hex())


else:
    plain_text = input("Plain Text: \n[In ASCII] ")
    print("[In HEX]", plain_text.encode('utf-8').hex())
    if (len(plain_text) % 16) != 0:
        pad_count = 16 - (len(plain_text) % 16)
        plain_text = plain_text + " " * pad_count

    key = input("Key : \n[In ASCII] ")
    print("[In HEX]", key.encode('utf-8').hex())



if option == "2":
    global new_plain
    new_plain = []
    for i in range(len(plain_text)):
        new_plain.append(format(plain_text[i],'X'))

#key generation
time_1 = time.time()
roundkeys = generate_roundkey(key)
time_2 = time.time()
key_scheduling_time = time_2 - time_1


#encryption
time_1 = time.time()
if option == "2":
    cipher_text = encryption(new_plain, roundkeys, 1)
else:
    cipher_text = encryption(plain_text, roundkeys, 0)
time_2 = time.time()
encryption_time = time_2 - time_1


#decryption
time_1 = time.time()
decrypted_text = decryption(cipher_text, roundkeys)
decrypted_text = decrypted_text[: len(decrypted_text) - pad_count]
time_2 = time.time()
decryption_time = time_2 - time_1

decrypted_text_int = []
for i in decrypted_text:
    decrypted_text_int.append(ord(i))

if option == "2":
    file = open("./To/{}".format(filename), "wb+")
    file.write(bytearray(decrypted_text_int))
    file.close()


print("\nCipher Text:")
cipher_text = "".join(cipher_text)
print("[In HEX]", cipher_text)
bv = BitVector(hexstring = cipher_text)
ascii_string = bv.get_bitvector_in_ascii()
print("[In ASCII]", ascii_string)


print("\nDeciphered Text:")
print("[In HEX]", decrypted_text.encode('utf-8').hex())
print("[In ASCII]", decrypted_text)

print("\nExecution Time:")
print("Key Scheduling Time : " + str(key_scheduling_time) + " sec")
print("Encryption Time : " + str(encryption_time) + " sec")
print("Decryption Time : " + str(decryption_time) + " sec")
