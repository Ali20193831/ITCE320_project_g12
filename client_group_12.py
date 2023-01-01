import socket
from prettytable import PrettyTable

PORT = 49999
SERVER = "127.0.0.1"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((SERVER, PORT)) # connect to the server
except:
    print("cant find server restart client") # if there is  problem then the client will shutsdown
    exit(0)

pretty_list_client = PrettyTable(["user name"]) # make the "user name" header for the clients list table

user = input("Enter the Username : ") # gets the client name from user 
user_encode = user.encode('utf-8')
client.sendall(user_encode) # send name to the server after encoding it