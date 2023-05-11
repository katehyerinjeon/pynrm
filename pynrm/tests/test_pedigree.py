import pandas as pd
import unittest
import pynrm.Pedigree as Pedigree


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.pedigree = Pedigree.Pedigree()

    def tearDown(self):
        self.pedigree = None

    def test_pedigree(self):
        with self.assertRaises(TypeError):
            Pedigree.Pedigree("not dataframe")

        self.assertEqual(self.pedigree.data.shape[1], 5, "expected 5 columns")
        self.assertEqual(self.pedigree.data[self.pedigree.data["sex"] == "M"].shape[0], 500, "expected 500 males")
        self.assertEqual(self.pedigree.data[self.pedigree.data["sex"] == "F"].shape[0], 500, "expected 500 females")
        self.assertEqual(self.pedigree.data["gen"][0], 0, "expected generation 0")
        self.assertTrue(pd.isna(self.pedigree.data["sire"][0]), "expected sire NA")
        self.assertTrue(pd.isna(self.pedigree.data["dam"][0]), "expected dam NA")

    def test_get_avg_ebv(self):
        with self.assertRaises(TypeError):
            self.pedigree.get_avg_ebv("not int")

        self.pedigree.data["ebv"] = 1.5
        self.assertEqual(self.pedigree.get_avg_ebv(0), 1.5, "expected average EBV 1.5")
