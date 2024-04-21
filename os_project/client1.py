import socket
import time
import json
import requests

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server hostname and port
host = socket.gethostname()
port = 12345

# Connect to the server
client_socket.connect((host, port))

api_key = '227487d348e815512d9f1c997142adde'
latitude = '40.7128'
longitude = '-74.0060'

current_timestamp = int(time.time())
start_time = current_timestamp - 3600
end_time = current_timestamp

city_name = "newyork"
client_socket.sendall(city_name.encode())

url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start_time}&end={end_time}&appid={api_key}"
    
response = requests.get(url)
response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
# If the request was successful, print the JSON response
result = response.json()

# Convert JSON object to string
result_string = json.dumps(result)

# Encode the string into bytes
result_bytes = result_string.encode()

# Send the data to the server
client_socket.sendall(result_bytes)



# Receive the response from the server
response = client_socket.recv(1024).decode()


print("AQI in newyork that received from server:",  str(int(round(float(response)))))

# Close the client socket
client_socket.close()
