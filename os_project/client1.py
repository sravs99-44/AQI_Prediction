# This client python file is code is related to the Newyork city.
import socket
import requests
import pandas as pd
import time
import pickle

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server hostname and port
host = socket.gethostname()
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Send data to the server
message = "Hello, server!"
client_socket.send(message.encode())

def get_air_pollution_history(lat, lon,  api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        # If the request was successful, print the JSON response
        result = response.json()
        result_list = result['list']
        df = []
        for i in result_list:
            row = {}
            
            for j in i['components']:
                row[j] = i['components'][j]
            row['aqi'] = i['main']['aqi']
            row['dt'] = i['dt']
            df.append(row)
            
        df = pd.DataFrame(df)
        df_sorted = df.sort_values(by='dt', ascending=False)
        
        # Assuming 'df' is your DataFrame containing the data
        # Split the DataFrame into features (X) and target variable (y)
        X = df_sorted.drop(columns=['aqi'])  # Features (remove the target column)
        y = df_sorted['aqi'] 
        print(X.iloc[0])
        df_bytes = pickle.dumps(X.iloc[0])
        client_socket.sendall(df_bytes)



    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error during API request: {e}")


api_key = '227487d348e815512d9f1c997142adde'
latitude = '40.7128'
longitude = '-74.0060'

current_timestamp = int(time.time())


get_air_pollution_history(latitude, longitude, api_key)

# Receive data from the server
response = client_socket.recv(1024)
print(f"Received from server: {response.decode()}")

# Close the connection
client_socket.close()
