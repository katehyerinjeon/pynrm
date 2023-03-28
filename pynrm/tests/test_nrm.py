import unittest
from pynrm.nrm import get_nrm
from pynrm.Pedigree import Pedigree


class TestNrm(unittest.TestCase):
    def setUp(self):
        self.pedigree = Pedigree()

    def tearDown(self):
        self.pedigree = None

    def test_get_nrm(self):
        with self.assertRaises(TypeError):
            get_nrm("not dataframe", 0, 0)
        with self.assertRaises(TypeError):
            get_nrm(self.pedigree, "not int", 0)
        with self.assertRaises(TypeError):
            get_nrm(self.pedigree, 0, "not int")
        with self.assertRaises(ValueError):
            get_nrm(self.pedigree, -1, 0)
        with self.assertRaises(ValueError):
            get_nrm(self.pedigree, 0, -1)
        self.assertEqual(get_nrm(self.pedigree, 0, 0), 1, "wrong nrm value")


if __name__ == "__main__":
    unittest.main()
