import matplotlib.pyplot as plt
import numpy as np
import random
from .nrm import get_nrm, get_avg_inbreeding
from .Pedigree import Pedigree


class Simulator:
    """Simulates reproductive cycles.

    Performs livestock breeding simulations that provide fine-grained control.

    Attributes:
        pedigree: An instance of Pedigree class holding the recorded ancestry data.
        male_k: An integer count of males to select on each reproduction.
        female_k: An integer count of females to select on each reproduction.
        h: A float indicating heritability value.
        w: A float indicating penalization weight for inbreeding while reproduction.
        gen: An integer indicating latest generation number starting from 0. Increments after each reproduction.
    """

    def __init__(self, pedigree, male_k, female_k, h, w):
        """Initializes the instance with pedigree and user-defined parameters.

        Args:
            pedigree: Defines the intial pedigree before simulation.
            male_k: Defines male_k value. Set throughout all simulations.
            female_k: Defines female_k value. Set throughout all simulations.
            h: Defines h value. Set throughout all simulations.
            w: Defines w value. Set throughout all simulations.
        """

        if not isinstance(pedigree, Pedigree):
            raise TypeError("'pedigree' must be of type Pedigree")
        if not isinstance(male_k, int):
            raise TypeError("'male_k' must be of type int")
        if not isinstance(female_k, int):
            raise TypeError("'female_k' must be of type int")
        if not isinstance(h, float):
            raise TypeError("'h' must be of type float")
        if not isinstance(w, float):
            raise TypeError("'w' must be of type float")

        if male_k < 0:
            raise ValueError("'male_k' cannot be negative")
        if female_k < 0:
            raise ValueError("'female_k' cannot be negative")
        if h < 0:
            raise ValueError("'h' cannot be negative")
        if w < 0:
            raise ValueError("'w' cannot be negative")

        self.pedigree = pedigree
        self.male_k = male_k
        self.female_k = female_k
        self.h = h
        self.w = w
        self.gen = 0

    def get_ebv(self, sire, dam):
        """Randomly generates EBV of an individual animal.

        EBV is computed using heritability, EBV and inbreeding coefficients of sire and dam. It first solves the
        square root of heritability and average of inbreeding coefficients of sire and dam derived from NRM. Then, it
        calculates some values, multiplies by random normal deviates, and adds them to the average of EBV of
        sire and dam.

        Args:
            sire: An integer indicating the sire id.
            dam: An integer indicating the dam id.

        Returns:
            A float that corresponds to the randomly generated EBV.
        """

        if sire < 0:
            raise ValueError("'sire' cannot be negative")
        if dam < 0:
            raise ValueError("'dam' cannot be negative")

        h_sqrt = np.sqrt(self.h)
        f = 0.5 * (get_nrm(self.pedigree, sire, sire) + get_nrm(self.pedigree, dam, dam)) - 1

        ebv = 0.5 * (self.pedigree.data.iloc[sire].ebv + self.pedigree.data.iloc[dam].ebv)
        +round(np.random.normal(0, 1), 3) * h_sqrt * np.sqrt((1 - f) / 2)
        +round(np.random.normal(0, 1), 3) * np.sqrt(1 - self.h)

        return round(ebv, 3)

    def get_adjusted_ebv(self, candidate, already_selected):
        """Computes adjusted EBV of the candidate.

        EBV is adjusted to alleviate high inbreeding when selecting top k animals. This is calculated by
        solving the average relationship between the candidate and already selected animals. EBV of the candidate
        is then penalized for the average relationship with the user-defined weight of the simulator.

        Args:
            candidate: An integer indicating the candidate id.
            already_selected: A list of already selected animals.

        Returns:
            A float that corresponds to the adjusted EBV of the candidate.
        """

        ebv = self.pedigree.data.iloc[candidate].ebv

        # if none selected as top k yet, then original EBV is used for scoring
        if len(already_selected) == 0:
            return round(ebv, 3)

        # adjust EBV relative to top animals already selected
        sum_rel = 0
        for i in already_selected:
            sum_rel += get_nrm(self.pedigree, i, candidate)
        avg_rel = sum_rel / len(already_selected)

        adjusted_ebv = ebv * (1 - self.w * avg_rel)

        return round(adjusted_ebv, 3)

    def get_top_k(self, top_k, candidates, k):
        """Selects top k animals

        Chooses top k animals recursively by picking the candidate with highest adjusted EBV on each iteration until
        there are k animals selected.

        Args:
            top_k: A list of already selected animals.
            candidates: A list of all remaining candidates excluding the already selected animals.
            k: Number of animals to select.

        Returns:
            A list of all selected animals so far. This is a list that contains already selected animals and the newly
            selected animal from this iteration.
        """

        if len(top_k) > k:
            raise ValueError("Length of 'top_k' should not exceed k")

        # base case - top k animals selected
        if len(top_k) == k:
            return top_k

        # print("Length of candidates:", len(candidates))
        # recursive case
        for i, candidate in enumerate(candidates):
            adjusted_ebv = self.get_adjusted_ebv(candidate, top_k)
            if i == 0:
                selected = candidate
                max_adjusted_ebv = adjusted_ebv
            else:
                if adjusted_ebv > max_adjusted_ebv:
                    selected = candidate
                    max_adjusted_ebv = adjusted_ebv

        top_k.append(selected)
        candidates.remove(selected)

        return self.get_top_k(top_k, candidates, k)

    def reproduce(self):
        """Produces the next generation of animals

        Selects males and females (male_k and female_k animals each) to reproduce and generates new animals. It also
        updates the latest generation number and pedigree of the simulator to reflect the new reproductive cycle.

        Returns:
            A dataframe consisting all animals before reproduction and newly bred animals.
        """

        # fetch all males and females from the latest generation
        curr_gen = self.pedigree.data[self.pedigree.data["gen"] == self.gen]
        all_males = curr_gen[curr_gen["sex"] == "M"].index.tolist()
        all_females = curr_gen[curr_gen["sex"] == "F"].index.tolist()

        # select top males and females to reproduce
        top_males = self.get_top_k([], all_males, self.male_k)
        # print("Get top {} males from {} done".format(self.male_k, len(all_males)))
        top_females = self.get_top_k([], all_females, self.female_k)
        # print("Get top {} females {} done".format(self.female_k, len(all_females)))

        # copy current pedigree data before reproduction and increment generation number
        new_pedigree_data = self.pedigree.data
        self.gen += 1

        for i in range(len(top_males)):
            sire = top_males[i]
            for j in range(len(top_females)):
                dam = top_females[j]
                ebv = self.get_ebv(sire, dam)
                new_pedigree_data.loc[len(new_pedigree_data.index)] = [
                    self.gen,
                    sire,
                    dam,
                    ebv,
                    random.choices(["M", "F"])[0],
                ]

        self.pedigree = Pedigree(new_pedigree_data)

        return new_pedigree_data

    def plot_inbreeding_by_gen(self):
        """Plot average inbreeding coefficients by generation.

        Average inbreeding coefficients by generation is calculated and displayed as a basic line graph. All
        generations that have been generated in a Simulator instance is displayed.
        """
        gen = list(range(0, self.gen + 1))
        avg_inbreeding = []

        for i in range(self.gen + 1):
            avg_inbreeding.append(get_avg_inbreeding(self.pedigree, i))

        plt.plot(gen, avg_inbreeding)
        plt.xticks(np.arange(0, self.gen + 1, 1))
        plt.xlabel("Generation")
        plt.ylabel("Inbreeding Coefficient")
        plt.title("Average Inbreeding Coefficient by Generation")
        plt.show()

    def plot_ebv_by_gen(self):
        """Plot average EBV by generation.

        Average EBV by generation is calculated and displayed as a basic line graph. All generations that have been
        generated in a Simulator instance is displayed.
        """
        gen = list(range(0, self.gen + 1))
        avg_ebv = []

        for i in range(self.gen + 1):
            avg_ebv.append(self.pedigree.get_avg_ebv(i))

        plt.plot(gen, avg_ebv)
        plt.xticks(np.arange(0, self.gen + 1, 1))
        plt.xlabel("Generation")
        plt.ylabel("Estimated Breeding Value")
        plt.title("Average Estimated Breeding Value by Generation")
        plt.show()

    def export_to_csv(self, filename):
        """Exports generated pedigree data as csv.

        Writes pedigree data that have been generated in a Simulator instance to a comma-separated values (csv) file.

        Args:
            filename: A name of the path object or file-like object to export to.
        """
        self.pedigree.data.to_csv(filename)
