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
aqi_values = {city: np.random.randint(1, 6) for city in cities}

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

# Add markers for each city with color-coded AQI values
for city, aqi in aqi_values.items():
    folium.CircleMarker(location=get_coordinates(city), radius=10, color=colors[aqi], fill=True, fill_color=colors[aqi], fill_opacity=0.5, popup=f'{city}: AQI {aqi}').add_to(m)

# Display map
m

m.save("map2.html")
