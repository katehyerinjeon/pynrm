import pandas as pd
import numpy as np

# random generate 0th generation of 10 males and females each
male0 = pd.DataFrame({"gen": 0, "sire": None ,"dam": None, "ebv": np.random.normal(0, 1, size=10), "sex": "M"})
female0 = pd.DataFrame({"gen": 0, "sire": None,"dam": None, "ebv": np.random.normal(0, 1, size=10), "sex": "F"})

# create a pedigree containing 0th generation
pedigree = male0.append(female0, ignore_index=True)

# calculate the nrm value for i-th row and j-th column
def get_nrm(i, j):
    if i > j:
        tmp = i; i = j; j = tmp

    sire = pedigree.iloc[j].sire
    dam = pedigree.iloc[j].dam

    # diagonal
    if i is not None and i == j:
        if sire is not None and dam is not None:
            res = 1 + 0.5 * get_nrm(sire, dam)
        else:
            res = 1

    # off-diagonal
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