import unittest
import io
from unittest.mock import patch

from backend.app import app, db, LostReport


class TestPrediction(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret_key"

        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def login(self):
        """Crea una sesión simulada de usuario"""
        with self.client.session_transaction() as sess:
            sess["nombre"] = "test_user"
            sess["account_type"] = "user"
            sess["logged_in"] = True

    def fake_image(self):
        """Genera una imagen falsa para subir"""
        return (io.BytesIO(b"fake image data"), "test.jpg")

    @patch("backend.model.predict")
    def test_prediction_saves_image(self, mock_predict):
        mock_predict.return_value = "beagle"

        self.login()

        response = self.client.post(
            "/predict",
            data={
                "imagen": self.fake_image(),
                "latitud": "40.0",
                "longitud": "-3.0",
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)

        with app.app_context():
            report = LostReport.query.first()
            self.assertIsNotNone(report)
            self.assertEqual(report.raza, "beagle")

        print("✅ Predicción guarda imagen PASADO")

    @patch("backend.model.predict")
    def test_prediction_response_structure(self, mock_predict):
        mock_predict.return_value = "beagle"

        self.login()

        response = self.client.post(
            "/predict",
            data={
                "imagen": self.fake_image(),
                "latitud": "40.0",
                "longitud": "-3.0",
            },
            content_type="multipart/form-data"
        )

        data = response.get_json()

        self.assertIn("reporte_usuario", data)
        self.assertIn("protegidos_similares", data)

        print("✅ Predicción estructura respuesta PASADO")

    @patch("backend.model.predict")
    def test_model_predicts_allowed_breeds(self, mock_predict):
        allowed = [
            "beagle",
            "boxer",
            "chihuahua",
            "dalmatian",
            "french_bulldog"
        ]

        for breed in allowed:

            mock_predict.return_value = breed
            self.login()

            response = self.client.post(
                "/predict",
                data={
                    "imagen": self.fake_image(),
                    "latitud": "40.0",
                    "longitud": "-3.0",
                },
                content_type="multipart/form-data"
            )

            data = response.get_json()

            self.assertEqual(
                data["reporte_usuario"]["raza"],
                breed
            )

        print("✅ Predicción razas válidas PASADO")

    @patch("backend.model.predict")
    def test_same_breed_filtering(self, mock_predict):
        mock_predict.return_value = "beagle"

        self.login()

        response = self.client.post(
            "/predict",
            data={
                "imagen": self.fake_image(),
                "latitud": "40.0",
                "longitud": "-3.0",
            },
            content_type="multipart/form-data"
        )

        data = response.get_json()

        for r in data["protegidos_similares"]:
            self.assertEqual(r["raza"], "beagle")

        print("✅ Predicción filtrado misma raza PASADO")


if __name__ == "__main__":
    unittest.main()