import pandas as pd
import unittest
from pynrm.Pedigree import Pedigree


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.pedigree = Pedigree()

    def tearDown(self):
        self.pedigree = None

    def test_pedigree(self):
        with self.assertRaises(TypeError):
            Pedigree("wrong data type")

        self.assertEqual(self.pedigree.data.shape[1], 5, "expected 5 columns")
        self.assertEqual(self.pedigree.data[self.pedigree.data["sex"] == "M"].shape[0], 500, "expected 500 males")
        self.assertEqual(self.pedigree.data[self.pedigree.data["sex"] == "F"].shape[0], 500, "expected 500 females")
        self.assertEqual(self.pedigree.data["gen"][0], 0, "expected generation 0")
        self.assertTrue(pd.isna(self.pedigree.data["sire"][0]), "expected sire NA")
        self.assertTrue(pd.isna(self.pedigree.data["dam"][0]), "expected dam NA")
