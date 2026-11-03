import xarray as xr
import numpy as np

fpath_nc = r"C:\Users\jcmul\capstone2026\netcdf_files\ETOPO_2022_v1_15s_N45W105_surface.nc"

dataset = xr.open_dataset(fpath_nc)

print("VARIABLES:")
for varname in dataset.variables:
    print(varname)

print("VARIABLE INFO")
for varname, var in dataset.variables.items():
    print(f"\nVariable: {varname}")
    print(f"Dimensions: {var.dims}")
    print(f"Shape: {var.shape}")
    print(f"Data Type: {var.dtype}")
    print(f"Attributes: {var.attrs}")

print("\nDATA VARIABLES")
print(list(dataset.data_vars))

print("\nCOORDINATES")
print(list(dataset.coords))

