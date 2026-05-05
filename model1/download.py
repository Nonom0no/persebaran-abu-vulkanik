import requests
import os
from tqdm import tqdm

def download_gfs():
    url = "https://psl.noaa.gov/thredds/fileServer/Datasets/ncep.reanalysis/surface_gauss/uwnd.10m.gauss.2020.nc"
    filename = "data/wind.nc"

    os.makedirs("data", exist_ok=True)

    # cek apakah file sudah ada (resume)
    if os.path.exists(filename):
        existing_size = os.path.getsize(filename)
    else:
        existing_size = 0

    headers = {"Range": f"bytes={existing_size}-"}

    response = requests.get(url, headers=headers, stream=True)

    total_size = int(response.headers.get("content-length", 0)) + existing_size

    mode = "ab" if existing_size > 0 else "wb"

    with open(filename, mode) as f, tqdm(
        total=total_size, initial=existing_size, unit="B", unit_scale=True
    ) as pbar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    print("Download selesai:", filename)