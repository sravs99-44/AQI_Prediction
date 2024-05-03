import folium
import numpy as np

def get_coordinates(city):
    coordinates = {
        'New York': (40.7128, -74.0060),      # Latitude and longitude of New York City
        'Boston': (42.3601, -71.0589),        # Latitude and longitude of Boston
        'Philadelphia': (39.9526, -75.1652),  # Latitude and longitude of Philadelphia
        'Harrisburg': (40.2732, -76.8867),    # Latitude and longitude of Harrisburg (corrected)
        'Washington D.C': (38.9072, -77.0369) # Latitude and longitude of Washington D.C (corrected)
    }
    return coordinates.get(city, (0, 0))

# Generate mock air quality data for New York, Boston, Philadelphia, Harrisburg, and Washington D.C.
cities = ['New York', 'Boston', 'Philadelphia', 'Harrisburg', 'Washington D.C']
aqi_values = {city: np.random.randint(1, 6) for city in cities}

aqi_values['NewYork'] = 5
aqi_values['Boston'] = 4
aqi_values['Harrisburg'] = 1

# Define AQI categories
aqi_categories = {
    1: 'Good',
    2: 'Fair',
    3: 'Moderate',
    4: 'Poor',
    5: 'Very Poor'
}

# Define colors for AQI values
colors = {
    1: 'green',
    2: 'yellow',
    3: 'orange',
    4: 'darkorange',
    5: 'red'
}

# Create a map centered on the United States
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add markers for each city with color-coded AQI values and popup information
for city, aqi in aqi_values.items():
    popup_content = f'{city}: AQI {aqi} ({aqi_categories[aqi]})'
    folium.CircleMarker(location=get_coordinates(city), radius=10, color=colors[aqi], fill=True, fill_color=colors[aqi], fill_opacity=0.5, popup=popup_content).add_to(m)

# Display map
m

m.save("map3.html")
