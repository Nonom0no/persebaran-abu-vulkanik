import numpy as np
from scipy.ndimage import gaussian_filter

def init_grid(nx, ny):
    C = np.zeros((nx, ny))
    C[nx//2, ny//2] = 100
    return C

def update(C, u, v, dt=0.2, dx=1, dy=1, D=0.2):
    C_new = C.copy()

    # advection lebih kuat
    C_new[1:-1,1:-1] -= dt * (
        u[1:-1,1:-1] * (C[1:-1,1:-1] - C[:-2,1:-1]) +
        v[1:-1,1:-1] * (C[1:-1,1:-1] - C[1:-1,:-2])
    )

    # difusi ringan
    from scipy.ndimage import gaussian_filter
    C_new = gaussian_filter(C_new, sigma=0.5)

    # jaga nilai
    C_new[C_new < 0] = 0

    C_new = np.clip(C_new, 0, 200)

    return C_new