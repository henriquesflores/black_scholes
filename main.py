#!usr/bin/env python3
from Call import Call
from Put import Put

import pandas as pd

FIXED_RATE = 1.7180 / 100

def get_dt(series: pd.Series) -> int:
    """
        returns option days until expire

        receives pd.Series with the following dates:
            SETT         expiry date
            EXP          start date
    """
    timedelta = series["SETT"] - series["EXP"]
    return timedelta.days / 252

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
    option_params['PX'] = series['UNDL_PX']
    option_params['K']  = series['STRIKE']
    option_params['dT'] = days_to_expire
    option_params['r']  = FIXED_RATE 
    option_params['sigma'] = series['VOL'] /  100 
   
    return option_params

def main():
    test_data = pd.read_excel("Pasta1.xlsx", header = 1).iloc[0]
    op = extract_option_params_from_excel(test_data)
    put = Call(**op)
    print(put.delta() - 1)

if __name__ == "__main__": main()


