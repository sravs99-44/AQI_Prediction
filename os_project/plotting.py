import matplotlib.pyplot as plt
import numpy as np

# Creating a 10x10 array
data = np.random.rand(10,10)

# Creating a heatmap using imshow()
plt.imshow(data, cmap='hot', interpolation='nearest')
plt.show()

# Output:
# A heatmap visualization of the data using Matplotlib
