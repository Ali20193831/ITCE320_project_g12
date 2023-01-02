import socket
import threading
import json
import requests
from prettytable import PrettyTable

PORT = 49999
SERVER = "127.0.0.1"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER, PORT))
server.listen(3)

list_client = []


def my_func(conn, address, api_response):
    # this is a client thread
    print("< Accept Connection From {0} >".format(address))
    # first get client name and add it to the connected client and send the list to the current client
    client_name = conn.recv(2084).decode('utf-8')
    list_client.append(str(client_name))
    conn.sendall(str(list_client).encode())
    # ask the user for arr_icao
    print(client_name, " is connected right now ")
    while True:
        # this while loop receivers the client option and sends the appropriate answer
        try:
            # get user choice
            option = conn.recv(1000).decode()
            print("{:<9}".format(client_name), "Chose--> Option ", option)
            # depending on the option number the user will get a different output
            # their is an else to stop any number than is invalid just in case
            # but that should not happen because the client can't send any invalid number
            if option == '1':
                flight_list = option_1(api_response)
                print("sending option 1 to ", client_name)
                send_to_client(conn, flight_list)
            elif option == '2':
                flight_list = option_2(api_response)
                print("sending option 2 to ", client_name)
                send_to_client(conn, flight_list)
            elif option == '3':
                city_iata = conn.recv(1000).decode()
                flight_list = option_3(api_response, city_iata)
                print("sending option 3 to ", client_name)
                send_to_client(conn, flight_list)
            elif option == '4':
                flight_iata = conn.recv(1000).decode()
                print(flight_iata)
                flight_list = option_4(api_response, flight_iata)
                print("sending option 4 to ", client_name)
                send_to_client(conn, flight_list)
            elif option == '5':
                print(client_name, "client disconnected")
                break
            else:
                list_client.remove(client_name)
                print(client_name, "client disconnected")
                print('something went wrong')
                break
        except:
            # we used this except to close the thread when something un expected happens
            print('something went wrong')
            print(client_name, "connection is over")
            conn.close()
            break
    list_client.remove(client_name)
    print(client_name, "removed from current users list")
    conn.close()


def send_to_client(conn, flight_list_with_header):
    # this function will convert a list to string , encode and sends it the thread user
    flight_list_with_header = str(flight_list_with_header)
    conn.sendall(flight_list_with_header.encode('utf-8'))


def begin_new_connection():
    def valid_input(input_str):
        # this function takes the input provided by the user and checks for its validity
        if len(input_str) >= 4:
            return True

        else:
            print("Error! Only 4 characters allowed!")
            return False

    while True:
        # this function asks the user to input the arr_icao,
        # asks valid_input for its validity and
        arr_icao = input("Enter the airport code ( four letter or more ) : ")

        if valid_input(arr_icao):
            break
    print("icao is: ", arr_icao)
    # use the arr_icao to get the json response of the API
    api_response = get_api(arr_icao)
    # this function will accept new connection and start a new Thread
    while True:
        conn, address = server.accept()
        t = threading.Thread(target=my_func, args=(conn, address, api_response))
        t.start()


def option_1(api_response):
    # api_response is the json API response
    header = ['status', 'IATA', 'departure airport', 'arrival time','terminal', 'gate']
    # add the header as the header of the PrettyTable items
    items = PrettyTable(header)
    for flight in api_response['data']:
        if flight['flight_status'] == 'landed':
            if flight['flight']['codeshared'] is not None:
                # add a new row to the PrettyTable items table
                items.add_row([
                    str(flight['flight_status']),
                    str(flight['flight']['codeshared']['flight_iata']),
                    str(flight['departure']['airport']),
                    str(flight['arrival']['actual']),
                    str(flight['arrival']['terminal']),
                    str(flight['arrival']['gate'])
                ])

            else:
                # add a new row to the PrettyTable items table
                items.add_row([
                    str(flight['flight_status']),
                    str(flight['flight']['codeshared']),
                    str(flight['departure']['airport']),
                    str(flight['arrival']['actual']),
                    str(flight['arrival']['terminal']),
                    str(flight['arrival']['gate'])]
                )
    # return the full PrettyTable object
    return items


def option_2(api_response):
    # api_response is the json API response
    header = ['status', 'IATA', 'departure airport', 'departure time',
              'estimated arrival time', 'terminal', 'gate', ' delay']
    # add the header as the header of the PrettyTable items
    items = PrettyTable(header)
    for flight in api_response['data']:
        if flight['departure']['delay'] is not None:
            if flight['flight']['codeshared'] is not None:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['flight']['codeshared']['flight_iata']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['actual']),
                        str(flight['arrival']['estimated']),
                        str(flight['arrival']['terminal']),
                        str(flight['arrival']['gate']),
                        str(flight['departure']['delay'])
                    ]
                )

            else:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['flight']['codeshared']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['actual']),
                        str(flight['arrival']['estimated']),
                        str(flight['arrival']['terminal']),
                        str(flight['arrival']['gate']),
                        str(flight['departure']['delay'])
                    ]
                )
    return items


def option_3(api_response, city_iata):
    # api_response is the json API response
    header = ['status', 'IATA', 'departure airport', 'departure time',
              'estimated arrival time', 'terminal', 'gate', 'arrival IATA']
    # add the header as the header of the PrettyTable items
    items = PrettyTable(header)
    for flight in api_response['data']:
        if flight['departure']['iata'] == str(city_iata).upper():
            if flight['flight']['codeshared'] is not None:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['departure']['iata']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['actual']),
                        str(flight['arrival']['estimated']),
                        str(flight['arrival']['terminal']),
                        str(flight['arrival']['gate']),
                        str(flight['arrival']['iata'])
                    ]
                )

            else:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['departure']['iata']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['actual']),
                        str(flight['arrival']['estimated']),
                        str(flight['arrival']['terminal']),
                        str(flight['arrival']['gate']),
                        str(flight['arrival']['iata'])
                    ]
                )
    return items


def option_4(api_response, flight_iata):
    # api_response is the json API response
    header = ['status', 'IATA', 'date',
              'dep airport', 'dep gate', 'dep terminal',
              'arr airport', 'arr gate', 'arr terminal',
              'scheduled departure time', 'scheduled  arrival time', 'delay']
    # add the header as the header of the PrettyTable items
    items = PrettyTable(header)
    for flight in api_response['data']:
        if flight['flight']['iata'] == flight_iata:
            if flight['flight']['codeshared'] is not None:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['flight']['iata']),
                        str(flight['flight_date']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['gate']),
                        str(flight['departure']['terminal']),
                        str(flight['arrival']['airport']),
                        str(flight['arrival']['gate']),
                        str(flight['arrival']['terminal']),
                        str(flight['departure']['scheduled']),
                        str(flight['arrival']['scheduled']),
                        str(flight['departure']['delay'])
                    ]
                )

            else:
                # add a new row to the PrettyTable items table
                items.add_row(
                    [
                        str(flight['flight_status']),
                        str(flight['flight']['iata']),
                        str(flight['flight_date']),
                        str(flight['departure']['airport']),
                        str(flight['departure']['gate']),
                        str(flight['departure']['terminal']),
                        str(flight['arrival']['airport']),
                        str(flight['arrival']['gate']),
                        str(flight['arrival']['terminal']),
                        str(flight['departure']['scheduled']),
                        str(flight['arrival']['scheduled']),
                        str(flight['departure']['delay'])
                    ]
                )
    return items


def get_api(arr_icao):
    
    params = {
        'access_key': 'c74fef5e8c9f00e61a87ce11303cde5f', # parameters for the API response call with the user arr_icao
        'arr_icao': arr_icao,
        'limit': 100
    }
    print("getting API response for ", arr_icao, 'from:')
    print(('http://api.aviationstack.com/v1/flights', params))

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params) #the response from aviationstack
    
    with open("c:/Users/alial/OneDrive/Desktop/Python project/group_12.json", "w") as out_put_file:# save the response to a json file
        json.dump(api_result.json(), out_put_file)

    api_response = json.load(open('c:/Users/alial/OneDrive/Desktop/Python project/group_12.json', ))
    return api_response


print(20*"=", "server is starting",20*"=")
begin_new_connection()
