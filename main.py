#!usr/bin/env python3
import numpy as np
import pandas as pd
from datetime import date

from Call import Call
from Put import Put

FIXED_RATE = 3.40 / 100 # (1.6 - 3.98) / 100

def get_dt(series: pd.Series) -> int:
    """
        returns option days until expire

        receives pd.Series with the following dates:
            SETT         expiry date
            EXP          start date
    """
    timedelta = series["EXP"].date() - date.today()
    timedelta = timedelta.days
    if timedelta < 0:
        print("Option has already expired. Time difference is {:}".format(timedelta))
        return 0

    return timedelta / 252

def extract_option_params_from_excel(series: pd.Series) -> dict:
    """
        returns dict with option attributes

        receives a pd.Series with the following fields:
            UNDL_PX        underlying price
            STRIKE         strike price
            SETT           expiry date
            EXP            start date
            VOL            implied volatility
    """
    days_to_expire = get_dt(series) 

    option_params = {}  
    option_params['S'] = series['UNDL_PX']
    option_params['K']  = series['STRIKE']
    option_params['dT'] = days_to_expire 
    option_params['r']  = FIXED_RATE 
    option_params['sigma'] = series['VOL'] / 100 
   
    return option_params

def main():
    test_data = pd.read_excel("Pasta1.xlsx", header = 1).iloc[0]
    op = extract_option_params_from_excel(test_data)
    put = Put(**op)

    NOTIONAL = - 50_000_000
    dollar_gamma = 0.5 * put.gamma() * pow(put.S / 100, 2)
    print("Delta = {:,.3f}".format(put.delta()))
    print("Dollar Delta = {:,.0f}".format(NOTIONAL * put.delta()))
    print("Gamma = {:,.3f}".format(put.gamma()))
    print("Dollar Gamma = {:,.0f}".format(NOTIONAL * dollar_gamma))

if __name__ == "__main__": main()


