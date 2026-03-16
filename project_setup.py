from pathlib import Path

import requests
import zipfile
from tqdm.auto import tqdm


if __name__ == "__main__":

    DOWNLOAD_BLOCK_SIZE = 1024

    MODEL_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/best.pth'
    SHELTERS_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/shelters_uploads.zip'
    UPLOADS_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/uploads.zip'
    ASSETS_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/assets.zip'
    (MODEL_OUTFILE := Path('backend/inference/models/best.pth')).parent.mkdir(parents=True, exist_ok=True)
    SHELTERS_OUTFILE = Path('frontend/static/shelters_uploads.zip')
    UPLOADS_OUTFILE = Path('frontend/static/uploads.zip')
    ASSETS_OUTFILE = Path('frontend/static/assets.zip')

    if not MODEL_OUTFILE.is_file():

        model_response = requests.get(MODEL_URL, stream=True)
        total_model_size = int(model_response.headers.get("content-length", 0))

        with(tqdm(total=total_model_size, unit="B", unit_scale=True) as progress_bar,
            open(MODEL_OUTFILE, "wb") as model_fd):
            for data in model_response.iter_content(DOWNLOAD_BLOCK_SIZE):
                progress_bar.update(len(data))
                model_fd.write(data)
    else:
        print(f"Model file already exists at {MODEL_OUTFILE}, skipping download.")

    if not (SHELTERS_OUTFILE.parent / "shelters_uploads").is_dir():
        shelters_response = requests.get(SHELTERS_URL, stream=True)
        total_shelters_size = int(shelters_response.headers.get("content-length", 0))

        with(tqdm(total=total_shelters_size, unit="B", unit_scale=True) as progress_bar,
            open(SHELTERS_OUTFILE, "wb") as shelters_fd):
            for data in shelters_response.iter_content(DOWNLOAD_BLOCK_SIZE):
                progress_bar.update(len(data))
                shelters_fd.write(data)

        with zipfile.ZipFile(SHELTERS_OUTFILE, 'r') as zip_ref:
            zip_ref.extractall(SHELTERS_OUTFILE.parent)

        SHELTERS_OUTFILE.unlink()
    else:
        print(f"Shelters file already exists at {SHELTERS_OUTFILE}, skipping download.")

    if not (UPLOADS_OUTFILE.parent / "uploads").is_dir():
        uploads_response = requests.get(UPLOADS_URL, stream=True)
        total_uploads_size = int(uploads_response.headers.get("content-length", 0))

        with(tqdm(total=total_uploads_size, unit="B", unit_scale=True) as progress_bar,
            open(UPLOADS_OUTFILE, "wb") as uploads_fd):
            for data in uploads_response.iter_content(DOWNLOAD_BLOCK_SIZE):
                progress_bar.update(len(data))
                uploads_fd.write(data)

        with zipfile.ZipFile(UPLOADS_OUTFILE, 'r') as zip_ref:
            zip_ref.extractall(UPLOADS_OUTFILE.parent)

        UPLOADS_OUTFILE.unlink()
    else:
        print(f"Uploads file already exists at {UPLOADS_OUTFILE}, skipping download.")

    if not (ASSETS_OUTFILE.parent / "assets").is_dir():
        assets_response = requests.get(ASSETS_URL, stream=True)
        total_uploads_size = int(assets_response.headers.get("content-length", 0))

        with(tqdm(total=total_uploads_size, unit="B", unit_scale=True) as progress_bar,
            open(ASSETS_OUTFILE, "wb") as assets_fd):
            for data in assets_response.iter_content(DOWNLOAD_BLOCK_SIZE):
                progress_bar.update(len(data))
                assets_fd.write(data)

        with zipfile.ZipFile(ASSETS_OUTFILE, 'r') as zip_ref:
            zip_ref.extractall(ASSETS_OUTFILE.parent)

        ASSETS_OUTFILE.unlink()
    else:
        print(f"Uploads file already exists at {ASSETS_OUTFILE}, skipping download.")




