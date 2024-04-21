import numpy as np
import matplotlib.pyplot as plt

# Generate random AQI data for demonstration
num_locations = 100
aqi_values = np.random.randint(0, 500, num_locations)

# Generate random latitude and longitude coordinates
latitudes = np.random.uniform(-90, 90, num_locations)
longitudes = np.random.uniform(-180, 180, num_locations)

# Plot the heatmap
plt.figure(figsize=(10, 6))
plt.scatter(longitudes, latitudes, c=aqi_values, cmap='Reds', s=100, alpha=0.7)
plt.colorbar(label='AQI')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Air Quality Index Heatmap')
plt.grid(True)
plt.show()
