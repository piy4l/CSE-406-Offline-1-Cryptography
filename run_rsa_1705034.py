from rsa_1705034 import *
#input
option = input("1. Text transfer\n2. File transfer\n")

if option == "2":
    filename = input("Enter file name from [From] folder : ")
    file = open("./From/{}".format(filename), "rb")
    file_content = file.read()
    file.close()
    plain_text = bytearray(file_content)
else:
    plain_text = input("Enter the plain text : ")

k = input("Enter the value of k : ")

#key generation
time_1 = time.perf_counter()
keys = key_generation(k)
time_2 = time.perf_counter()
diff = time_2 - time_1
print("\nKey generation time : " + str(diff) + " sec")
e = keys[0]
d = keys[1]
n = keys[2]
#print(e, d, n)
print("\nGenerated Keys : ")
print("{'public' : ("+str(e)+", "+str(n)+"), ", end = "")
print("'private' : ("+str(d)+", "+str(n)+")}")

#encryption
time_1 = time.perf_counter()
if option == "2":
    cipher_text = encryption(plain_text, e, n, 1)
else:
    cipher_text = encryption(plain_text, e, n, 0)
time_2 = time.perf_counter()
diff = time_2 - time_1
print("\nEncryption time : " + str(diff) + " sec")

#decryption
time_1 = time.perf_counter()
decrypted_text = decryption(cipher_text, d, n)
time_2 = time.perf_counter()
diff = time_2 - time_1
print("Decryption time : " + str(diff) + " sec")


decrypted_text_int = []
for i in decrypted_text:
    decrypted_text_int.append(ord(i))

if option == "2":
    file = open("./To/{}".format(filename), "wb+")
    file.write(bytearray(decrypted_text_int))
    file.close()

print("\nCipher text : ")
print(cipher_text)

print("\nDecrypted text : ")
print(decrypted_text)
