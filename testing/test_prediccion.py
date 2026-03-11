import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from backend.app import app, db, LostReport, UPLOAD_FOLDER


class TestPrediccion(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        self.ctx = app.app_context()
        self.ctx.push()

        db.create_all()

        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["account_type"] = "user"
            sess["nombre"] = "testuser"

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    @patch("backend.app.predict")
    def test_predict_endpoint(self, mock_predict):

        mock_predict.return_value = "labrador"

        data = {
            "imagen": (BytesIO(b"fake image data"), "dog.png"),
            "latitud": "40.4168",
            "longitud": "-3.7038"
        }

        response = self.client.post(
            "/predict",
            data=data,
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()

        self.assertIn("reporte_usuario", json_data)
        self.assertIn("protegidos_similares", json_data)

        report = json_data["reporte_usuario"]

        self.assertEqual(report["raza"], "labrador")
        self.assertEqual(report["username"], "testuser")

        db_report = LostReport.query.first()

        self.assertIsNotNone(db_report)
        self.assertEqual(db_report.raza, "labrador")
        self.assertEqual(db_report.username, "testuser")

        image_path = UPLOAD_FOLDER / "testuser"
        self.assertTrue(image_path.exists())

        saved_images = list(image_path.glob("*.png"))
        self.assertTrue(len(saved_images) > 0)

        mock_predict.assert_called_once()

        print("✅ Predicción completa PASADO")


    def test_predict_requires_session(self):

        with self.client.session_transaction() as sess:
            sess.clear()

        data = {
            "imagen": (BytesIO(b"fake"), "dog.png"),
            "latitud": "40",
            "longitud": "-3"
        }

        response = self.client.post(
            "/predict",
            data=data,
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 401)

        print("✅ Predicción sin sesión PASADO")


    def test_predict_requires_image(self):

        data = {
            "latitud": "40",
            "longitud": "-3"
        }

        response = self.client.post("/predict", data=data)

        self.assertEqual(response.status_code, 400)

        print("✅ Predicción sin imagen PASADO")


    def test_predict_requires_coordinates(self):

        data = {
            "imagen": (BytesIO(b"fake"), "dog.png")
        }

        response = self.client.post(
            "/predict",
            data=data,
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)

        print("✅ Predicción sin coordenadas PASADO")


if __name__ == "__main__":
    unittest.main()