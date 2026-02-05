from pathlib import Path
import time

import requests

import numpy as np
import cv2

BASE_URL = "https://dog.ceo/api"
DATASET_DIR = Path(__file__).parent
DATASET_DIR.mkdir(parents=True, exist_ok=True)

resp = requests.get(f"{BASE_URL}/breeds/list/all")
resp_json = resp.json()

if __name__ == "__main__":
    if resp_json["status"] != "success":
        raise RuntimeError("Failed to fetch breeds list.")
    
    all_breeds = []
    for breed, sub_breeds in resp_json["message"].items():
        if sub_breeds:
            for sub in sub_breeds:
                all_breeds.append(f"{breed}-{sub}")
        else:
            all_breeds.append(breed)
            
print(f"Total breeds found: {len(all_breeds)}")

SELECTED_BREEDS = [
    ("labrador", None),          # Labrador
    ("bulldog", "english"),      # English Bulldog
    ("bulldog", "french"),       # French Bulldog
    ("retriever", "golden"),     # Golden Retriever
    ("retriever", "chesapeake"), # Chesapeake Bay Retriever
    ("retriever", "curly"),      # Curly Retriever
    ("retriever", "flatcoated"), # Flat‑Coated Retriever
    ("germanshepherd", None),    # German Shepherd
    ("beagle", None),            # Beagle
    ("boxer", None),             # Boxer
    ("doberman", None),          # Doberman
    ("husky", None),             # Siberian Husky
    ("dachshund", None),         # Dachshund
    ("pomeranian", None),        # Pomeranian
    ("poodle", "standard"),      # Poodle (standard)
    ("poodle", "miniature"),     # Poodle (miniature)
    ("poodle", "toy"),           # Poodle (toy)
    ("chihuahua", None),         # Chihuahua
    ("spaniel", "cocker"),       # Cocker Spaniel
    ("spaniel", "irish")         # Irish Spaniel
]

print(f"Selected breeds ({len(SELECTED_BREEDS)}): {SELECTED_BREEDS}")

for breed, sub_breed in SELECTED_BREEDS:
    if sub_breed:
        url = f"{BASE_URL}/breed/{breed}/{sub_breed}/images"
    else:
        url = f"{BASE_URL}/breed/{breed}/images"
    
    print(f"Fetching images for {breed} ...")
    r = requests.get(url).json()
    if r["status"] != "success":
        print(f"  ⚠️ Skipped {breed}")
        continue

    img_urls = r["message"]
    print(f"  Found {len(img_urls)} images")

    breed_dir = DATASET_DIR / breed
    breed_dir.mkdir(exist_ok=True)

    for idx, img_url in enumerate(img_urls, start=1):
        try:
            img_resp = requests.get(img_url, stream=True)
            if img_resp.status_code != 200:
                print(f"    Failed to download {img_url}")
                continue

            arr = np.asarray(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                print(f"    Failed to decode {img_url}")
                continue

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            save_path = breed_dir / f"{idx}.png"
            cv2.imwrite(str(save_path), cv2.cvtColor(img, cv2.COLOR_RGB2BGR)) 
            print(f"    Saved {save_path}") 

        except Exception as e:
            print(f"    Failed {img_url}: {e}")
            
BASE_URL = "https://api.thecatapi.com/v1"
IMAGES_PER_BREED = 180          
IMAGES_PER_REQUEST = 20 
SELECTED_BREEDS = {
    "bengal": "beng",
    "siamese": "siam",
    "persian": "pers",
    "ragdoll": "ragd",
    "maine_coon": "mcoo",
    "british_shorthair": "bsho"
}

for breed_name, breed_id in SELECTED_BREEDS.items():
    print(f"\n🐾 Fetching images for {breed_name} ({breed_id})")

    breed_dir = DATASET_DIR / breed_name
    breed_dir.mkdir(exist_ok=True)

    downloaded = 0
    page = 0

    while downloaded < IMAGES_PER_BREED:
        params = {
            "breed_ids": breed_id,
            "limit": IMAGES_PER_REQUEST,
            "page": page,
            "order": "DESC"
        }

        resp = requests.get(
            f"{BASE_URL}/images/search",
            params=params
        )

        if resp.status_code != 200:
            print(f"  ⚠️ API error on page {page}")
            break

        images = resp.json()
        if not images:
            print("  ⚠️ No more images available")
            break

        for img_data in images:
            if downloaded >= IMAGES_PER_BREED:
                break

            img_url = img_data["url"]

            try:
                img_resp = requests.get(img_url, timeout=10)
                if img_resp.status_code != 200:
                    continue

                arr = np.asarray(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

                if img is None:
                    continue

                save_path = breed_dir / f"{downloaded + 1}.png"
                cv2.imwrite(str(save_path), img)

                downloaded += 1
                print(f"    Saved {save_path}")

            except Exception as e:
                print(f"    Failed {img_url}: {e}")

        page += 1
        time.sleep(0.25) 

print("✅ Dataset download complete!")