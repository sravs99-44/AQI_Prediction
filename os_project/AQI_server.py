import socket
import pickle
import pandas as pd
import json
import subprocess


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and port
host = socket.gethostname()
port = 12345

# Bind to the port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    city_name = client_socket.recv(1024).decode()
    print(city_name)

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(type(data))
    # Convert the message to uppercase
    df_json = json.loads(data)
    df_json = df_json["list"]
    print(type(df_json))
    df = []
    for i in df_json:
        row = {}
        print(i)
        for j in i['components']:
            row[j] = i['components'][j]
        row['aqi'] = i['main']['aqi']
        row['dt'] = i['dt']
        df.append(row)
            
    df = pd.DataFrame(df)
    df = df.drop(columns=['aqi'])
    print(df)

    if city_name == "newyork":
        with open('model_c1.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
    elif city_name == "phildelphia":
        with open('model_c2.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
    elif city_name == "boston":
        with open('model_c3.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
    

    predictions = loaded_model.predict(df)
    
    aqi_prediction = str(predictions[0])
    
    print(len(aqi_prediction.encode()))
    print(aqi_prediction)
    

    # Send the uppercase message back to the client
    client_socket.sendall(aqi_prediction.encode())

    # Define the command to execute
    command = ["python3", "AQI_test.py", city_name]

    # Execute the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()

    # Print the output
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())
    print("New Model trained with new data")



    # Close the connection
    client_socket.close()
