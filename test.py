from utils.option import Call, Put

call_price_test = { 'answer' : 5.85       \
                  , 'S' : 65.0            \
                  , 'K' : 60.0            \
                  , 'T' : 30.0            \
                  , 'v' : 35.0            \
                  , 'r' : 2.493           \
                  , 'q' : 0               }

put_price_test = { 'answer' : 0.9         \
                 , 'S' : 62.0             \
                 , 'K' : 60.0             \
                 , 'T' : 30.0             \
                 , 'v' : 25.0             \
                 , 'r' : 1.62             \
                 , 'q' : 0                }

call_delta_test = { 'answer' : 0.2386     \
                  , 'S' : 150.0           \
                  , 'K' : 180.0           \
                  , 'T' : 350.0           \
                  , 'v' : 20.0            \
                  , 'r' : 2.493           \
                  , 'q' : 0               }

put_delta_test = { 'answer' : -0.4433     \
                 , 'S' : 20.0             \
                 , 'K' : 20.0             \
                 , 'T' : 50.0             \
                 , 'v' : 70.0             \
                 , 'r' : 2.493            \
                 , 'q' : 0                }

call_gamma_test = { 'answer' : 0.01       \
                  , 'S' : 15.0            \
                  , 'K' : 30.0            \
                  , 'T' : 35.0            \
                  , 'v' : 100.0           \
                  , 'r' : 2.493           \
                  , 'q' : 0               }

put_gamma_test = { 'answer' : 0.004       \
                 , 'S' : 220.0            \
                 , 'K' : 200.0            \
                 , 'T' : 50.0             \
                 , 'v' : 110.0            \
                 , 'r' : 2.493            \
                 , 'q' : 0                }

call_vega_test = { 'answer' : 0.014       \
                 , 'S' : 30.0             \
                 , 'K' : 30.0             \
                 , 'T' : 5.0              \
                 , 'v' : 40.0             \
                 , 'r' : 2.493            \
                 , 'q' : 0                }

put_vega_test = { 'answer' : 1.473        \
                , 'S' : 1000.0            \
                , 'K' : 1050.0            \
                , 'T' : 50.0              \
                , 'v' : 110.0             \
                , 'r' : 2.493             \
                , 'q' : 0                 }

call_theta_test = { 'answer' : -0.0002    \
                  , 'S' : 29.0            \
                  , 'K' : 30.0            \
                  , 'T' : 5.0             \
                  , 'v' : 10.0            \
                  , 'r' : 2.493           \
                  , 'q' : 0               }

put_theta_test = { 'answer' : -0.0522     \
                 , 'S' : 100.0            \
                 , 'K' : 150.0            \
                 , 'T' : 350.0            \
                 , 'v' : 110.0            \
                 , 'r' : 2.493            \
                 , 'q' : 0                }

call_rho_test = { 'answer' : 0.0          \
                , 'S' : 25.0              \
                , 'K' : 30.0              \
                , 'T' : 5.0               \
                , 'v' : 10.0              \
                , 'r' : 0.0               \
                , 'q' : 0                 }

put_rho_test = { 'answer' : -1.1078       \
               , 'S' : 100.0              \
               , 'K' : 150.0              \
               , 'T' : 350.0              \
               , 'v' : 110.0              \
               , 'r' : 5.0                \
               , 'q' : 0                  }

def example() -> dict:

    params = dict()
    params['S'] = 20.1594
    params['K'] = 20.50
    params['T'] = 12 / 365
    params['v'] = 12.868 / 100
    params['r'] = 3.847 / 100
    params['q'] = 0

    return params

def adjust_option_time(opt_param: dict):
    value = opt_param.get('T')
    opt_param['T'] = value / 365
    return opt_param

def adjust_option_vol(opt_param: dict):
    value = opt_param.get('v')
    opt_param['v'] = value / 100
    return opt_param

def adjust_option_interest(opt_param: dict):
    value = opt_param.get('r')
    opt_param['r'] = value / 100
    return opt_param

def adjust_all_params(opt_params: dict):
    opt = adjust_option_time(opt_params)
    opt = adjust_option_vol(opt)
    return adjust_option_interest(opt)

def run_tests(test_dict: dict, which):
    for test in test_dict.keys():
        params = test_dict[test]
       
        true_answer = params.pop('answer')
        adjusted_params = adjust_all_params(params)
        
        our_answer = getattr(which(**adjusted_params), test)()

        print("For {:}:\n\tTrue value = {:.2f}\n\tComp Value = {:.2f}".format(test, true_answer, our_answer))


def main():
    CALL_TESTS = { 'price' : call_price_test   \
                 , 'delta' : call_delta_test   \
                 , 'gamma' : call_gamma_test   \
                 , 'vega'  : call_vega_test    \
                 , 'theta' : call_theta_test   \
                 , 'rho'   : call_rho_test     }

    PUT_TESTS = { 'price' : put_price_test   \
                , 'delta' : put_delta_test   \
                , 'gamma' : put_gamma_test   \
                , 'vega'  : put_vega_test    \
                , 'theta' : put_theta_test   \
                , 'rho'   : put_rho_test     }

    run_tests(CALL_TESTS, Call)
    print("-----------------")
    run_tests(PUT_TESTS, Put)

if __name__ == "__main__": main()
