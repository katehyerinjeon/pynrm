import sys

sys.path.append('..')
import unittest
from pynrm import nrm
from pynrm import pedigree


class TestNrm(unittest.TestCase):
    def setUp(self):
        self.pedigree = pedigree.pedigree

    def tearDown(self):
        self.pedigree = None

    def test_get_nrm(self):
        self.assertEqual(nrm.get_nrm(self.pedigree, 0, 0), 1, 'wrong nrm value')


if __name__ == "__main__":
    unittest.main()
