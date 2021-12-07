import sys
#moves bit to a new place
def move_bit(sequence, _from, to, in_length, out_length):
    temp = (sequence&(1<<(in_length-_from)))
    push = (in_length-out_length)+(to-_from)
    if  push > 0:
        return temp >> push
    return temp << -1*push

#preforms initial permuation
def init_perm(block):
    hold = 0
    perm_init_list = [58, 50, 42, 34, 26, 18, 10, 2,
                      60, 52, 44, 36, 28, 20, 12, 4,
                      62, 54, 46, 38, 30, 22, 14, 6,
                      64, 56 ,48, 40, 32, 24, 16, 8,
                      57, 49, 41, 33, 25, 17, 9, 1,
                      59, 51, 43, 35, 27, 19, 11, 3,
                      61, 53, 45, 37, 29, 21, 13, 5,
                      63, 55, 47, 39, 31, 23, 15, 7]
    for i, p in enumerate(perm_init_list):        
        hold = move_bit(block, p, i+1, 64, 64)|hold
    return hold
    
#preforms inverse of initial permuation
def inv_init_perm(block): 
    hold = 0
    perm_init_list = [58, 50, 42, 34, 26, 18, 10, 2,
                      60, 52, 44, 36, 28, 20, 12, 4,
                      62, 54, 46, 38, 30, 22, 14, 6,
                      64, 56 ,48, 40, 32, 24, 16, 8,
                      57, 49, 41, 33, 25, 17, 9, 1,
                      59, 51, 43, 35, 27, 19, 11, 3,
                      61, 53, 45, 37, 29, 21, 13, 5,
                      63, 55, 47, 39, 31, 23, 15, 7]
    for i, p in enumerate(perm_init_list):        
        hold = move_bit(block, i+1, p, 64, 64)|hold
    return hold

#preforms permute on 64 input ket to generate 56 to then be shifted
def permute_1(my_key):
    hold = 0
    perm_1_list = [57, 49, 41, 33, 25, 17, 9,
                   1, 58, 50, 42, 34, 26, 18,
                   10, 2, 59, 51,  43, 35, 27,
                   19, 11, 3, 60, 52, 44, 36,
                   63, 55, 47, 39, 31, 23, 15,
                   7, 62, 54, 46, 38, 30, 22,
                   14, 6, 61, 53, 45, 37, 29,
                   21, 13, 5, 28, 20, 12, 4]
    for i, p in enumerate(perm_1_list):        
        hold = move_bit(my_key, p, i+1, 64, 56)|hold
    return hold
#preforms permute to generate subkey from cictular left shift subkey
def permute_2(my_key):
    hold = 0
    perm_2_list = [14, 17, 11, 24, 1, 5, 3, 28, 15,
                   6, 21, 10, 23, 19, 12, 4, 26,
                   8, 16, 7, 27, 20, 13, 2, 41,
                   52, 31, 37, 47, 55, 30, 40, 51,
                   45, 33, 48, 44, 49, 39, 56, 34,
                   53, 46, 42, 50, 36, 29, 32]
    for i, p in enumerate(perm_2_list):        
        hold = move_bit(my_key, p, i+1, 56, 48)|hold
    return hold

#prefors circluar left shift step that is needed to generate subkey
def get_subkey(key, my_round):
    shift_by=[1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    shift= shift_by[my_round]
    left = (key&(~268435455))>>28
    right = key&268435455
    left = ((left<<shift)|(left>>(28-shift)))&268435455
    right = ((right<<shift)|(right>>(28-shift)))&268435455
    next_key=(left<<28)|(right)
    return next_key

#expands 32bit to 48 in the way des specifies
def expand(sequence):
    hold = 0
    expand_list = [32, 1, 2, 3, 4, 5,
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]
    for i, p in enumerate(expand_list):        
        hold = move_bit(sequence, p, i+1, 32, 48)|hold
    return hold

#does the sboxs
def sbox(sequence):
    box=[[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
          [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
          [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
          [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
         [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
          [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
          [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
          [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
         [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
          [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
          [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
          [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
         [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
          [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
          [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
          [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
         [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
          [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
          [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
          [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
         [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
          [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
          [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
          [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
         [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
          [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
          [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
          [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    hold = 0
    for i in range(8):
        hold = hold<<4
        x = move_bit(sequence, 1+i*6, 1,48,2)
        x = x|move_bit(sequence, 6+i*6, 2,48,2)
        y = move_bit(sequence, 2+i*6, 1,48,4)
        y = y|move_bit(sequence, 3+i*6, 2,48,4)
        y = y|move_bit(sequence, 4+i*6, 3,48,4)
        y = y|move_bit(sequence, 5+i*6, 4,48,4)
        hold = hold|box[i][x][y]
    return hold

#the permustion of 32 bit 
def perm(sequence):
    hold = 0
    perml = [16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25]
    for i, p in enumerate(perml):        
        hold = move_bit(sequence, p, i+1, 32, 32)|hold
    return hold


def des(block, key):
    #splits into halfs
    left = (block & (~4294967295))>>32
    right = block & 4294967295
    #expands xor with key sbox the perm
    expanded = expand(right)
    en_right = perm(sbox(expanded^key))

    #switches left and right
    en = (left^en_right)|(right<<32)
    return en



def startEncryption(text, key):
    #runs the algo with sys args
    key = int(key, base=16)
    message = int(text, base=16)
    #generate list of subkeys
    subkeys=[]
    next_key = permute_1(key)
    for i in range(16):
        next_key=get_subkey(next_key,i)
        subkeys.append(permute_2(next_key))
        
    print(f'plaintext: {message:016x}, key: {key:016x}')

    #initial perm
    next_mess=init_perm(message)
    #16 rounds encryption
    rounds=[]
    for i in range(16):
        inter = des(next_mess, subkeys[i])
        print(f'{i:2} {next_mess:016x} × {subkeys[i]:012x} => {inter:016x}')
        rounds.append(inter)
        next_mess=inter

    #swap left and right and inv initial
    left = (next_mess & (~4294967295))>>32
    right = next_mess & 4294967295
    ciphertext = inv_init_perm((left)|(right<<32))
    print(f'ciphertext: {ciphertext:016x}')
    return ciphertext

def startDecrpyt(text, key):
    #WE NEED A WAY TO GET THE SUBKEYS TO THIS ALGORITHM
    #RIGHT NOW I SET IT TO BE A GLOBAL, IDK IF THIS WILL BITE US LATER
    ciphertext = int(text, base=16)
    key = int(key, base=16)
    #get keys back
    subkeys=[]
    next_key = permute_1(key)
    for i in range(16):
        next_key=get_subkey(next_key,i)
        subkeys.append(permute_2(next_key))

    print(f'ciphertext: {ciphertext:016x}, key: {key:016x}')

    #initial perm
    next_mess=init_perm(ciphertext)
    #16 rounds decryption
    cipher_rounds=[]
    for i in range(16):
        inter = des(next_mess, subkeys[15-i])
        print(f'{i:2} {next_mess:016x} × {subkeys[15-i]:012x} => {inter:016x}')
        cipher_rounds.append(inter)
        next_mess=inter
    #swap left and right and inv initial    
    left = (next_mess & (~4294967295))>>32
    right = next_mess & 4294967295
    unciphertext = inv_init_perm((left)|(right<<32))
    print(f'unciphertext: {unciphertext:016x}')
    return unciphertext