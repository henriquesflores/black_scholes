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

"""
    TODOs:
        - [x] Automate table generation: for all greeks
        - [x] Adjust notional signal if it's sold or bought
        - [x] Information about option type in greeks table
        - [ ] DataFrame to png
"""

def main():

    # interval = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25,30,40,50]) / 100
    interval = np.array([1, 2, 5, 7, 10]) / 100
    main_interval = np.concatenate((-np.flip(interval), 0, interval), axis = None)

    calls, puts = fetch_data_from_pickle("data.pickle")
    call_options, call_notionals, call_names = extract_option_params(calls)
    put_options, put_notionals, put_names = extract_option_params(puts)

    call_options.S = generate_spot_interval(call_options.S, main_interval)
    put_options.S = generate_spot_interval(put_options.S, main_interval)

    call_deltas = black_scholes_call_dollar_delta(call_notionals, call_options)
    put_deltas = black_scholes_put_dollar_delta(put_notionals, put_options)

    call_gammas = black_scholes_call_dollar_gamma(call_notionals, call_options)
    put_gammas = black_scholes_put_dollar_gamma(put_notionals, put_options)

    column_names = ["delta_{:}".format(x).replace("-", "n") for x in main_interval]
    table_delta = consolidate_call_put_into_dataframe(call_deltas, call_names, put_deltas, put_names, column_names)

    column_names = ["gamma_{:}".format(x).replace("-", "n") for x in main_interval]
    table_gamma = consolidate_call_put_into_dataframe(call_gammas, call_names, put_gammas, put_names, column_names)
    
    with pd.ExcelWriter("greeks.xlsx") as writer: 
        table_delta.to_excel(writer, sheet_name = "Delta")
        table_gamma.to_excel(writer, sheet_name = "Gamma")

if __name__ == "__main__": main()

