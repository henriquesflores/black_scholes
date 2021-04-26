import numpy as np 
import pandas as pd 

def extract_option_params_from_pickle(pickle_file: str) -> tuple:

    data = pd.read_pickle(pickle_file)

    S = data.spot.to_numpy()
    K = data.strike.to_numpy()
    T = data.tenor.to_numpy() / 365
    v = data.vol.to_numpy()
    r = data.r_d.to_numpy()
    q = data.r_f.to_numpy()

    return S, K, T, v, r, q

def extract_option_params_from_xlsx(xlsx_file: str) -> tuple:

    data = pd.read_excel(xlsx_file, engine = "openpyxl")

    S = data.spot.to_numpy()
    K = data.strike.to_numpy()
    T = data.tenor.to_numpy() / 365
    v = data.vol.to_numpy()
    r = data.r_d.to_numpy()
    q = data.r_f.to_numpy()

    return S, K, T, v, r, q

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
