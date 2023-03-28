import numpy as np
import pandas as pd


class Pedigree:
    def __init__(self, data=None):
        dtype = {"gen": int, "sire": pd.Int64Dtype(), "dam": pd.Int64Dtype(), "ebv": float, "sex": str}

        if data is not None:
            if isinstance(data, pd.DataFrame):
                self.data = pd.DataFrame(data=data, columns=["gen", "sire", "dam", "ebv", "sex"]).astype(dtype=dtype)
            else:
                raise TypeError("'data' must be of type dataframe")
        else:
            male = pd.DataFrame(
                {
                    "gen": 0,
                    "sire": None,
                    "dam": None,
                    "ebv": np.random.normal(0, 1, size=500),
                    "sex": "M",
                }
            )
            female = pd.DataFrame(
                {
                    "gen": 0,
                    "sire": None,
                    "dam": None,
                    "ebv": np.random.normal(0, 1, size=500),
                    "sex": "F",
                }
            )
            data = male.append(female, ignore_index=True)
            self.data = pd.DataFrame(data=data, columns=["gen", "sire", "dam", "ebv", "sex"]).astype(dtype=dtype)
