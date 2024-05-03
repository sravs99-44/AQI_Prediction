Process of running the code.

Prequisities:
1. Python
2. Pip
3. Sklearn
4. Matplotlib
5. Pandas
6. Socket
7. Threading

Steps:
Step 1: Execute the AQI_server.py file in one of the terminal.
Step 2: Execute the client1.py file in another terminal. Client1 represents the newyork city.
Step 3: You should be getting the air quality index of next hour and visualization.
Step 4: Similarly try to execute the Client2.py and other files.
Step 5: You should be getting the prediction from the server without any late because we are using multithreading to handle multiple requests.


Procedure:

. Initially we train the models with the past 20 years of data of air quality index using the ensemble model of machine learning.
. These models are created using the AQI_server_ensemble.py file which in terms create the pickle files for each client.
. Using these pickle files for the next prediction when the request comes from the client.
. Usage of multithreading handles the multiple requests from the multiple clients to the same server.
