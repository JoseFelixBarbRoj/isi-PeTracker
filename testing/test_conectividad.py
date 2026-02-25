import unittest
from pathlib import Path
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

BACKEND_PATH = Path(__file__).parent.parent / "backend"
DATA_PATH = BACKEND_PATH / "inference" / "data"

EXPECTED_CAT_BREEDS = {
    "bengal": 180,
    "siamese": 180,
    "persian": 180,
    "ragdoll": 180,
    "maine_coon": 180,
    "british_shorthair": 180
}

CAT_LISTS = list(EXPECTED_CAT_BREEDS.keys())

DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/perros_app"

DOG_API_BASE = "https://dog.ceo/api"
CAT_API_BASE = "https://api.thecatapi.com/v1"

ALLOWED_DOG_BREEDS = {
    "labrador": [None],
    "bulldog": ["english", "french"],
    "retriever": ["golden", "chesapeake", "curly", "flatcoated"],
    "germanshepherd": [None],
    "beagle": [None],
    "boxer": [None],
    "doberman": [None],
    "husky": [None],
    "dachshund": [None],
    "pomeranian": [None],
    "poodle": ["standard", "miniature", "toy"],
    "chihuahua": [None],
    "spaniel": ["cocker", "irish"]
}


class TestBackend(unittest.TestCase):

    def test_database_connection(self):
        engine = create_engine(DATABASE_URI)
        try:
            conn = engine.connect()
            conn.close()
        except OperationalError as e:
            self.fail(f"No se pudo conectar a la base de datos: {e}")
        print("✅ Test conexión a base de datos PASADO")

    def test_dog_api_connectivity(self):
        try:
            resp = requests.get(f"{DOG_API_BASE}/breeds/list/all", timeout=5)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data["status"], "success")
        except Exception as e:
            self.fail(f"No se pudo conectar a la API de perros: {e}")
        print("✅ Test conexión API perros PASADO")

    def test_cat_api_connectivity(self):
        try:
            resp = requests.get(f"{CAT_API_BASE}/breeds", timeout=5)
            self.assertEqual(resp.status_code, 200)
        except Exception as e:
            self.fail(f"No se pudo conectar a la API de gatos: {e}")
        print("✅ Test conexión API gatos PASADO")

    def test_dog_images_count(self):
        for breed_dir in DATA_PATH.iterdir():
            if not breed_dir.is_dir():
                continue

            if breed_dir.name in CAT_LISTS:
                continue

            parts = breed_dir.name.split("-")
            breed = parts[0]
            sub_breed = parts[1] if len(parts) > 1 else None

            if breed not in ALLOWED_DOG_BREEDS:
                continue

            allowed_subs = ALLOWED_DOG_BREEDS[breed]

            if sub_breed not in allowed_subs:
                continue

            local_count = len(list(breed_dir.glob("*.png")))

            if sub_breed:
                url = f"{DOG_API_BASE}/breed/{breed}/{sub_breed}/images"
            else:
                url = f"{DOG_API_BASE}/breed/{breed}/images"

            api_resp = requests.get(url, timeout=10)
            self.assertEqual(api_resp.status_code, 200)

            api_data = api_resp.json()
            self.assertEqual(api_data["status"], "success")

            api_count = len(api_data["message"])

            self.assertEqual(
                local_count,
                api_count,
                f"{breed_dir.name}: locales={local_count}, api={api_count}"
            )

            print(f"✅ Test imágenes perro PASADO: {breed_dir.name}")

    def test_cat_images_count(self):
        for breed, expected_count in EXPECTED_CAT_BREEDS.items():
            breed_dir = DATA_PATH / breed
            self.assertTrue(breed_dir.exists(), f"No existe la carpeta de gato: {breed}")

            local_count = len(list(breed_dir.glob("*.png")))

            self.assertEqual(
                local_count,
                expected_count,
                f"{breed}: locales={local_count}, esperadas={expected_count}"
            )

            print(f"✅ Test imágenes gato PASADO: {breed}")


if __name__ == "__main__":
    unittest.main()