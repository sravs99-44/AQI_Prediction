import requests
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import time
import pickle


def get_air_pollution_history(lat, lon, start, end, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"

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
        print(df.head())
        # Assuming 'df' is your DataFrame containing the data
        # Split the DataFrame into features (X) and target variable (y)
        X = df.drop(columns=['aqi'])  # Features (remove the target column)
        y = df['aqi']  # Target variable

        X_train = X[:-1]  # All rows except the last one for training
        X_test = X[-1:]   # Last row for testing
        y_train = y[:-1]  # All target values except the last one for training
        y_test = y[-1:]

        # Split the data into 90% training and 10% testing data
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/len(X), random_state=42)

        # Print the shapes of the training and testing data
        print("Training data shape (X_train, y_train):", X_train.shape, y_train.shape)
        print("Testing data shape (X_test, y_test):", X_test.shape, y_test.shape)

        # 2. Choose a Model
        model = DecisionTreeClassifier()

        # 3. Train the Model
        model.fit(X_train, y_train)

        with open('model_c1.pkl', 'wb') as file:
            pickle.dump(model, file)

        # 4. Make Predictions

        
        y_pred = model.predict(X_test)

        # Evaluate the predictions (optional)
        print("Air Quality index at this particular time:" , y_pred[0])
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
  
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error during API request: {e}")

# Replace 'YOUR_API_KEY', 'LATITUDE', 'LONGITUDE', 'START_DATE', and 'END_DATE' with your OpenWeatherMap API key, latitude, longitude, start date, and end date
api_key = '227487d348e815512d9f1c997142adde'
latitude = '40.7128'
longitude = '-74.0060'
start_date = 1388534400
current_timestamp = int(time.time())
end_date = current_timestamp

get_air_pollution_history(latitude, longitude, start_date, end_date, api_key)

