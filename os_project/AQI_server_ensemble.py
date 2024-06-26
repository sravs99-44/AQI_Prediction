import threading
import requests
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import VotingRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from catboost import CatBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
import time
import pickle
import sys
from sklearn.model_selection import train_test_split
import warnings
import matplotlib.pyplot as plt

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

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

        # Initialize base regressor models
        svr = SVR()
        rf = RandomForestRegressor()
        catboost = CatBoostRegressor(logging_level='Silent')  # Set logging level to silent
        knn = KNeighborsRegressor()
        adaboost = AdaBoostRegressor()
        xgboost = XGBRegressor()
        dt = DecisionTreeRegressor()

        # Create ensemble model
        model = VotingRegressor([
            ('rf', rf),
            ('catboost', catboost),
            ('knn', knn),
            ('adaboost', adaboost),
            ('xgboost', xgboost),
            ('dt', dt)  # Add Decision Tree
        ])
        

        # Train the model
        model.fit(X_train, y_train)

        # Save the model to a file
        with open(model_file_name, 'wb') as file:
            pickle.dump(model, file)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the predictions
        r2 = r2_score(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)
  
        print("R-square:", r2)
        print("RMSE:", rmse)
        print("MAE:", mae)

        # Plot actual vs. predicted values
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, y_pred, color='blue')
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
        plt.xlabel('Actual AQI')
        plt.ylabel('Predicted AQI')
        plt.title('Actual vs. Predicted AQI')
        plt.grid(True)
        plt.show()

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
        longitude = '-75.1652'
        model_file_name = "model_c2.pkl"
    elif city_name == "boston":
        latitude = '42.3601'
        longitude = '-71.0589'
        model_file_name = "model_c3.pkl"
    elif city_name == "washington":
        latitude = '38.9072'
        longitude = '-77.0369'
        model_file_name = "model_c4.pkl"
    elif city_name == "harrisburg":
        latitude = '40.2732'
        longitude = '-76.8867'
        model_file_name = "model_c5.pkl"
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
