import numpy as np
import pandas as pd
from Pedigree import Pedigree


def get_nrm(pedigree, i, j):
    """Calculates the numerator relationship matrix (NRM) value.

    Recursively computes the (i, j) value of NRM using information available from the pedigree provided.

    Args:
        pedigree: An instance of Pedigree class holding the recorded ancestry data.
        i: An integer indicating the row.
        j: An integer indicating the column.

    Returns:
        A float that corresponds to the (i, j) value of NRM.
    """

    if not isinstance(pedigree, Pedigree):
        raise TypeError("'pedigree' must be of type Pedigree")
    if i is not pd.NA and not isinstance(i, int) and not isinstance(i, np.int64):
        raise TypeError("'i' must be of type int")
    if j is not pd.NA and not isinstance(j, int) and not isinstance(i, np.int64):
        raise TypeError("'j' must be of type int")

    if i is not pd.NA and i < 0:
        raise ValueError("'i' cannot be negative")
    if j is not pd.NA and j < 0:
        raise ValueError("'j' cannot be negative")

    # swap i and j if i is larger than j
    if i is not pd.NA and j is not pd.NA and i > j:
        tmp = i
        i = j
        j = tmp

    # get sire and dam of j from the pedigree
    sire = pedigree.data.iloc[j].sire
    dam = pedigree.data.iloc[j].dam

    # diagonal - i and j is the same
    if i is not pd.NA and i == j:
        if sire is not pd.NA and dam is not pd.NA:
            res = 1 + 0.5 * get_nrm(pedigree, sire, dam)
        else:
            res = 1

    # off-diagonal - i and j is not the same
    else:
        if sire is not pd.NA and dam is not pd.NA:
            res = 0.5 * (get_nrm(pedigree, sire, i) + get_nrm(pedigree, dam, i))
        elif sire is not pd.NA:
            res = 0.5 * get_nrm(pedigree, sire, i)
        elif dam is not pd.NA:
            res = 0.5 * get_nrm(pedigree, dam, i)
        else:
            res = 0

    return round(float(res), 3)


def get_avg_inbreeding(pedigree, gen):
    """Returns the average inbreeding rate of a generation.

    Average inbreeding rate is calculated across the generation.

    Args:
        gen: An integer indicating the generation number.

    Returns:
        A float that corresponds to the average inbreeding rate of the given generation.
    """

    if not isinstance(pedigree, Pedigree):
        raise TypeError("'pedigree' must be of type Pedigree")
    if not isinstance(gen, int):
        raise TypeError("'gen' must be of type int")

    ids = pedigree.data.index[pedigree.data["gen"] == gen].tolist()
    if len(ids) == 0:
        raise ValueError("'gen' must be present in the 'pedigree'")

    sum_inbreeding = 0
    for i in ids:
        sum_inbreeding += get_nrm(pedigree, i, i) - 1
    avg_inbreeding = sum_inbreeding / len(ids)

    return round(avg_inbreeding, 3)
