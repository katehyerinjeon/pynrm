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

    if i < 0:
        raise ValueError("'i' cannot be negative")
    if j < 0:
        raise ValueError("'j' cannot be negative")

    # swap i and j if i is larger than j
    if i > j:
        tmp = i
        i = j
        j = tmp

    # get sire and dam of j from the pedigree
    sire = pedigree.iloc[j].sire
    dam = pedigree.iloc[j].dam

    # diagonal - i and j is the same
    if i is not None and i == j:
        if sire is not None and dam is not None:
            res = 1 + 0.5 * get_nrm(sire, dam)
        else:
            res = 1

    # off-diagonal - i and j is not the same
    else:
        if sire is not None and dam is not None:
            res = 0.5 * (get_nrm(sire, i) + get_nrm(dam, i))
        elif sire is not None:
            res = 0.5 * get_nrm(sire, i)
        elif dam is not None:
            res = 0.5 * get_nrm(dam, i)
        else:
            res = 0

    return round(float(res), 3)
