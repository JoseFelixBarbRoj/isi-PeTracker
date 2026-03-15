from pathlib import Path

import requests
import zipfile
from tqdm.auto import tqdm


if __name__ == "__main__":

    DOWNLOAD_BLOCK_SIZE = 1024

    MODEL_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/best.pth'
    SHELTERS_URL = 'https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/download/0.1.0/shelters_uploads.zip'

    (MODEL_OUTFILE := Path('backend/inference/models/best.pth')).parent.mkdir(parents=True, exist_ok=True)
    SHELTERS_OUTFILE = Path('frontend/static/shelters_uploads.zip')

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

