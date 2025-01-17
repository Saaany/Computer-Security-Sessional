import socket
import random
from ECDH import *
from aes import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))
print("Connection established")
print("")

# receive parameters from server
eliptic_curve_parameters = str(sock.recv(1024).decode()).split(" ")
p = int(eliptic_curve_parameters[0])
a = int(eliptic_curve_parameters[1])
b = int(eliptic_curve_parameters[2])
G = (int(eliptic_curve_parameters[3]), int(eliptic_curve_parameters[4]))


K_prv, K_pub = generate_Eliptic_Curve_keys(p,a,b,G)
# print("Private key: {}".format(K_prv))
# print("Public key: {}".format(K_pub))

print("Sending public key to server...")
sock.send((str(K_pub[0])+' '+str(K_pub[1])).encode())

print("Receiving public key from server...")
server_pub_key = str(sock.recv(1024).decode()).split(" ")
server_pub_key = (int(server_pub_key[0]), int(server_pub_key[1]))
# print("Server public key: {}".format(server_pub_key))


# generate shared secret
S = double_add_algorithm(server_pub_key, K_prv, a, p)
# print("Shared secret generated: "+str(S[0]))

# send message
data = input(">> Write something to send to server: ")
data = aes_encryption(data, str(S[0]), str(S[1]))
data = sock.send(data.encode())
print("Data sent successfully!")

# receive message
received = sock.recv(1024)
print(">> Received Cipher Text: "+received.decode())
received = aes_decryption(received.decode(), str(S[0]), str(S[1]))
# print("Received data: "+received)

sock.close()
print("Connection closed")


