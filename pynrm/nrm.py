import pandas as pd
from .Pedigree import Pedigree


def get_nrm(pedigree, i, j):
    """
    Calculate nrm value of i-th row and j-th column

    :param dataframe pedigree: pedigree of animals
    :param int i: id of the first animal
    :param int j: id of the second animal (can be same as i)
    :return: nrm value of i-th rown and j-th column
    :rtype: float
    :raises ValueError: if i or j is not non-negative
    """

    if not isinstance(pedigree, Pedigree):
        raise TypeError("'pedigree' must be of type Pedigree")
    if i is not pd.NA and not isinstance(i, int):
        raise TypeError("'i' must be of type int")
    if j is not pd.NA and not isinstance(j, int):
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
