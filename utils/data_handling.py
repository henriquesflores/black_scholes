import sys
import numpy as np
import pandas as pd

from black_scholes import option

must_have_columns = { "ativo"             \
                    , "call_put"          \
                    , "direction"         \
                    , "tenor"             \
                    , "spot"              \
                    , "strike"            \
                    , "forward"           \
                    , "notional"          \
                    , "vol"               \
                    , "r_d"               \
                    , "r_f"               \
}

def split_bygroup(data: pd.DataFrame, col: str) -> list:
    return [x for _, x in data.groupby(col)]

def extract_option_params(data: pd.DataFrame) -> tuple:

    o = option( data.spot.to_numpy()          \
              , data.strike.to_numpy()        \
              , data.tenor.to_numpy() / 365   \
              , data.vol.to_numpy()           \
              , data.r_d.to_numpy()           \
              , data.r_f.to_numpy()           \
        )

    data = data.assign(sign = lambda x: [-1 if i == "Sell" else 1 for i in x.direction], 
                       signed_notional = lambda x: x.notional * x.sign)

    notional = data.signed_notional.to_numpy()

    names = data.ativo
    call_put = data.call_put
    buy_sell = data.direction

    new_index = [ x + "-" +  y + "-" + z for x, y, z in zip(names, call_put, buy_sell)]
    option_name = pd.Series(new_index, index = data.ativo.index)

    return o, notional, option_name

def delete_fake_callput(table: pd.DataFrame) -> pd.DataFrame:
    return table.iloc[:-2, :]

def add_fake_callput(table: pd.DataFrame) -> pd.DataFrame:
   
    fake = table.loc[0:1, :].copy()
    fake.loc[0, "call_put"] = "Call"
    fake.loc[1, "call_put"] = "Put"

    fake_table = pd.concat([table, fake], ignore_index = True) 
    return fake_table

def fetch_data_from_pickle(pickle_file: str) -> tuple:
   
    raw_data = pd.read_pickle(pickle_file)
    
    if not must_have_columns.issubset(raw_data):
        print("ERROR: Expected column names:")
        print(must_have_columns)
        sys.exit(1)

    complete_data = add_fake_callput(raw_data)
    splited_data  = split_bygroup(complete_data, "call_put")

    return splited_data[0], splited_data[1]

def fetch_data_from_excel(xlsx_file: str) -> tuple:
   
    raw_data = pd.read_excel(xlsx_file, engine = "openpyxl")

    if not must_have_columns.issubset(raw_data):
        print("ERROR: Expected column names:")
        print(must_have_columns)
        sys.exit(1)

    complete_data = add_fake_callput(raw_data)
    splited_data = split_bygroup(complete_data, "call_put")

    return splited_data[0], splited_data[1]
   
def generate_spot_interval(spots: np.ndarray, percentuals: np.ndarray) -> np.ndarray:
    """
    This function generates an (i, s) matrix (numpy.ndarray) where
    (s,) is the dimension of spots and (i,) is the dimension of percentuals.
    Each row of this matrix is the array of spots with the percentuals added.

    It makes sense to use (i, s) since numpy right aligns dimesions to
    perform broadcasting.
    """
    return spots + np.outer(percentuals, spots)

def make_forward(o: option) -> np.ndarray:
    return o.S * np.exp(- o.r * o.T)

def greek_to_dataframe(greek: np.ndarray, colnames: list, index: pd.Series):
    return pd.concat([index.reset_index(), pd.DataFrame(greek.T, columns = colnames)], axis = 1)

def consolidate_call_put_into_dataframe(call_greek: np.ndarray, 
                                        call_index: pd.Series, 
                                        put_greek: np.ndarray,
                                        put_index: pd.Series, 
                                        colnames: list) -> pd.DataFrame:

    call_greek_table = delete_fake_callput(
        greek_to_dataframe(call_greek, colnames, call_index) 
    )

    put_greek_table =  delete_fake_callput(
        greek_to_dataframe(put_greek, colnames, put_index) 
    ) 

    final_data = pd.concat([call_greek_table.set_index("index"), put_greek_table.set_index("index")], axis = 0)

    return final_data.sort_index().set_index(0)

