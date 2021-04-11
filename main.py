#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Option

FIXED_RATE = 3.40 / 100 # (1.6 - 3.98) / 100
NOTIONAL = - 50_000_000

def main():
    data = pd.read_excel("Pasta1.xlsx", header = 1).iloc[0]
    params = excel.extract_option_params(data, FIXED_RATE)

    p = Option.Put(**params)
    print("Dollar delta = {:,.2f}".format(p.dollar_delta(NOTIONAL)))



if __name__ == "__main__": main()


