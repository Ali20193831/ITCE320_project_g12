import socket
from prettytable import PrettyTable

PORT = 49999
SERVER = "127.0.0.1"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((SERVER, PORT)) # connect to the server
except:
    print("cant find server !") # if there is  problem then the client will shutsdown
    exit(0)

pretty_list_client = PrettyTable(["user name"]) # make the "user name" header for the clients list table

user = input("Enter the Username : ") # gets the client name from user 
user_encode = user.encode('utf-8')
client.sendall(user_encode) # send name to the server after encoding it

# the client receives a list of the currently connected users
list_client = client.recv(2085).decode()
print("clients list table: ")

pretty_list_client.clear_rows() #clients list table
for item in eval(list_client):
    pretty_list_client.add_row([item])
print(pretty_list_client)
print("Welcome", user)
print(10*"=","Menu",10*"=")

# this function takes the data sent by the server prints it
def data_list(input_):
   
    input_decoded = input_.decode('utf-8')
    print(input_decoded)

while True:
    try:
        print("1- All arrived flights")
        print("2- All delayed flights")
        print("3- All flights from a specific city")
        print("4- Details of a particular flight")
        print("5- Quit and print goodbye message")
        print(24*"=")
        option = input("Enter the option : ")
        if option == "1":
            client.sendall(option.encode())
            data = client.recv(8192)
            data_list(data)

        elif option == "2":
            client.sendall(option.encode())
            data = client.recv(16384)
            data_list(data)

        elif option == "3":
            client.sendall(option.encode())
            city_iata = input("please enter city iata: ")
            client.sendall(city_iata.encode())
            data = client.recv(8192)
            data_list(data)

        elif option == "4":
            client.sendall(option.encode())
            flight_iata = input("please enter flight iata GF5300: ")
            client.sendall(flight_iata.encode())
            data = client.recv(8192)
            data_list(data)

        elif option == "5":
            client.sendall(option.encode())
            print("you are closed")
            client.close()
            break

        else:
            print("\n invalid number! please choose from 1 to 5: ")
        print(10*"=","Menu",10*"=")
    except:
        print("cant find server !")
        break
