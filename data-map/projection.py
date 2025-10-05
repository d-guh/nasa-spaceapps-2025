import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap

# Load your CSV
df = pd.read_csv("filtered_open_flowers.csv")

# Load Blue Marble image
img_path = "world.200404.3x5400x2700.jpg"
img = plt.imread(img_path)

# Create figure
fig, ax = plt.subplots(figsize=(12,6))

# Basemap with Robinson projection (similar to Blue Marble)
m = Basemap(projection='robin', lon_0=0, resolution='c', ax=ax)

# Draw background image (Blue Marble)
# Basemap expects image in (lon, lat) range: (-180,180),(-90,90)
m.imshow(img, origin='upper', extent=[-180, 180, -90, 90])

# Convert lat/lon to map projection coordinates
x, y = m(df['decimalLongitude'].values, df['decimalLatitude'].values)

# Create a 2D histogram for heatmap
heatmap, xedges, yedges = np.histogram2d(x, y, bins=[500, 250])

# Plot heatmap
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
cmap = plt.cm.hot
ax.imshow(heatmap.T, extent=extent, origin='lower', cmap=cmap, alpha=0.6)

# Optional: overlay points
ax.scatter(x, y, color='blue', s=10, alpha=0.5)

# Remove axes
ax.axis('off')

plt.show()
