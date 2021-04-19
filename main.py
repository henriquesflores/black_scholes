#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Option

from scipy.stats import norm

FIXED_RATE = 3.8470 / 100 # (1.6 - 3.98) / 100
NOTIONAL = - 50_000_000

def make_forward(params: dict) -> dict:
    S = params['S']
    r = params['r']
    T = params['T']
    
    params['S'] = S * np.exp(-r * T)
    return params

def main():
#    data = pd.read_excel("Pasta1.xlsx", header = 1, engine = "openpyxl").iloc[0]
#    params = excel.extract_option_params(data, FIXED_RATE)

#   S = F e^{-rT}

    params = dict()
    params['S'] = 20.1809 
    params['K'] = 20.50
    params['T'] = 12 / 365
    params['v'] = 12.868 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0
    
    oparams = params.copy()
    params = make_forward(params)

    p1 = Option.Put(**params)
    delta_1 = p1.dollar_delta(NOTIONAL)
    gamma_1 = p1.dollar_gamma(NOTIONAL)

    print("{:,.2f}".format(delta_1))
    print("{:,.2f}".format(delta_1 + gamma_1))


if __name__ == "__main__": main()
