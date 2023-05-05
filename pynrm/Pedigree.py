import numpy as np
import pandas as pd


class Pedigree:
    """Holds pedigree data.

    Given a dataframe, validates and converts it to the form that Simulator class expects. If data not provided,
    randomly generates initial generation of 1000 animals with 500 males and females each.

    Attributes:
        data: A dataframe where each row contains information of an individual animal including generation, sire id,
            dam id, genetic value or estimated breeding value (EBV), and sex. Index of the row represents the id of
            each animal. Columns for ids of sire and dam have nullable integer datatype for when the information is
            unknown.
    """

    def __init__(self, data=None, male_size=500, female_size=500):
        """Initializes the instance with pedigree data.

        Args:
            data: Defines the pedigree data. Should be a dataframe instance that can be fed to create a new dataframe
                that Simulator class consumes. Defaults to None.
            male_size: An integer count of males to generate for initial generation when data is None. Defaults to 500.
            female_size: An integer count of females to generate for initial generation when data is None. Defaults to
                500.
        """

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
                    "ebv": np.random.normal(0, 1, size=male_size),
                    "sex": "M",
                }
            )
            female = pd.DataFrame(
                {
                    "gen": 0,
                    "sire": None,
                    "dam": None,
                    "ebv": np.random.normal(0, 1, size=female_size),
                    "sex": "F",
                }
            )
            data = pd.concat([male, female], ignore_index=True, copy=False)
            self.data = pd.DataFrame(data=data, columns=["gen", "sire", "dam", "ebv", "sex"]).astype(dtype=dtype)

    def get_avg_ebv(self, gen):
        """Returns the average EBV of a generation.

        Average EBV is computed across the generation.

        Args:
            gen: An integer indicating the generation number.

        Returns:
            A float that corresponds to the average EBV of the given generation.
        """

        if not isinstance(gen, int):
            raise TypeError("'gen' must be of type int")

        return round(self.data[self.data["gen"] == gen]["ebv"].mean(), 3)
