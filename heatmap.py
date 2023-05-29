import numpy as np
import matplotlib.pyplot as plt

# Generate random data points and metric values
num_points = 100
print(num_points)
x = np.random.randint(0, 10, num_points)
y = np.random.randint(0, 10, num_points)
metric_values = np.random.rand(num_points)  # Random metric values between 0 and 1
# print(metric_values)
# Create a 10x10 grid for the heatmap
grid_size = 10
heatmap = np.zeros((grid_size, grid_size))

# Accumulate metric values for each grid cell
for i in range(num_points):
    heatmap[x[i], y[i]] += metric_values[i]

# Plot the heatmap
plt.imshow(heatmap, cmap='hot', interpolation='nearest')
plt.colorbar(label='Metric Value')
plt.title('Heatmap with Metric Values')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
