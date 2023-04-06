import unittest
from pynrm.Pedigree import Pedigree
from pynrm.Simulator import Simulator


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator(Pedigree(), 2, 4, 0.6, 0.2)

    def tearDown(self):
        self.simulator = None

    def test_simulator(self):
        with self.assertRaises(TypeError):
            Simulator("not dataframe", 2, 4, 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator(self.simulator.pedigree, "not int", 4, 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator(self.simulator.pedigree, 2, "not int", 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator(self.simulator.pedigree, 2, 4, "not float", 0.2)
        with self.assertRaises(TypeError):
            Simulator(self.simulator.pedigree, 2, 4, 0.6, "not float")
        with self.assertRaises(ValueError):
            Simulator(self.simulator.pedigree, -2, 4, 0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator(self.simulator.pedigree, 2, -4, 0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator(self.simulator.pedigree, 2, 4, -0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator(self.simulator.pedigree, 2, 4, 0.6, -0.2)

    def test_get_ebv(self):
        with self.assertRaises(ValueError):
            self.simulator.get_ebv(-1, 0)
        with self.assertRaises(ValueError):
            self.simulator.get_ebv(0, -1)

    def test_get_adjusted_ebv(self):
        ebv = round(self.simulator.pedigree.data.iloc[0].ebv, 3)
        self.assertEqual(self.simulator.get_adjusted_ebv(0, []), ebv, "incorrect adjusted ebv value")

    def test_get_top_k(self):
        best_ebv = self.simulator.pedigree.data.iloc[[1, 2, 3]][["ebv"]].idxmax()[0]
        self.assertEqual(
            self.simulator.get_top_k([], [1, 2, 3], 0),
            [],
            "not an empty list when k = 0",
        )
        self.assertEqual(
            self.simulator.get_top_k([], [1, 2, 3], 1),
            [best_ebv],
            "not a list with the best ebv when k = 1",
        )

    def test_reproduce(self):
        self.simulator.reproduce()
        self.assertEqual(self.simulator.gen, 1, "generation not incremented")


if __name__ == "__main__":
    unittest.main()
