import numpy as np
import pandas as pd

from black_scholes_functions import option

def split_bygroup(data: pd.DataFrame, col: str) -> list:
    return [x for _, x in data.groupby(col)]

def extract_option_params(data: pd.DataFrame) -> tuple:

    o = option( data.spot.to_numpy()          \
              , data.strike.to_numpy()        \
              , data.tenor.to_numpy() / 365   \
              , data.vol.to_numpy()           \
              , data.r_d.to_numpy()           \
              , data.r_f.to_numpy()           )

    notional = data.notional.to_numpy()
    option_name = data.ativo

    return o, notional, option_name

def fetch_data_from_pickle(pickle_file: str) -> tuple:

    complete_data = pd.read_pickle(pickle_file)
    splited_data = split_bygroup(complete_data, "call_put")

    return splited_data[0], splited_data[1]

def fetch_data_from_excel(xlsx_file: str) -> tuple:

    complete_data = pd.read_excel(xlsx_file)
    splited_data = split_bygroup(complete_data, "call_put")

    return splited_data[0], splited_data[1]

def generate_spot_interval(spots: np.ndarray, percentuals: np.ndarray) -> np.ndarray:
    """
    This function generates an (i, s) matrix (numpy.ndarray) where
    (s,) is the dimension of spots and (i,) is the dimension of percentuals.
    Each row of this matrix is the array of spots with the percentuals added.

    It makes sense to use (i, s) since numpy right aligns dimesions to
    perform broadcasting.
    """
    return spots + np.outer(percentuals, spots)

def make_forward(S: np.ndarray, \
                 r: np.ndarray, \
                 T: np.ndarray) -> np.ndarray:
    return S * np.exp(- r * T)
