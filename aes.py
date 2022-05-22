from bitvectordemo import Sbox
rcon = (0x01, 0x02,	0x04, 0x08,	0x10, 0x20,	0x40, 0x80,	0x1B, 0x36)
## input ##
key = input("Enter the key : ")
plain_text = input("Enter the plain text : ")


## key scheduling/expansion ##
#hex conversion
key_hex = []
for i in range(0, len(key)):
    x = key[i].encode('utf-8')
    key_hex.append(x.hex())

plain_text_hex = []
for i in range(0, len(plain_text)):
    x = plain_text[i].encode('utf-8')
    plain_text_hex.append(x.hex())

w = [[0]*4 for i in range(44)]
for i in range(0, 4):
    w[i][0] = hex(int(key_hex[4*i + 0], 16))
    w[i][1] = hex(int(key_hex[4*i + 1], 16))
    w[i][2] = hex(int(key_hex[4*i + 2], 16))
    w[i][3] = hex(int(key_hex[4*i + 3], 16))
print(w[3])

rconidx = 0
for i in range(4, 44):
    #calculating g func
    if i%4 == 0:

        temp_w = w[i-1]
        print(i)
        print(w[3])
        #circular left shift
        temp = temp_w[0]
        temp_w[0] = temp_w[1]
        temp_w[1] = temp_w[2]
        temp_w[2] = temp_w[3]
        temp_w[3] = temp                #hex

        #byte substitution
        for j in range(0, 4):
            #print(temp_w[j])
            if(len(temp_w[j]) == 3):
                x = '0'
                y = temp_w[j][2]
            else:
                x = temp_w[j][2]
                y = temp_w[j][3]
            x = int(x, 16)
            y = int(y, 16)
            temp_w[j] = hex(Sbox[16*x + y])  #hex
        #adding round constant
        temp_w[0] = hex(int(temp_w[0], 16) ^ rcon[rconidx])
        rconidx = rconidx + 1

        for j in range (0,4):
            w[i][j] = hex(int(w[i-4][j], 16) ^ int(temp_w[j], 16))

    else:
        for j in range (0,4):
            w[i][j] = hex(int(w[i-1][j], 16) ^ int(w[i-4][j], 16))
#print(w)
