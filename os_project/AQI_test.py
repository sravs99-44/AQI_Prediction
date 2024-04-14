import threading
import requests
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import time
import pickle
import sys
from sklearn.model_selection import train_test_split

def retrieve_data_and_train_model(lat, lon, start, end, api_key, model_file_name):
    try:
        # Retrieve data from the API
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()['list']
        
        # Process the data
        df = []
        for i in result:
            row = {}
            for j in i['components']:
                row[j] = i['components'][j]
            row['aqi'] = i['main']['aqi']
            row['dt'] = i['dt']
            df.append(row)
            
        df = pd.DataFrame(df)
        df = df.sort_values(by='dt', ascending=False)
        
        # Split data into features (X) and target variable (y)
        X = df.drop(columns=['aqi'])
        y = df['aqi']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Save the model to a file
        with open(model_file_name, 'wb') as file:
            pickle.dump(model, file)

        # Make predictions and evaluate accuracy
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error during API request: {e}")

def main():
    api_key = '227487d348e815512d9f1c997142adde'
    city_name = sys.argv[1]

    if city_name == "newyork":
        latitude = '40.7128'
        longitude = '-74.0060'
        model_file_name = "model_c1.pkl"
    elif city_name == "phildelphia":
        latitude = '39.9526'
        longitude = '75.1652'
        model_file_name = "model_c2.pkl"
    elif city_name == "boston":
        latitude = '42.3601'
        longitude = '71.0589'
        model_file_name = "model_c3.pkl"
    else:
        print("Invalid city name.")
        return

    current_timestamp = int(time.time())
    start_date = 1072915200  # Unix time for January 1st, 2004
    end_date = current_timestamp

    # Create threads for retrieving data and training the model
    thread = threading.Thread(target=retrieve_data_and_train_model, args=(latitude, longitude, start_date, end_date, api_key, model_file_name))
    thread.start()
    thread.join()

if __name__ == "__main__":
    main()
