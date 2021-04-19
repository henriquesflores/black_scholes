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
    params['S'] = 20.16
    params['K'] = 20.50
    params['T'] = 12 / 361
    params['v'] = 12.87 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0
    p, d, g = option_yield_metrics(params)

    dollar_gamma = NOTIONAL * g * params["S"] / 100
    
    print("Price = {:,.4f}".format(p))
    print("Delta = {:,.4f}".format(d))
    print("Gamma = {:,.4f}".format(g))
    print("Dollar gamma = {:,.1f}".format(dollar_gamma))

if __name__ == "__main__": main()
