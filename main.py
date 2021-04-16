#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Option

from scipy.stats import norm

FIXED_RATE = 3.8470 / 100 # (1.6 - 3.98) / 100
NOTIONAL = - 50_000_000

def option_yield_metrics(option_parameters: dict) -> tuple:
    s = option_parameters['S']
    k = option_parameters['K']
    v = option_parameters['v']
    t = option_parameters['T']
    r = option_parameters['r']
    q = option_parameters['q']

    d1 = 1 / (v * np.sqrt(t)) * (np.log(s / k) + (r - q + 0.5 * v * v) * t)
    d2 = d1 - v * np.sqrt(t)
    E = np.exp(- r * t)
    F = s * np.exp((r - q) * t)
    N1 = norm.cdf(-d1)
    N2 = norm.cdf(-d2) 
    price = E * (- F * N1 + k * N2) 
    delta = - np.exp(-q * t) * N1 
    gamma = - np.exp(-q * t) * norm.pdf(d1) / (s * v * np.sqrt(t))

    return price, delta, gamma


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
    
    print("Price = {:,.4f}".format(p))
    print("Delta = {:,.4f}".format(d))
    print("Gamma = {:,.4f}".format(g))


if __name__ == "__main__": main()

