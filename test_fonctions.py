import re
import unittest
from data_extractor import Extracteur

class TestExtracteurMethods(unittest.TestCase):

    def test_extraire_espace_disque(self):
        # Test case 1
        line = "Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 10413 MB, 91.85% complet"
        expected_output = {'vol_disque': '/glimsdbf/', 'vol_disp_MB': '10413', 'vol_occup%': '91.85'}
        self.assertEqual(Extracteur.extraire_espace_disque(line), expected_output)

    def test_extraire_schema_area(self):
        # Test case 1
        lines = [
            "'Schema Area' (db glims) est presque plein (419998 blocks libres,  96.4 % utilisé)",
            "Il n'y a que 3281 MB libre dans cet environnement",
            "Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"
        ]
        expected_output = {
            "area": "db glims",
            "blk_libres": "419998",
            "area_occup%": "96.4",
            "area_MB_libres": "3281"
        }
        self.assertEqual(Extracteur.extraire_schema_area(lines), expected_output)

        # Add more test cases here if needed

if __name__ == '__main__':
    unittest.main()
