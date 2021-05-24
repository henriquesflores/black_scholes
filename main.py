#!usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils.tables
import black_scholes
from utils.data_handling import *

pd.options.display.float_format = "{:,.2f}".format

EXCEL_OUTPUT_FILE = "greeks.xlsx"
MAIN_DIRECTORY = os.path.dirname(__file__)

def main(file: str) -> None:

    interval = np.array([1, 2, 5, 7, 10]) / 100
    main_interval = np.concatenate((-np.flip(interval), 0, interval), axis = None)
    
    calls, puts = fetch_data_from_excel(file)
    call_options, call_notionals, call_names = extract_option_params(calls)
    put_options, put_notionals, put_names = extract_option_params(puts)

    make_forward(call_options)
    make_forward(put_options)

    call_options.S = generate_spot_interval(call_options.S, main_interval)
    put_options.S = generate_spot_interval(put_options.S, main_interval)

    call_deltas = black_scholes.call_dollar_delta(call_notionals, call_options)
    put_deltas = black_scholes.put_dollar_delta(put_notionals, put_options)

    call_gammas = black_scholes.call_dollar_gamma(call_notionals, call_options)
    put_gammas = black_scholes.put_dollar_gamma(put_notionals, put_options)

    column_names = ["Delta {:}%".format(int(100 * x)) for x in main_interval]
    table_delta = consolidate_call_put_into_dataframe(call_deltas, call_names, put_deltas, put_names, column_names)
    table_delta.name = "table_delta"

    column_names = ["Gamma {:}%".format(int(100 * x)) for x in main_interval]
    table_gamma = consolidate_call_put_into_dataframe(call_gammas, call_names, put_gammas, put_names, column_names)
    table_gamma.name = "table_gamma"

    output_path = os.path.join(MAIN_DIRECTORY, "data", EXCEL_OUTPUT_FILE)
    with pd.ExcelWriter(output_path) as writer:
        table_delta.to_excel(writer, sheet_name = "Delta")
        table_gamma.to_excel(writer, sheet_name = "Gamma")
    
    p_delta = utils.tables.plot_table(table_delta)
    p_gamma = utils.tables.plot_table(table_gamma)
    
    utils.tables.save_table_heatmap(p_delta, os.path.join(MAIN_DIRECTORY, "data", "table_delta.png"))
    utils.tables.save_table_heatmap(p_gamma, os.path.join(MAIN_DIRECTORY, "data", "table_gamma.png"))
    plt.show()

if __name__ == "__main__": main(sys.argv[1])

