import socket
import pickle

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

    # Receive data from the client
    data = client_socket.recv(1024)
    df_bytes = b""
    while data:
        df_bytes += data
        data = client_socket.recv(1024)

    # Deserialize the DataFrame
    df = pickle.loads(df_bytes)
    print("Received DataFrame:")
    print(df)

    with open('model_c1.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    predictions = loaded_model.predict(df)
    print(df)

    # Close the connection
    client_socket.close()
