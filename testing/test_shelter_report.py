import unittest
from io import BytesIO
from unittest.mock import patch

from backend.app import create_app, db, ShelterReport, LostReport


class TestShelterEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()   
        db.create_all()
        self.shelter_folder = self.app.config["SHELTER_UPLOAD_FOLDER"]

        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["account_type"] = "shelter"
            sess["nombre"] = "testshelter"

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # =========================
    # TEST /report
    # =========================

    @patch("backend.app.predict")
    def test_report_success(self, mock_predict):

        mock_predict.return_value = "labrador"

        data = {
            "imagen": (BytesIO(b"fake image"), "dog.png"),
            "latitud": "40.4",
            "longitud": "-3.7"
        }

        response = self.client.post(
            "/report",
            data=data,
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()

        self.assertIn("reporte_actual", json_data)
        self.assertIn("perdidos", json_data)
        self.assertIn("protegidos", json_data)

        # BD
        db_report = ShelterReport.query.first()
        self.assertIsNotNone(db_report)
        self.assertEqual(db_report.raza, "labrador")
        self.assertEqual(db_report.protectora, "testshelter")

        # Imagen guardada
        folder = self.shelter_folder / "testshelter"
        self.assertTrue(folder.exists())
        self.assertTrue(len(list(folder.glob("*.png"))) > 0)

        # Modelo llamado
        mock_predict.assert_called_once()

        print("✅ /report funciona correctamente")

    def test_report_requires_session(self):

        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.post("/report")

        self.assertEqual(response.status_code, 401)

        print("✅ /report requiere sesión")

    def test_report_requires_shelter(self):

        with self.client.session_transaction() as sess:
            sess["account_type"] = "user"

        response = self.client.post("/report")

        self.assertEqual(response.status_code, 403)

        print("✅ /report requiere cuenta de protectora")

    def test_report_requires_image(self):

        response = self.client.post("/report", data={
            "latitud": "40",
            "longitud": "-3"
        })

        self.assertEqual(response.status_code, 400)

        print("✅ /report requiere imagen")

    def test_report_requires_coordinates(self):

        data = {
            "imagen": (BytesIO(b"fake"), "dog.png")
        }

        response = self.client.post(
            "/report",
            data=data,
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)

        print("✅ /report requiere coordenadas")

    # =========================
    # TEST /shelter/maps
    # =========================

    def test_shelter_maps_success(self):

        # Insertar datos en BD
        db.session.add(ShelterReport(
            path_imagen="test.png",
            raza="labrador",
            latitud=40,
            longitud=-3,
            protectora="testshelter"
        ))

        db.session.add(LostReport(
            path_imagen="lost.png",
            raza="beagle",
            latitud=41,
            longitud=-4,
            username="user1"
        ))

        db.session.commit()

        response = self.client.get("/shelter/maps")

        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()

        self.assertIn("protegidos", json_data)
        self.assertIn("perdidos", json_data)

        self.assertEqual(len(json_data["protegidos"]), 1)
        self.assertEqual(len(json_data["perdidos"]), 1)

        print("✅ /shelter/maps devuelve datos correctamente")

    def test_shelter_maps_requires_session(self):

        with self.client.session_transaction() as sess:
            sess.clear()

        response = self.client.get("/shelter/maps")

        self.assertEqual(response.status_code, 401)

        print("✅ /shelter/maps requiere sesión")

    def test_shelter_maps_requires_shelter(self):

        with self.client.session_transaction() as sess:
            sess["account_type"] = "user"

        response = self.client.get("/shelter/maps")

        self.assertEqual(response.status_code, 403)

        print("✅ /shelter/maps requiere cuenta de protectora")


if __name__ == "__main__":
    unittest.main()