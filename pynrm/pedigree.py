import pandas as pd
import numpy as np

# random generate initial generation of 500 males and females each
male = pd.DataFrame({
    "gen": 0,
    "sire": None,
    "dam": None,
    "ebv": round(np.random.normal(0, 1, size=500), 3),
    "sex": "M"
})

female = pd.DataFrame({
    "gen": 0,
    "sire": None,
    "dam": None,
    "ebv": round(np.random.normal(0, 1, size=500), 3),
    "sex": "F"
})

# create a pedigree containing initial generation males and females
pedigree = male.append(female, ignore_index=True)
