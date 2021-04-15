import pandas as pd
from datetime import date

def get_days_until_expire(series: pd.Series) -> int:
    """
        returns option days until expire

        receives pd.Series with the following dates:
            EXP          start date
    """
    timedelta = series["EXP"].date() - date.today()
    timedelta = timedelta.days
    if timedelta < 0:
        print("Option has already expired. Time difference is {:}".format(timedelta))
        return 0

    return timedelta / 252

def extract_option_params(series: pd.Series, r) -> dict:
    """
        returns dict with option attributes

        receives a pd.Series with the following fields:
            UNDL_PX        underlying price
            STRIKE         strike price
            SETT           expiry date
            EXP            start date
            VOL            implied volatility
    """
    days_to_expire = get_days_until_expire(series) 

    option_params = {}  
    option_params['S'] = series['UNDL_PX']
    option_params['K'] = series['STRIKE']
    option_params['T'] = days_to_expire
    option_params['r'] = r 
    option_params['v'] = series['VOL'] / 100 
   
    return option_params


