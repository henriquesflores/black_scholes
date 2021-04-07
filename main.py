#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Call
import Put

FIXED_RATE = 3.40 / 100 # (1.6 - 3.98) / 100
NOTIONAL = - 50_000_000

def main():
    data = pd.read_excel("Pasta1.xlsx", header = 1).iloc[0]
    params = excel.extract_option_params_from_excel(data, FIXED_RATE)

    c = Call.Call(**params)
    p = Put.Put(**params)

    p_dollar_delta = p.dollar_delta(NOTIONAL)
    p_dollar_gamma = p.dollar_gamma(NOTIONAL)
    p_dollar_theta = p.dollar_theta(NOTIONAL)
    p_dollar_vega  = p.dollar_vega(NOTIONAL)
    p_dollar_rho   = p.dollar_rho(NOTIONAL)

    print("Delta = {:,.2f}\nGamma = {:,.2f}\nVega = {:,.2f}\nTheta = {:,.2f}\nRho = {:,.2f}".format(p_dollar_delta, p_dollar_gamma, p_dollar_vega, p_dollar_theta, p_dollar_rho))


if __name__ == "__main__": main()


