import unittest


DOG_BREEDS = [
    "bulldog","boxer","spaniel","beagle","poodle","pomeranian",
    "retriever","dachshund","labrador","husky","doberman","chihuahua"
]

CAT_BREEDS = [
    "ragdoll","siamese","maine_coon","persian","bengal","british_shorthair"
]


def filter_reports(data, species="all", max_distance=None):

    def species_filter(r):
        if species == "all":
            return True
        if species == "Perro":
            return r["raza"] in DOG_BREEDS
        if species == "Gato":
            return r["raza"] in CAT_BREEDS

    def distance_filter(r):
        if max_distance is None:
            return True
        return r["distancia_km"] <= max_distance

    perdidos = [
        r for r in data["perdidos"]
        if species_filter(r) and distance_filter(r)
    ]

    protegidos = [
        r for r in data["protegidos"]
        if species_filter(r) and distance_filter(r)
    ]

    return perdidos, protegidos


class TestFrontendLogic(unittest.TestCase):

    def setUp(self):

        self.backend_data = {
            "reporte_actual":{
                "latitud":40.4,
                "longitud":-3.7,
                "raza":"labrador"
            },
            "perdidos":[
                {"raza":"labrador","distancia_km":1},
                {"raza":"siamese","distancia_km":2},
                {"raza":"beagle","distancia_km":15},
                {"raza":"ragdoll","distancia_km":30}
            ],
            "protegidos":[
                {"raza":"bulldog","distancia_km":5},
                {"raza":"persian","distancia_km":8},
                {"raza":"boxer","distancia_km":20}
            ]
        }

    def test_species_classification(self):

        self.assertIn("labrador", DOG_BREEDS)
        self.assertIn("siamese", CAT_BREEDS)

        print("✅ Clasificación de especies correcta")


    def test_filter_dogs(self):

        perdidos, protegidos = filter_reports(self.backend_data, species="Perro")

        self.assertEqual(len(perdidos), 2)
        self.assertEqual(len(protegidos), 2)

        print("✅ Filtro por especie Perro correcto")


    def test_filter_cats(self):

        perdidos, protegidos = filter_reports(self.backend_data, species="Gato")

        self.assertEqual(len(perdidos), 2)
        self.assertEqual(len(protegidos), 1)

        print("✅ Filtro por especie Gato correcto")


    def test_filter_distance(self):

        perdidos, protegidos = filter_reports(self.backend_data, max_distance=10)

        self.assertEqual(len(perdidos), 2)
        self.assertEqual(len(protegidos), 2)

        print("✅ Filtro por distancia correcto")


    def test_map_marker_count(self):

        perdidos, protegidos = filter_reports(self.backend_data)

        total_markers = 1 + len(perdidos) + len(protegidos)  

        self.assertEqual(total_markers, 8)

        print("✅ Número de marcadores en mapa correcto")


if __name__ == "__main__":
    unittest.main()