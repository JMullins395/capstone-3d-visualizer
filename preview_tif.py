import rasterio
import numpy as np

fpath_tif = r"C:\Users\jcmul\capstone2026\geotiff_files\ETOPO_2022_v1_15s_N45W105_surface.tif"

dataset = rasterio.open(fpath_tif)

print(dataset.profile)
print(dataset.meta)