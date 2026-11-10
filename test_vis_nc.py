import xarray as xr
import numpy as np
import pyvista as pv
from pyproj import Transformer

fpath_nc = r"C:\Users\jcmul\capstone2026\netcdf_files\ETOPO_2022_v1_15s_N45W105_surface.nc"
fpath_out_nc = (r"C:\Users\jcmul\capstone2026\nc_dataviz_output")

# for later: pass in 'xname' 'yname' and 'zname' variables, plus an optional 'dtvarname', for generalized input.
def get_nc_array(fpath_nc):
    fpath_nc = fpath_nc

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
    return grid

# create
def create_pyvista_grid(numpy_grid):
    # read in numpy grid, extract data, build a PyVista StructuredGrid with it, and return the resulting object.
    # longitude
    x = numpy_grid[:, :, 0]
    # latitude
    y = numpy_grid[:, :, 1]
    # elevation
    z = numpy_grid[:, :, 2]

    # print("X ARRAY:")
    # print("Shape:", x.shape)
    # print("Minimum:", np.nanmin(x))
    # print("Maximum:", np.nanmax(x))
    #
    # print("\nY ARRAY:")
    # print("Shape:", y.shape)
    # print("Minimum:", np.nanmin(y))
    # print("Maximum:", np.nanmax(y))
    #
    # print("\nZ ARRAY:")
    # print("Shape:", z.shape)
    # print("Minimum:", np.nanmin(z))
    # print("Maximum:", np.nanmax(z))

    # coordinate transformer
    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:5070",
        always_xy=True
    )

    # convert lat/lon into projected meters
    x_m, y_m = transformer.transform(x, y)

    # create structured grid
    pv_grid = pv.StructuredGrid(x_m, y_m, z)

    pv_grid["Elevation"] = z.ravel(order="F")

    # Print resulting grid information
    print("\nPYVISTA GRID:")
    print("Dimensions:", pv_grid.dimensions)
    print("Bounds:", pv_grid.bounds)
    print("Number of Points:", pv_grid.n_points)
    print("Number of Cells:", pv_grid.n_cells)

    return pv_grid

def visualize_interactive(vista_grid, elevation_exaggeration):

    # Make a copy of the grid to preserve original data
    modified_grid = vista_grid.copy(deep=True)
    modified_grid.points[:, 2] *= elevation_exaggeration

    # open PyVista StructuredGrid as a render in an interactive window
    plotter = pv.Plotter()
    plotter.add_mesh(
        # pass in grid
        modified_grid,
        # tieback to array reference name assigned earlier in create_pyvista_grid()
        scalars = "Elevation",
        # pick a color palate to use on map; replaces "color" from earlier iterations
        cmap = "RdBu_r",
        # minimum and maximum elevations colorbar uses to assign color values to points; uses dataset units (meters in this case)'
        clim = [-50, 2500],
        # show edges boolean
        show_edges=False,
        # configures legend for graphic
        scalar_bar_args = {"title": "Elevation (meters)"}
    )
    plotter.show()

def save_birdseye_png(vista_grid, fpath_out_nc):
    pass

def save_3d_png(vista_grid, fpath_out_nc):
    pass

def save_grid_data(vista_grid, fpath_out_nc):
    pass

if __name__ == "__main__":
    grid = get_nc_array(fpath_nc)
    pv_grid = create_pyvista_grid(grid)
    visualize_interactive(pv_grid, 10)
