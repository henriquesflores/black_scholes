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
        - [ ] Automate table generation: for all greeks
        - [ ] Adjust notional signal if it's sold or bought
        - [ ] Information about option type in greeks table
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

    column_names = ["delta_{:}".format(x).replace("-", "n") for x in main_interval]
    call_delta_table = pd.concat([call_names.reset_index(), pd.DataFrame(call_deltas.T, columns = column_names)], axis = 1)
    put_delta_table = pd.concat([put_names.reset_index(), pd.DataFrame(put_deltas.T, columns = column_names)], axis = 1)
    
    what = pd.concat([call_delta_table.set_index("index"), put_delta_table.set_index("index")], axis = 0).sort_index()
    print(what)
"""
    with pd.ExcelWriter("greeks.xlsx") as writer: 
        delta_table.to_excel(writer, sheet_name = "Delta")
        gamma_table.to_excel(writer, sheet_name = "Gamma")

def main():
    data = pd.read_pickle("data.pickle")
    print(data.head())
"""
if __name__ == "__main__": main()

