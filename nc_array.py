import xarray as xr
import numpy as np

fpath_nc = r"C:\Users\jcmul\capstone2026\netcdf_files\ETOPO_2022_v1_15s_N45W105_surface.nc"

data = xr.open_dataset(fpath_nc)

lat = data["lat"].values
lon = data["lon"].values
z = data["z"].values

lat2d = lat[:, np.newaxis]
lon2d = lon[np.newaxis, :]

lat_grid = np.broadcast_to(lat2d, z.shape)
lon_grid = np.broadcast_to(lon2d, z.shape)

grid = np.stack((lon_grid, lat_grid, z), axis=-1)

print("Grid shape: ", grid.shape)
print("First point [lon, lat, height]: ", grid[0, 0])