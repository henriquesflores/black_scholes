#!usr/bin/env python3
import numpy as np
import pandas as pd

from black_scholes_functions import *
from utils.data_handling import *

pd.options.display.float_format = "{:,.2f}".format

NOTIONAL = - 50_000_000

def example() -> dict:

    params = dict()
    params['S'] = 20.1594
    params['K'] = 20.50
    params['T'] = 12 / 365
    params['v'] = 12.868 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0

    return params

def main():

    # interval = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25,30,40,50]) / 100
    interval = np.array([1, 2, 5, 7, 10]) / 100
    main_interval = np.concatenate((-np.flip(interval), 0, interval), axis = None)

    spots, strikes, times, vols, rs, qs = extract_option_params_from_pickle("data.pickle")
    spots_intervals = generate_spot_interval(spots, main_interval)

    deltas = black_scholes_put_delta(spots_intervals, strikes, times, vols, rs, qs)
    gammas = black_scholes_put_gamma(spots_intervals, strikes, times, vols, rs, qs)
    thetas = black_scholes_put_theta(spots_intervals, strikes, times, vols, rs, qs)
    vegas  = black_scholes_put_vega(spots_intervals, strikes, times, vols, rs, qs)
    rhos   = black_scholes_put_rho(spots_intervals, strikes, times, vols, rs, qs)

    print(pd.DataFrame(thetas.T, columns = ["theta_{:}".format(x).replace("-", "n") for x in main_interval]))
    print(pd.DataFrame(vegas.T,  columns = ["vega_{:}".format(x).replace("-", "n") for x in main_interval]))
    print(pd.DataFrame(rhos.T,   columns = ["rho_{:}".format(x).replace("-", "n") for x in main_interval]))

#    column_names = ["delta_{:}".format(x).replace("-", "n") for x in main_interval]
#    delta_table = pd.DataFrame(deltas.T, columns = column_names)
#    print(delta_table.head())
#
#    column_names = ["gamma_{:}".format(x).replace("-", "n") for x in main_interval]
#    gamma_table = pd.DataFrame(gammas.T, columns = column_names)
#    print(gamma_table.head())


if __name__ == "__main__": main()

