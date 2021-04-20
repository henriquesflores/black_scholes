#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Option

from scipy.stats import norm

FIXED_RATE = 3.8470 / 100 # (1.6 - 3.98) / 100
NOTIONAL = - 50_000_000
NOTIONAL = 100 

def main():
#    data = pd.read_excel("Pasta1.xlsx", header = 1, engine = "openpyxl").iloc[0]
#    params = excel.extract_option_params(data, FIXED_RATE)
#    p = Option.Put(**params)
#    pdel = p.delta()

    params = dict()
    params['S'] = 20.1594
    params['K'] = 20.50
    params['T'] = 12 / 365
    params['v'] = 12.868 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0

    p = Option.Put(**params)
    Dg=p.dollar_gamma(NOTIONAL)
    Dd=p.dollar_delta(NOTIONAL)


    print(p.greeks())
    print("Dolgar Gamma - " + str(Dg))
    print("Dolgar Delta - " + str(Dd))

if __name__ == "__main__": main()
