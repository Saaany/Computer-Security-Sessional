import socket
from ECDH import *
from aes import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(5)
print("Server started")

while True:
    print("Waiting for connection...")
    connection, address = sock.accept()
    print("Connection from {}".format(address))
    print("")

    # eliptic curve parameters
    p, a, b, G = eliptic_curve_parameters_generator()

    # send parameters to client
    connection.send((str(p)+' '+str(a)+' '+str(b)+' '+str(G[0])+' '+str(G[1])).encode())


    # receive public key
    eliptic_curve_key = str(connection.recv(1024).decode()).split(" ")
    client_pub_key = (int(eliptic_curve_key[0]), int(eliptic_curve_key[1]))

    # generate public key
    K_prv, K_pub = generate_Eliptic_Curve_keys(p, a, b, G)
    # print("Private key: {}".format(K_prv))
    # print("Public key: {}".format(K_pub))

    # send public key
    connection.send((str(K_pub[0])+' '+str(K_pub[1])).encode())

    # generate shared secret
    S = double_add_algorithm(client_pub_key, K_prv, a, p)
    #print("Shared secret: " + str(S[0]))


    # receive message
    received = connection.recv(1024)
    print(">> Received Cipher Text: "+received.decode())
    received = aes_decryption(received.decode(), str(S[0]), str(S[1]))
    # print("Received data: "+received)

    data = input(">> Write something to send to server: ")

    data = aes_encryption(data, str(S[0]), str(S[1]))
    data = connection.send(data.encode())
    print(">> Data sent successfully!")
    print('>> Waiting for server response...')

    connection.close()