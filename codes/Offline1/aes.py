import time
import numpy as np
from BitVector import *
import constants as const

time_list = [0,0,0]

def println(text,flag = True):
    if(flag):
        print(text)


def aes_encryption(plain_text,key_text, cbc_vector = "0" * const.BLOCK_SIZE_BYTE):

    plain_text = padding(plain_text)
    print("In Hex: " + plain_text.encode("utf-8").hex())
    print("")

    # timing
    KEY_SCHEDULE_TIME = 1000* time.time()
    keys = key_schedule(convert_block(key_text))
    KEY_SCHEDULE_TIME = 1000* time.time() - KEY_SCHEDULE_TIME
    time_list[0] = KEY_SCHEDULE_TIME

    cipher_text = ""
    # cbc mode
    # cbc_vector = "0" * const.BLOCK_SIZE_BYTE
    cbc_vector = convert_block(cbc_vector)
    #print("CBC Vector:"+cbc_vector)

    cipher_ascii=""
    
    ENCRYPTION_TIME = 1000 * time.time()
    for i in range(0,len(plain_text),const.BLOCK_SIZE_BYTE):

        block = plain_text[i:i+const.BLOCK_SIZE_BYTE]

        block = xor_string(block,cbc_vector)
        # encryption block by block
        cbc_vector = cipher(encrypt_block(block,keys))
        #cbc_vector = cipher_text[-2*const.BLOCK_SIZE_BYTE:]
        cipher_text += cbc_vector

        # convert cbc_vector hex string to ascii string
        cbc_vector = "".join(chr(int(cbc_vector[i:i+2],16)) for i in range(0,len(cbc_vector),2))
        cipher_ascii += cbc_vector

    ENCRYPTION_TIME = 1000 * time.time() - ENCRYPTION_TIME
    time_list[1] = ENCRYPTION_TIME

    print("Ciphered Text:")
    print("In Hex: " + cipher_text)
    print("In ASCII: " + cipher_ascii)
    print(" ")

    return cipher_text

def xor_string(str1,str2):

    if(len(str1) != len(str2)):
        raise Exception("Invalid string length")
    else:
        return "".join(chr(ord(a) ^ ord(b)) for a,b in zip(str1,str2))
    
def aes_decryption(cipher_text,key_text, cbc_vector = "0" * const.BLOCK_SIZE_BYTE):

    keys = key_schedule(convert_block(key_text))

    plain_text = ""
    # cbc_vector = "0" * const.BLOCK_SIZE_BYTE
    cbc_vector = convert_block(cbc_vector)

    DECRYPTON_TIME = 1000* time.time()
    for i in range(0,len(cipher_text),2*const.BLOCK_SIZE_BYTE):

        block = cipher_text[i:i+2*const.BLOCK_SIZE_BYTE]

        block = decipher(decrypt_block(block,keys))
        block = xor_string(block,cbc_vector)
        plain_text += block

        cbc_vector = cipher_text[i:i+2*const.BLOCK_SIZE_BYTE]

        # convert cbc_vector to string
        cbc_vector = "".join(chr(int(cbc_vector[i:i+2],16)) for i in range(0,len(cbc_vector),2))
    
    DECRYPTON_TIME = 1000* time.time() - DECRYPTON_TIME
    time_list[2] = DECRYPTON_TIME

    print("Deciphered Text:")
    print("In Hex: " + plain_text.encode("utf-8").hex())
    # print("In ASCII: " + plain_text)
    # print("")
    # unpadding
    plain_text = unpadding(plain_text)

    print("In ASCII: " + plain_text)
    print("")

    return plain_text  

def unpadding(text):

    if(len(text) == 0):
        return text
    
    pad_len = ord(text[-1])
    pad_txt = text[-pad_len:]
    if(pad_len > const.BLOCK_SIZE_BYTE):
        return text
    elif(pad_txt != chr(pad_len) * pad_len):
        return text
    
    return text[:-pad_len]

def decipher(state_mat):
    # convert state matrix to string
    hex_str = ""
    row_size = const.BLOCK_SIZE_WORD
    col_size = const.COLUMN_SIZE

    for i in range(row_size):
        for j in range(col_size):

            hex_val = state_mat[j][i][2:]

            if(len(hex_val) == 1):
                hex_val = "0" + hex_val
            hex_str += hex_val

    #return bytearray.fromhex(hex_str).decode()
    return "".join(chr(int(hex_str[i:i+2],16)) for i in range(0,len(hex_str),2))

def cipher(state_mat):
    # convert state matrix to string
    cipher_text = ""
    row_size = const.BLOCK_SIZE_WORD
    col_size = const.COLUMN_SIZE

    for i in range(row_size):
        for j in range(col_size):

            hex_val = state_mat[j][i]
            if(hex_val.startswith("0x")):
                hex_val = hex_val[2:]
            
            if(len(hex_val) == 1):
                hex_val = "0" + hex_val
            
            cipher_text += hex_val
    
    return cipher_text

def encrypt_block(plain_text,keys):

    if(len(plain_text) != const.BLOCK_SIZE_BYTE):
        raise Exception("Invalid block size")
    
    state_mat = state_matrix(plain_text)
    state_mat = add_round_key(state_mat,keys[0])

    for i in range(1,10):
        state_mat = sub_bytes(state_mat)
        state_mat = shift_rows(state_mat)
        state_mat = mix_columns(state_mat)
        state_mat = add_round_key(state_mat,keys[i])

    # final round
    state_mat = sub_bytes(state_mat)
    state_mat = shift_rows(state_mat)
    state_mat = add_round_key(state_mat,keys[10])

    
    return state_mat

def decrypt_block(cipher_text,keys):
    
    if(len(cipher_text) != 2*const.BLOCK_SIZE_BYTE):
        raise Exception("Invalid block size")
    
    state_mat = inv_state_matrix(cipher_text)
    state_mat = add_round_key(state_mat,keys[10])

    for i in range(9,0,-1):
        state_mat = inv_shift_rows(state_mat)
        state_mat = inv_sub_bytes(state_mat)
        state_mat = add_round_key(state_mat,keys[i])
        state_mat = inv_mix_columns(state_mat)

    # final round
    state_mat = inv_shift_rows(state_mat)
    state_mat = inv_sub_bytes(state_mat)
    state_mat = add_round_key(state_mat,keys[0])

    return state_mat

def inv_state_matrix(text):

    if(len(text) %2 != 0):
        raise Exception("Invalid text length")
    else:
        row_size = const.BLOCK_SIZE_WORD
        col_size = const.COLUMN_SIZE
        matrix =  list(text[i:i+2] for i in range(0,len(text),2))
        return np.reshape(matrix,(row_size,col_size)).T.tolist() # column major order

def inv_shift_rows(state_mat):

    new_state_mat = []
    for i in range(const.BLOCK_SIZE_WORD):
        new_state_mat.append(np.roll(state_mat[i],i)) # TODO: check if this works
    
    return new_state_mat

def inv_sub_bytes(state_mat):
    
    new_state_mat = []
    for i in range(const.BLOCK_SIZE_WORD):
        new_state_mat.append([hex(const.InvSbox[int(c,16)]) for c in state_mat[i]])
    
    return new_state_mat

def inv_mix_columns(state_mat):
    
    new_state_mat = []
    state_mat = np.array(state_mat).T # row major order
    row_size = const.BLOCK_SIZE_WORD
    col_size = const.COLUMN_SIZE

    for i in range(row_size):
        row = []
        for j in range(col_size):
            dot_prod = 0

            for k in range(row_size):
                bv1 = const.InvMixer[i][k]
                bv2 = BitVector(intVal=int(state_mat[j][k],16))

                dot_prod ^= (bv1.gf_multiply_modular(bv2,const.AES_modulus,8)).int_val()
            
            row.append(hex(dot_prod))
        new_state_mat.append(row)
    return new_state_mat

def sub_bytes(state_mat):
    
    new_state_mat = []
    for i in range(const.BLOCK_SIZE_WORD):
        new_state_mat.append([hex(const.Sbox[int(c,16)]) for c in state_mat[i]])
    
    return new_state_mat

def shift_rows(state_mat):

    new_state_mat = []
    for i in range(const.BLOCK_SIZE_WORD):
        new_state_mat.append(np.roll(state_mat[i],-i)) # TODO: check if this works
    
    return new_state_mat

def mix_columns(state_mat):
    
    new_state_mat = []
    state_mat = np.array(state_mat).T # row major order
    row_size = const.BLOCK_SIZE_WORD
    col_size = const.COLUMN_SIZE

    for i in range(row_size):
        row = []
        for j in range(col_size):
            dot_prod = 0

            for k in range(row_size):
                bv1 = const.Mixer[i][k]
                bv2 = BitVector(intVal=int(state_mat[j][k],16))

                dot_prod ^= bv1.gf_multiply_modular(bv2,const.AES_modulus,8).intValue()
            
            row.append(hex(dot_prod))
        new_state_mat.append(row)
    return new_state_mat
        


def state_matrix(text):

    matrix =  text_to_matrix(convert_block(text))
    return np.array(matrix).T.tolist() # column major order

def add_round_key(state_mat,key):

    new_state_mat = []
    round_key = np.array(key).T.tolist()

    for i in range(const.BLOCK_SIZE_WORD):
        new_state_mat.append(xor(state_mat[i],round_key[i]))
    
    return new_state_mat

def padding(text):

    block_size_bytes = const.BLOCK_SIZE_BYTE
    pad_len = block_size_bytes - len(text) % block_size_bytes

    if(pad_len == 0):
        return text
    elif (pad_len == block_size_bytes):
        return text
    else:
        return text + (chr(pad_len) * pad_len)
    
def key_schedule(key_text):

    keys = [text_to_matrix(key_text)]

    for i in range(10):
        keys.append(key_expansion(keys[i],i+1))

    return keys


def convert_block(text):

    length = len(text)

    if(length < const.BLOCK_SIZE_BYTE):
        return text + ("0" * (const.BLOCK_SIZE_BYTE - length))
    elif(length > const.BLOCK_SIZE_BYTE):
        return text[0:int(const.BLOCK_SIZE_BYTE)]
    
    return text

def text_to_matrix(text):

    hex_val_list = [hex(ord(c)) for c in text]

    row_size = const.BLOCK_SIZE_WORD
    col_size = const.COLUMN_SIZE

    matrix = np.matrix(np.reshape(hex_val_list,(int(row_size),int(col_size)))).tolist()
    return matrix

def key_expansion(prev_key,round_num):

    next = [xor(prev_key[0],g_func(prev_key[3],round_num))]
    # sub bytes
    for i in range(1,const.BLOCK_SIZE_WORD):
        new_key_word = (xor(next[i-1],prev_key[i]))
        next.append(new_key_word)
    
    return next

def xor(arr1,arr2):
    # xor two arrays
    res = []
    for i in range(len(arr1)):
        res.append(hex(int(arr1[i],16) ^ int(arr2[i],16)))
    return res

def g_func(arr,round_num):
    # g function
    # rotate
    # sub bytes
    # add round constant
    arr = np.concatenate((arr[1:],arr[:1]))
    arr = [hex(const.Sbox[int(c,16)]) for c in arr]
    arr[0] = hex(int(arr[0],16) ^ round_constant(round_num))

    return arr

def round_constant(round_num):
    # return round constant
    if round_num == 1:
        return 0x01
    prev_rc = round_constant(round_num-1)
    return (prev_rc << 1) ^ (0x11b & -(prev_rc >> 7))

def main():
    # test
    
    print("Key:")
    key_text = input("In ASCII: ")
    print("In Hex: " + key_text.encode("utf-8").hex())
    print("")
    print("Plain Text:")
    plain_text = input("In ASCII: ")

    # plain_text = "Never Gonna Give you up"
    # key_text = "BUET CSE19 Batch"

    cipher = aes_encryption(plain_text,key_text)
    aes_decryption( cipher,key_text)

    print("Execution Time Details:")
    print("Key Schedule Time: " + str(time_list[0]) + " ms")
    print("Encryption Time: " + str(time_list[1]) + " ms")
    print("Decryption Time: " + str(time_list[2]) + " ms")
    print("")

if __name__ == "__main__":
    main()
