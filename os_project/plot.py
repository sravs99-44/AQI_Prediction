import folium
import numpy as np


def get_coordinates(city):
    coordinates = {
        'New York': (40.7128, -74.0060),  # Latitude and longitude of New York City
        'Boston': (42.3601, -71.0589),    # Latitude and longitude of Boston
        'Philadelphia': (39.9526, -75.1652)  # Latitude and longitude of Philadelphia
    }
    return coordinates.get(city, (0, 0))  # Return coordinates of the city if found, otherwise (0, 0)


# Generate mock air quality data for New York, Boston, and Philadelphia
cities = ['New York', 'Boston', 'Philadelphia']
air_quality = {city: np.random.randint(0, 101) for city in cities}

# Create map centered on the United States
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add markers for current air quality
for city, aqi in air_quality.items():
    folium.Marker(location=get_coordinates(city), popup=f'Current AQI: {aqi}').add_to(m)

# Add markers for future predictions (mock data)
future_predictions = {city: np.random.randint(0, 101) for city in cities}
for city, aqi in future_predictions.items():
    folium.CircleMarker(location=get_coordinates(city), radius=10, color='red', fill=True, fill_color='red', fill_opacity=0.5, popup=f'Future AQI: {aqi}').add_to(m)

# Display map
m
m.save("map.html")

