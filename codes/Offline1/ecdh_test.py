from ECDH import *
import time
from prettytable import PrettyTable

time_list = [[0,0,0,0],[0,0,0,0],[0,0,0,0]] # [alice, bob, alice_shared, bob_shared]

def ecdh_test(idx, key_size):
    # eliptic curve parameters
    p, a, b, G = eliptic_curve_parameters_generator(key_size)

    # alice's end
    t1 = 1000*time.time()
    K_prv_alice, K_pub_alice = generate_Eliptic_Curve_keys(p, a, b, G)
    t2 = 1000*time.time() - t1
    time_list[idx][0] += t2

    # bob's end
    t1 = 1000*time.time()
    K_prv_bob, K_pub_bob = generate_Eliptic_Curve_keys(p, a, b, G)
    t2 = 1000*time.time() - t1
    time_list[idx][1] += t2

    # alice's shared secret
    t1 = 1000*time.time()
    S_alice = double_add_algorithm(K_pub_bob, K_prv_alice, a, p)
    t2 = 1000*time.time() - t1
    time_list[idx][2] += t2
    
    # bob's shared secret
    t1 = 1000*time.time()
    S_bob = double_add_algorithm(K_pub_alice, K_prv_bob, a, p)
    t2 = 1000*time.time() - t1
    time_list[idx][3] += t2

    # print(S_alice == S_bob)

def data_populate(idx, key_size):
    for i in range(5):
        ecdh_test(idx,key_size)
    
    for i in range(3):
        time_list[idx][i] = time_list[idx][i] / 5

def printTable(time_list):
    
    table = PrettyTable()

    # Define the table headers
    table.field_names = ["K", "A(ms)", "B(ms)","Shared key R(ms)"]

    # Add data to the table
    table.add_row(["128", (time_list[0][0] + time_list[0][2])/5 , (time_list[0][1] + time_list[0][3])/5, ((time_list[0][2] + time_list[0][3])/10)])
    table.add_row(["192", (time_list[1][0] + time_list[1][2])/5 , (time_list[1][1] + time_list[1][3])/5, ((time_list[1][2] + time_list[1][3])/10)])
    table.add_row(["256", (time_list[2][0] + time_list[2][2])/5 , (time_list[2][1] + time_list[2][3])/5, ((time_list[2][2] + time_list[2][3])/10)])

    # Print the table
    print(table)

def main():
    
    data_populate(0,128)
    data_populate(1,192)
    data_populate(2,256)
    
    printTable(time_list)
    
    

if __name__ == "__main__":
    main()

        
