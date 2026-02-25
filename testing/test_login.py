import unittest
from backend.app import app, db, User, Shelter


class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            if not User.query.filter_by(nombre="test_user").first():
                db.session.add(User(
                    nombre="test_user",
                    contraseña_hash="1234"
                ))

            if not Shelter.query.filter_by(nombre="test_shelter").first():
                db.session.add(Shelter(
                    nombre="test_shelter",
                    contraseña_hash="1234"
                ))

            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_user_success(self):
        response = self.client.post("/login", data={
            "nombre": "test_user",
            "password": "1234"
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/user", response.location)

        with self.client.session_transaction() as session:
            self.assertTrue(session.get("logged_in"))
            self.assertEqual(session.get("account_type"), "user")
            self.assertEqual(session.get("nombre"), "test_user")

        print("✅ Login usuario PASADO")

    def test_login_shelter_success(self):
        response = self.client.post("/login", data={
            "nombre": "test_shelter",
            "password": "1234"
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/shelter", response.location)

        with self.client.session_transaction() as session:
            self.assertTrue(session.get("logged_in"))
            self.assertEqual(session.get("account_type"), "shelter")
            self.assertEqual(session.get("nombre"), "test_shelter")

        print("✅ Login protectora PASADO")

    def test_login_failure(self):
        response = self.client.post("/login", data={
            "nombre": "no_existe",
            "password": "wrong"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

        print("✅ Login incorrecto PASADO")

    def test_login_empty_fields(self):
        response = self.client.post("/login", data={
            "nombre": "",
            "password": ""
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuario/Contraseña incorrectos".encode("utf-8"), response.data)

        print("✅ Login campos vacíos PASADO")


if __name__ == "__main__":
    unittest.main()