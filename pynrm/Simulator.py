import numpy as np
import random
from .nrm import get_nrm
from .pedigree import pedigree


class Simulator:
    def __init__(self, male_k, female_k, h, w):
        self.pedigree = pedigree
        self.gen = 0
        self.male_k = male_k
        self.female_k = female_k
        self.h = h
        self.w = w

    def get_ebv(self, sire, dam):
        """
        Random generate ebv for an individual using ebv values of its sire and
        dam given heritability value for simulation

        :param dataframe pedigree: pedigree of animals
        :param int sire: sire id
        :param int dam: dam id
        :param float h: heritability
        :return: ebv
        :rtype: float
        :raises ValueError: if sire or dam is not non-negative
        """

        if sire < 0:
            raise ValueError('\'sire\' cannot be negative')
        if dam < 0:
            raise ValueError('\'dam\' cannot be negative')

        h_sqrt = np.sqrt(self.h)
        v = round(np.random.normal(0, 1), 3)
        w = round(np.random.normal(0, 1), 3)
        f = 0.5 * (
            get_nrm(self.pedigree, sire, sire)
            + get_nrm(self.pedigree, dam, dam)
            ) - 1

        ebv = 0.5 * (
            self.pedigree.iloc[sire].ebv
            + self.pedigree.iloc[dam].ebv
            )
        +v * h_sqrt * np.sqrt((1 - f) / 2)
        +w * np.sqrt(1 - self.h)

        return round(ebv, 3)

    def get_adjusted_ebv(self, top_k, candidate):
        """
        Adjust ebv to alleviate high inbreeding when selecting top k animals

        :param dataframe pedigree: pedigree of animals
        :param list top_k: list of selected animals
        :param list candidate: candidate id
        :param float w: penalty weight of inbreeding rate in between top k
        animals
        :return: adjusted_ebv
        :rtype: float
        """

        ebv = self.pedigree.iloc[candidate].ebv

        # if none selected as top k, then original ebv is used for scoring
        if len(top_k) == 0:
            return round(ebv, 3)

        # adjust ebv relative to top animals already selected
        sum_rel = 0
        for i in top_k:
            sum_rel += get_nrm(self.pedigree, i, candidate)
        avg_rel = sum_rel / len(top_k)

        adjusted_ebv = ebv * (1 - self.w * avg_rel)

        return round(adjusted_ebv, 3)

    def get_top_k(self, top_k, candidates, k):
        """
        Select top k animals

        :param list top_k: list of selected animals
        :param list candidates: list of all remaining candidates
        :param int k: number of animals to select
        :return: top_k
        :rtype: list
        :raises ValueError: if length of top_k exceeds k
        """

        if len(top_k) > k:
            raise ValueError('Length of \'top_k\' should not exceed k')

        # base case - top k animals selected
        if len(top_k) == k:
            return top_k

        # recursive case
        for i, candidate in enumerate(candidates):
            adjusted_ebv = self.get_adjusted_ebv(top_k, candidate)

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
        """
        Generate new generation of animals and return a new pedigree

        :param dataframe pedigree: pedigree of animals
        :param int gen: generation number to newly create
        :return: pedigree
        :rtype: dataframe
        """

        all_males = self.pedigree[self.pedigree['sex'] == 'M'].index.tolist()
        all_females = self.pedigree[self.pedigree['sex'] == 'F'].index.tolist()

        top_males = self.get_top_k([], all_males, self.male_k)
        top_females = self.get_top_k([], all_females, self.female_k)
        random.shuffle(top_females)

        self.gen += 1
        new_pedigree = pedigree

        for i in range(len(top_males)):
            sire = top_males[i]
            breed_ratio = int(self.female_k / self.male_k)
            female_group = top_females[breed_ratio * i:breed_ratio * (i + 1):]

            for j in range(len(female_group)):
                dam = top_females[j]
                ebv = self.get_ebv(sire, dam)

                for k in range(10):
                    new_animal = {
                        "gen": self.gen,
                        "sire": sire,
                        "dam": dam,
                        "ebv": ebv,
                        "sex": random.choices(["M", "F"])[0],
                    }
                    new_pedigree = new_pedigree.append(
                        new_animal,
                        ignore_index=True
                    )

        self.pedigree = new_pedigree

        return new_pedigree
