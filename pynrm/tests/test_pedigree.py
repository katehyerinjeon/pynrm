import unittest
from pynrm.Pedigree import Pedigree


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.pedigree = Pedigree()

    def tearDown(self):
        self.simulator = None
