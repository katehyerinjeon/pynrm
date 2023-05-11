import unittest
from unittest import mock
import pynrm.Simulator as Simulator
import pynrm.Pedigree as Pedigree


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator.Simulator(Pedigree.Pedigree(), 2, 4, 0.6, 0.2)

    def tearDown(self):
        self.simulator = None

    def test_simulator(self):
        with self.assertRaises(TypeError):
            Simulator.Simulator("not dataframe", 2, 4, 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator.Simulator(self.simulator.pedigree, "not int", 4, 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator.Simulator(self.simulator.pedigree, 2, "not int", 0.6, 0.2)
        with self.assertRaises(TypeError):
            Simulator.Simulator(self.simulator.pedigree, 2, 4, "not float", 0.2)
        with self.assertRaises(TypeError):
            Simulator.Simulator(self.simulator.pedigree, 2, 4, 0.6, "not float")
        with self.assertRaises(ValueError):
            Simulator.Simulator(self.simulator.pedigree, -2, 4, 0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator.Simulator(self.simulator.pedigree, 2, -4, 0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator.Simulator(self.simulator.pedigree, 2, 4, -0.6, 0.2)
        with self.assertRaises(ValueError):
            Simulator.Simulator(self.simulator.pedigree, 2, 4, 0.6, -0.2)

    def test_get_ebv(self):
        with self.assertRaises(ValueError):
            self.simulator.get_ebv(-1, 0)
        with self.assertRaises(ValueError):
            self.simulator.get_ebv(0, -1)

    def test_get_adjusted_ebv(self):
        ebv = round(self.simulator.pedigree.data.iloc[0].ebv, 3)
        self.assertEqual(self.simulator.get_adjusted_ebv(0, []), ebv, "incorrect adjusted ebv value")

    def test_get_top_k(self):
        with self.assertRaises(ValueError):
            self.simulator.get_top_k([1, 2, 3], [1, 2, 3], 1)

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

    @mock.patch("%s.Simulator.plt" % __name__)
    def test_plot_inbreeding_by_gen(self, mock_plt):
        self.simulator.reproduce()
        self.simulator.plot_inbreeding_by_gen()
        mock_plt.title.assert_called_once_with("Average Inbreeding Coefficient by Generation")

    @mock.patch("%s.Simulator.plt" % __name__)
    def test_plot_ebv_by_gen(self, mock_plt):
        self.simulator.reproduce()
        self.simulator.plot_ebv_by_gen()
        mock_plt.title.assert_called_once_with("Average Estimated Breeding Value by Generation")

    def test_export_to_csv(self):
        with mock.patch.object(self.simulator.pedigree.data, "to_csv") as to_csv_mock:
            self.simulator.export_to_csv("pedigree.csv")
            to_csv_mock.assert_called_with("pedigree.csv")


if __name__ == "__main__":
    unittest.main()
