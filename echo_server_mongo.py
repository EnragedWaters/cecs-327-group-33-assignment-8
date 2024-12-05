from pymongo import MongoClient
from datetime import datetime, timedelta
import socket

def calculate_average_moisture(collection):
    """Calculate average moisture in the kitchen fridge over the past three hours."""
    three_hours_ago = datetime.utcnow() - timedelta(hours=3)
    query = {"time": {"$gte": three_hours_ago}, "payload.topic": "fridge_link"}
    results = collection.find(query)
    total_moisture = 0
    count = 0

    for result in results:
        total_moisture += float(result['payload'].get('Fridge Moisture Meter', 0))
        count += 1

    average_moisture = total_moisture / count
    print(f"Average moisture in the fridge in past 3 hours: {average_moisture}")

    return(f"Average moisture in the fridge in past 3 hours: {average_moisture}")
def dishwasher_water_consumption(collection):
    # Water consumption per cycle is generally pre-determined
    # So we just return a pre-determined variable
    return("Water consumption of Dishwasher: 10 gallons/cycle")
def find_greatest_ammeter_reading(collection):
    # Mapping of board names to their Ammeter fields
    device_info = {
        "Raspberry Pi 4 - board1": "Fridge Ammeter",
        "board 1 128e7f69-8111-4a92-8ae2-8861e1c631aa": "Fridge 2 Ammeter",
        "Raspberry Pi 4 - Dishwasher Board": "Dishwasher Ammeter"
    }

    ammeter_readings = {}


    for board_name, ammeter_field in device_info.items():
        query = {"payload.board_name": board_name}
        result = collection.find_one(query)

        if result:
            # Ammeter
            ammeter_reading = float(result['payload'].get(ammeter_field, 0))
            ammeter_readings[board_name] = ammeter_reading

    max_board = max(ammeter_readings, key=ammeter_readings.get)
    max_reading = ammeter_readings[max_board]


    print("Ammeter measurement:")
    for board, reading in ammeter_readings.items():
        print(f"  {board}: {reading} Amps")

    print(f"Highest Ammeter reading: {max_board} ({max_reading} A)")
    return(f"Highest Ammeter reading: {max_board} ({max_reading} A)")

def mongoConnection(command: str) -> str:
    try:
        link = "mongodb+srv://troy_waters_test:9Psuj4BJMAPVQSzB@cluster0-troy-waters.dm3qj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0-troy-waters"
        client = MongoClient(link)

        # MongoDB
        data = client['test']
        collection = data['Cluster0-troy-waters_virtual']

        if command == "1":
            return calculate_average_moisture(collection)
        elif command == "2":
            return dishwasher_water_consumption(collection)
        elif command == "3":
            return find_greatest_ammeter_reading(collection)
        else:
            return "Incorrect command. Try again. 1, 2, 3, or 4."

    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")


def start_server():
    # Input our port and host
    port = int(input("Enter the port number for server hosting:"))
    # 0.0.0.0 for Locahost
    #host = '0.0.0.0'
    # 10.39.30.228 is wi-fi IPv4
    #host = '10.39.30.228'
    host = input("Enter the host IP for server hosting:")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind to the proper port
        server_socket.bind((host, port))

        # Listening
        server_socket.listen(5)
        print(f"Server is now listening on {host}:{port}")

        while True:
            # Accept the connection from client
            client_socket, client_address = server_socket.accept()
            print(f" Client connection : {client_address}")

            while True:
                try:

                    # Attempt to recieve clients message
                    message = client_socket.recv(1024).decode('utf-8')

                    if not message:
                        break

                    print(f"Recieved message from client: {message}")

                    # Convert to uppercase
                    # capitalized_message = message.upper()

                    #Send it back capitalized
                    #client_socket.send(capitalized_message.encode('utf-8'))
                    client_socket.send(mongoConnection(message).encode('utf-8'))
                except ConnectionResetError:
                    print("Connection Reset Error")
                    break

            print(f"Connection closed with {client_address}")
            client_socket.close()

    except Exception as error:
        print(f"Error: {error}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
    #TO DO: Client request and call functions
