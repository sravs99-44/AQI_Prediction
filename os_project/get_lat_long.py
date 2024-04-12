from geopy.geocoders import Nominatim



def get_lat_long(city, country):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None

city = "New York"
country = "USA"
latitude, longitude = get_lat_long(city, country)
if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Location not found.")
