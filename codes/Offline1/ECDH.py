import random
import math
import constants as const
import Crypto.Util.number

# p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
# a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
# b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
# G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
# n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
# h = 0x1

BITS = 128
def eliptic_curve_parameters_generator(bits = 128):
    
    BITS = bits
    p = Crypto.Util.number.getPrime(BITS, randfunc=Crypto.Random.get_random_bytes)
    while p % 4 != 3:
        p = Crypto.Util.number.getPrime(BITS, randfunc=Crypto.Random.get_random_bytes)

    # print ("\nRandom n-bit Prime (p): ",p)
    
    while True:
        a = random.randint(1, p-1)
        b = random.randint(1, p-1)

        if (4 * a**3 + 27 * b**2) % p != 0:
            
            x_ord = random.randint(1, p-1)
            y_ord_square = (x_ord**3 + a*x_ord + b) % p
            y_ord = pow(y_ord_square, (p+1)//4, p)
            
            # https://www.geeksforgeeks.org/find-square-root-under-modulo-p-set-1-when-p-is-in-form-of-4i-3/
            # print("y_ord_square: ", y_ord)
            # Try "+(n^((p + 1)/4))" and "-(n^((p + 1)/4))" both
            if((y_ord**2 % p) == y_ord_square):
                #print("y_ord is good using + : ", y_ord)
                break

            y_ord = p - y_ord
            # print("y_ord_square: ", y_ord)
            if((y_ord**2 % p) == y_ord_square):
                #print("y_ord is good is using - :", y_ord)
                break

    G = (x_ord, y_ord)

    return p, a, b, G

def generate_Eliptic_Curve_keys(p,a,b,G):
    
    # hasse's theorem
    n = p - int(2*math.sqrt(p)) + 1
    # generate private key
    K_prv = random.randint(2, n - 1)
    # generate public key
    K_pub = double_add_algorithm(G, K_prv, a, p)
    return K_prv, K_pub


def add(P, Q, p):
    # find the slope of the line
    s = (Q[1] - P[1]) * pow(Q[0] - P[0], p-2, p) % p
    # find the x coordinate of the next point
    x = (s**2 - P[0] - Q[0]) % p
    # find the y coordinate of the next point
    y = (s * (P[0] - x) - P[1]) % p
    return (x, y)

def double(P, a, p):
    # find the slope of the tangent line
    s = (3 * P[0]**2 + a) * pow(2 * P[1], p-2, p) % p
    # find the x coordinate of the next point
    x = (s**2 - 2 * P[0]) % p
    # find the y coordinate of the next point
    y = (s * (P[0] - x) - P[1]) % p
    return (x, y)

def double_add_algorithm(P, n, a, p):
    # convert n to binary
    n_bin = bin(n)[2:]
    # initialize P to G
    T = P
    # loop through n_bin
    for i in range(1, len(n_bin)):
        # double P
        T = double(T, a, p)
        # if n_bin[i] == 1, add G to P
        if n_bin[i] == '1':
            T = add(T, P, p)
    # nG = P
    return P

# p,a,b,G = eliptic_curve_parameters_generator()
# n = p - int(2*math.sqrt(p)) + 1

# print(S_a == S_b)
# print(S_a)
# print(S_b)

# x = (G[0]**3 + a*G[0] + b) % p
# print(x == G[1]**2 % p)

