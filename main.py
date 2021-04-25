#!usr/bin/env python3
import numpy as np
import pandas as pd

from utils import *
import Option

FIXED_RATE = 3.8470 / 100 
NOTIONAL = - 50_000_000

def make_forward(params: dict) -> dict:
    """
    S = F e^{-rT} 
    """
    S = params['S']
    r = params['r']
    T = params['T']
    
    params['S'] = S * np.exp(-r * T)
    return params

def example() -> dict:

    params = dict()
    params['S'] = 20.1809 
    params['K'] = 20.50
    params['T'] = 12 / 365
    params['v'] = 12.868 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0

    return params

def generate_options(data: pd.DataFrame) -> list:
    option_data_names = ["option_type", "Forward", "Spot", "Strike", "Tenor", "Vol", "r_d", "r_f"]
    if not set(option_data_names).issubset(data.columns):
        return pd.DataFrame()

    option_type = data.loc[:, option_data_names.pop(0)]
    option_parameters = [None] * data.shape[0]
    for index, row in data.iterrows():
        a = row[option_data_names].to_dict()
        print(a)
        option_parameters[index] = a

    return option_parameters


def main():
    data = pd.read_excel("./data/plan_base.xlsx", engine = "openpyxl")
    data.columns = data.columns.str.replace("Call/Put", "option_type")
    notional = data.assign(sign = lambda x: [1 if i == "Sell" else -1 for i in x.Direction]) \
                   .assign(notional = lambda x: x.sign * x.Notional)                         \
                   .loc[:, "notional"]                                                       \
                   .to_numpy()

    ndata = generate_options(data)

    print(notional)
   
   
if __name__ == "__main__": main()
