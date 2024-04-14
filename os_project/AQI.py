import requests
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import time
import pickle
import sys
from sklearn.model_selection import train_test_split


def create_air_pollution_model(lat, lon, start, end, api_key, model_file_name):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        # If the request was successful, print the JSON response
        result = response.json()
        result_list = result['list']
        print(result_list)
        df = []
        for i in result_list:
            row = {}
            
            for j in i['components']:
                row[j] = i['components'][j]
            row['aqi'] = i['main']['aqi']
            row['dt'] = i['dt']
            df.append(row)
            
        df = pd.DataFrame(df)
        df = df.sort_values(by='dt', ascending=False)
        
        # Assuming 'df' is your DataFrame containing the data
        # Split the DataFrame into features (X) and target variable (y)
        X = df.drop(columns=['aqi'])  # Features (remove the target column)
        y = df['aqi']  # Target variable

        """X_train = X[:-1]  # All rows except the last one for training
        X_test = X[-1:]   # Last row for testing
        y_train = y[:-1]  # All target values except the last one for training
        y_test = y[-1:]"""

        # Split the data into 90% training and 10% testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state=42)

        # Print the shapes of the training and testing data
        print("Training data shape (X_train, y_train):", X_train.shape, y_train.shape)
        print("Testing data shape (X_test, y_test):", X_test.shape, y_test.shape)

        # 2. Choose a Model
        model = DecisionTreeClassifier()

        # 3. Train the Model
        model.fit(X_train, y_train)

        with open(model_file_name, 'wb') as file:
            pickle.dump(model, file)

        # 4. Make Predictions

        y_pred = model.predict(X_test)

        # Evaluate the predictions (optional)
        # print("Air Quality index at this particular time:" , y_pred[0])
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
  
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error during API request: {e}")

# Replace 'YOUR_API_KEY', 'LATITUDE', 'LONGITUDE', 'START_DATE', and 'END_DATE' with your OpenWeatherMap API key, latitude, longitude, start date, and end date
api_key = '227487d348e815512d9f1c997142adde'
city_name = sys.argv[1]

# Newyork(client 1) latidute and logitude values
if city_name == "newyork":
    latitude = '40.7128'
    longitude = '-74.0060'
    model_file_name = "model_c1.pkl"

# Phildelphia(client 2) latitude and logitude values
if city_name == "phildelphia":
    latitude = '39.9526'
    longitude = '75.1652'
    model_file_name = "model_c2.pkl"

# Boston(client 3) latitude and longitude values
if city_name == "boston":
    latitude = '42.3601'
    longitude = '71.0589' 
    model_file_name = "model_c3.pkl" 

current_timestamp = int(time.time())
start_date = 1072915200
end_date = current_timestamp

create_air_pollution_model(latitude, longitude, start_date, end_date, api_key, model_file_name)

