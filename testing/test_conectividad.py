import unittest
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/perros_app"

DOG_API_BASE = "https://dog.ceo/api"
CAT_API_BASE = "https://api.thecatapi.com/v1"
OSM_API = "https://nominatim.openstreetmap.org/search"


class TestConnectivity(unittest.TestCase):

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

    def test_openstreetmap_connectivity(self):
        try:
            resp = requests.get(
                OSM_API,
                params={
                    "q": "Madrid",
                    "format": "json",
                    "limit": 1
                },
                headers={
                    "User-Agent": "pet-tracker-test"
                },
                timeout=5
            )

            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertTrue(isinstance(data, list))

        except Exception as e:
            self.fail(f"No se pudo conectar a OpenStreetMap: {e}")

        print("✅ Test conexión OpenStreetMap PASADO")


if __name__ == "__main__":
    unittest.main()