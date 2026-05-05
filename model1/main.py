import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import xarray as xr

from simulation import init_grid, update

# =========================
# LOAD DATA (NOAA NetCDF)
# =========================
ds = xr.open_dataset("data/wind.nc")

# ambil semua time series
u_all = ds['uwnd'].values  # (time, lat, lon)

# crop biar ringan
u_all = u_all[:, :100, :100]

# jumlah timestep
time_steps = u_all.shape[0]

# =========================
# INIT SIMULATION
# =========================
nx, ny = u_all.shape[1], u_all.shape[2]
C = init_grid(nx, ny)

# posisi sumber erupsi
source_x, source_y = nx // 2, ny // 2

# =========================
# VISUALISASI
# =========================
fig, ax = plt.subplots()

# pakai log scale biar terlihat jelas
img = ax.imshow(np.log1p(C), cmap='inferno', origin='lower')
cbar = plt.colorbar(img)
cbar.set_label("Konsentrasi Abu (log scale)")

# =========================
# ANIMASI
# =========================
def animate(t):
    global C

    # ambil angin dari data real
    u = u_all[t] * 2
    
    # normalisasi + scaling
    u = u / (np.max(np.abs(u)) + 1e-5) * 5  # scaling biar efek terasa

    # buat komponen Y (karena dataset cuma uwnd)
    v = np.roll(u, shift=1, axis=0)

    # update simulasi
    C = update(C, u, v)

    # erupsi berkelanjutan
    C[source_x, source_y] += 20

    # visual update (pakai log biar keliatan)
    img.set_array(np.log1p(C))
    img.set_clim(0, 4)

    ax.set_title(f"Simulasi Penyebaran Abu Vulkanik (Step {t})")

    return [img]

# =========================
# JALANKAN ANIMASI
# =========================
ani = FuncAnimation(
    fig,
    animate,
    frames=100,     # bisa kamu ubah (misalnya 200)
    interval=50
)

plt.tight_layout()
plt.show()