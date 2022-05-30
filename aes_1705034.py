from bitvectordemo_1705034 import Sbox, Mixer, InvMixer, InvSbox
from BitVector import *
import time
rcon = (BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="04"), BitVector(hexstring="08"),	BitVector(hexstring="10"),
        BitVector(hexstring="20"), BitVector(hexstring="40"), BitVector(hexstring="80"), BitVector(hexstring="1B"), BitVector(hexstring="36"))

def byte_substitution(temp_w):
    for i in range(0, 4):
        b = BitVector(hexstring = temp_w[i].get_bitvector_in_hex())
        int_val = b.intValue()
        s = Sbox[int_val]
        s = BitVector(intVal=s, size=8)
        temp_w[i] = s
    return temp_w

def byte_substitution_2(state_matrix, inv):
    for i in range(0, 16):
        b = BitVector(hexstring = state_matrix[i].get_bitvector_in_hex())
        int_val = b.intValue()
        if inv == 0:
            s = Sbox[int_val]
        else:
            s = InvSbox[int_val]
        s = BitVector(intVal=s, size=8)
        state_matrix[i] = s
    return state_matrix

def row_shifting(arr, inv):
    arr2 = [[0]*4 for i in range(4)]
    for i in range(0, 4):
        for j in range(0, 4):
            arr2[i][j] = arr[i+4*j]
    if inv == 0:
        arr2[1] = arr2[1][1:] + arr2[1][:1]
        arr2[2] = arr2[2][2:] + arr2[2][:2]
        arr2[3] = arr2[3][3:] + arr2[3][:3]
    else:
        arr2[1] = arr2[1][-1:] + arr2[1][:-1]
        arr2[2] = arr2[2][-2:] + arr2[2][:-2]
        arr2[3] = arr2[3][-3:] + arr2[3][:-3]
    for i in range(0, 4):
        for j in range(0, 4):
            arr[i+4*j] = arr2[i][j]
    return arr

def mix_column(arr, inv):
    AES_modulus = BitVector(bitstring='100011011')
    arr2 = []
    for i in range(0, 4):
        for j in range(0, 4):
            x = BitVector(hexstring="00")
            for k in range(0, 4):
                if inv == 0:
                    x = x ^ Mixer[j][k].gf_multiply_modular(arr[4*i+k], AES_modulus, 8)
                else:
                    x = x ^ InvMixer[j][k].gf_multiply_modular(arr[4*i+k], AES_modulus, 8)
            arr2.append(x)
    return arr2

def generate_roundkey(key):
    #padding
    if len(key) > 16:
        key = key[0: 16]
    elif len(key) < 16:
        key = key + '0' * (16 - len(key))

    key_hex = []
    for i in range(0, len(key)):
        x = key[i].encode('utf-8')
        h = x.hex()
        key_hex.append(BitVector(hexstring = h.lstrip("0x")))


    w = [[0]*4 for i in range(44)]
    for i in range(0, 4):
        w[i][0] = key_hex[4*i + 0]
        w[i][1] = key_hex[4*i + 1]
        w[i][2] = key_hex[4*i + 2]
        w[i][3] = key_hex[4*i + 3]

    rconidx = 0
    for i in range(4, 44):
        #calculating g func
        if i%4 == 0:
            temp_w = w[i-1].copy()
            #circular left shift
            temp_w = temp_w[1:] + temp_w[:1]
            temp_w = byte_substitution(temp_w)
            #adding round constant
            temp_w[0] = temp_w[0] ^ rcon[rconidx]
            rconidx = rconidx + 1

            for j in range (0,4):
                w[i][j] = w[i-4][j] ^ temp_w[j]

        else:
            for j in range (0,4):
                w[i][j] = w[i-1][j] ^ w[i-4][j]

    roundkeys = [[0]*16 for i in range(11)]
    for i in range(0, 11):
        for j in range(0, 4):
            roundkeys[i][4*j] = w[4*i+j][0]
            roundkeys[i][4*j+1] = w[4*i+j][1]
            roundkeys[i][4*j+2] = w[4*i+j][2]
            roundkeys[i][4*j+3] = w[4*i+j][3]
    return roundkeys

def encryption(plain_text, roundkeys, is_hex):
    pad_count = 0
    if (len(plain_text) % 16) != 0:
        pad_count = 16 - (len(plain_text) % 16)
        plain_text = plain_text + " " * pad_count

    cipher_text = []
    blocks = int(len(plain_text) / 16)
    for i in range(0, blocks):
        cipher_text.extend(encryption_init(plain_text[0 + i*16 : 16 + i*16], roundkeys, is_hex))
    return cipher_text

def encryption_init(plain_text, roundkeys, is_hex):
    state_matrix = []
    for i in range(0, len(plain_text)):
        if is_hex == 0:
            x = plain_text[i].encode('utf-8')
            h = x.hex()
            state_matrix.append(BitVector(hexstring = h.lstrip("0x")))
        else:
            print(plain_text[i])
            state_matrix.append(BitVector(hexstring = plain_text[i]))


    for j in range(0, 16):
        state_matrix[j] = state_matrix[j] ^ roundkeys[0][j]
    for i in range(1, 11):
        state_matrix = byte_substitution_2(state_matrix, 0)
        state_matrix = row_shifting(state_matrix, 0)
        if i != 10:
            state_matrix = mix_column(state_matrix, 0)
        for j in range(0, 16):
            state_matrix[j] = state_matrix[j] ^ roundkeys[i][j]
    cipher_text = []
    for k in range(0, 16):
        cipher_text.append(state_matrix[k].get_bitvector_in_hex())
    return cipher_text

def decryption(cipher_text, roundkeys):
    decrypted_text = []
    blocks = int(len(cipher_text) / 16)
    for i in range(0, blocks):
        decrypted_text.extend(decryption_init(cipher_text[0 + i*16 : 16 + i*16], roundkeys))
    return "".join(decrypted_text)

def decryption_init(cipher_text, roundkeys):
    state_matrix = []
    for i in range(0, len(cipher_text)):
        #x = cipher_text[i].encode('utf-8')
        #h = x.hex()
        state_matrix.append(BitVector(hexstring = cipher_text[i]))

    for j in range(0, 16):
        state_matrix[j] = state_matrix[j] ^ roundkeys[10][j]
    for i in range(1, 11):
        state_matrix = row_shifting(state_matrix, 1)
        state_matrix = byte_substitution_2(state_matrix, 1)
        for j in range(0, 16):
            state_matrix[j] = state_matrix[j] ^ roundkeys[10-i][j]
        if i != 10:
            state_matrix = mix_column(state_matrix, 1)
    decrypted_text = []
    for k in range(0, 16):
        decrypted_text.append(state_matrix[k].get_bitvector_in_ascii())

    return decrypted_text
