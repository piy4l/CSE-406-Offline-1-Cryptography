## input ##
plain_text = input("Enter the plain text : ")
plain_text = plain_text.encode('utf-8')
key = input("Enter the key : ")
key = key.encode('utf-8')
print(plain_text.hex() + ' ' + key.hex())

## key scheduling/expansion ##
