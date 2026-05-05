import xarray as xr
import numpy as np

def load_wind():
    ds = xr.open_dataset("data/wind.nc")

    # ambil 1 timestep
    u = ds['uwnd'][0].values

    # buat v dummy (sementara)
    v = np.roll(u, shift=1, axis=0) * 0.3

    # crop biar ringan
    u = u[:100, :100]
    v = v[:100, :100]

    return u, v