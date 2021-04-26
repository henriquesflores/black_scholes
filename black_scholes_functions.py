from dataclasses import dataclass

import numpy as np
from scipy.stats import norm

@dataclass
class option:
    S: np.ndarray
    K: np.ndarray
    T: np.ndarray
    v: np.ndarray
    r: np.ndarray
    q: np.ndarray

def black_scholes_ds(o: option) -> tuple:
    denominator = o.v * np.sqrt(o.T)
    first_term  = np.log(o.S / o.K)
    second_term = o.r - o.q + o.v * o.v / 2

    d1 = (1 / denominator) * (first_term + second_term * o.T)
    d2 = d1 - denominator

    return d1, d2

def black_scholes_call_delta(o: option) -> np.ndarray:
    d1, d2 = black_scholes_ds(o)
    deltas = np.exp(- o.q * o.T) * norm.cdf(d1)
    return deltas

def black_scholes_call_gamma(o: option) -> np.ndarray:
    d1, _ = black_scholes_ds(o)
    g1 = np.exp(- o.q * o.T) * norm.pdf(d1)
    g2 = o.S * o.v * np.sqrt(o.T)
    return g1 / g2

def black_scholes_call_theta(o: option) -> np.ndarray:
    d1, d2 = black_scholes_ds(o)
    first_term  = - o.S * np.exp(-o.q * o.T) * norm.pdf(d1) * v / (2 * np.sqrt(o.T))
    second_term = - o.r * o.K * np.exp(-o.r * o.T) * norm.cdf(d2)
    third_term = o.q * o.S * np.exp(-o.q * o.T) * norm.cdf(d1)

    this_theta = first_term + second_term + third_term

    return this_theta / 100

def black_scholes_call_vega(o: option) -> np.ndarray:
    d1, _ = black_scholes_ds(o)
    this_vega = o.S * np.exp(-o.q * o.T) * norm.pdf(d1) * np.sqrt(o.T)
    return this_vega / 100

def black_scholes_call_rho(o: option) -> np.ndarray:
    _, d2 = black_scholes_ds(o)
    return o.K * np.exp(-o.r * o.T) * norm.cdf(d2) / 100

def black_scholes_call_dollar_delta(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_call_delta(o)

def black_scholes_call_dollar_gamma(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_call_gamma(o) * o.S / 100

def black_scholes_call_dollar_theta(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_call_theta(o)

def black_scholes_call_dollar_vega(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_call_vega(o)

def black_scholes_call_dollar_rho(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_call_rho(o)

def black_scholes_put_delta(o: option) -> np.ndarray:
    d1, _ = black_scholes_ds(o)
    deltas = np.exp(- o.q * o.T) * (norm.cdf(d1) - 1)
    return deltas

def black_scholes_put_gamma(o: option) -> np.ndarray:
    d1, _ = black_scholes_ds(o)
    g1 = np.exp(- o.q * o.T) * norm.pdf(d1)
    g2 = o.S * o.v * np.sqrt(o.T)
    return g1 / g2

def black_scholes_put_theta(o: option) -> np.ndarray:
    d1, d2 = black_scholes_ds(o)
    first_term  = - np.exp(o.q * o.T) * o.S * norm.pdf(d1) * o.v / (2 * np.sqrt(o.T))
    second_term = + o.r * o.K * np.exp(-o.r * o.T) * norm.cdf(-d2)
    third_term  = - o.q * o.S * np.exp(-o.q * o.T) * norm.cdf(-d1)

    this_theta = first_term + second_term + third_term

    return this_theta / 100

def black_scholes_put_vega(o: option) -> np.ndarray:
    d1, _ = black_scholes_ds(o)
    this_vega = o.S * np.exp(-o.q * o.T) * norm.pdf(d1) * np.sqrt(o.T)
    return this_vega / 100

def black_scholes_put_rho(o: option) -> np.ndarray:
    _, d2 = black_scholes_ds(o)
    return - o.K * np.exp(-o.r * o.T) * norm.cdf(-d2) / 100

def black_scholes_put_dollar_delta(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_put_delta(o)

def black_scholes_put_dollar_gamma(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_put_gamma(o) * o.S / 100

def black_scholes_put_dollar_theta(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_put_theta(o)

def black_scholes_put_dollar_vega(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_put_vega(o)

def black_scholes_put_dollar_rho(Notional: float, o: option) -> np.ndarray:
    return Notional * black_scholes_put_rho(o)


"""
def black_scholes_ds(S: np.ndarray, \
                     K: np.ndarray, \
                     T: np.ndarray, \
                     v: np.ndarray, \
                     r: np.ndarray, \
                     q: np.ndarray) -> tuple:

    denominator = v * np.sqrt(T)
    first_term  = np.log(S / K)
    second_term = r - q + v * v / 2

    d1 = (1 / denominator) * (first_term + second_term * T)
    d2 = d1 - denominator

    return d1, d2

def black_scholes_call_delta(S: np.ndarray, \
                             K: np.ndarray, \
                             T: np.ndarray, \
                             v: np.ndarray, \
                             r: np.ndarray, \
                             q: np.ndarray) -> np.ndarray:

    d1, d2 = black_scholes_ds(S, K, T, v, r, q)
    deltas = np.exp(- q * T) * norm.cdf(d1)
    return deltas

def black_scholes_call_gamma(S: np.ndarray, \
                             K: np.ndarray, \
                             T: np.ndarray, \
                             v: np.ndarray, \
                             r: np.ndarray, \
                             q: np.ndarray) -> np.ndarray:

    d1, d2 = black_scholes_ds(S, K, T, v, r, q)
    g1 = np.exp(- q * T) * norm.pdf(d1)
    g2 = S * v * np.sqrt(T)
    return g1 / g2

def black_scholes_call_theta(S: np.ndarray, \
                             K: np.ndarray, \
                             T: np.ndarray, \
                             v: np.ndarray, \
                             r: np.ndarray, \
                             q: np.ndarray) -> np.ndarray:

    d1, d2 = black_scholes_ds(S, K, T, v, r, q)
    first_term  = - S * np.exp(-q * T) * norm.pdf(d1) * v / (2 * np.sqrt(T))
    second_term = - r * K * np.exp(-r * T) * norm.cdf(d2)
    third_term = q * S * np.exp(-q * T) * norm.cdf(d1)

    this_theta = first_term + second_term + third_term

    return this_theta / 100

def black_scholes_call_vega(S: np.ndarray, \
                            K: np.ndarray, \
                            T: np.ndarray, \
                            v: np.ndarray, \
                            r: np.ndarray, \
                            q: np.ndarray) -> np.ndarray:

    d1, _ = black_scholes_ds(S, K, T, v, r, q)
    this_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
    return this_vega / 100

def black_scholes_call_rho(S: np.ndarray, \
                           K: np.ndarray, \
                           T: np.ndarray, \
                           v: np.ndarray, \
                           r: np.ndarray, \
                           q: np.ndarray) -> np.ndarray:

    _, d2 = black_scholes_ds(S, K, T, v, r, q)
    return K * np.exp(-r * T) * norm.cdf(d2) / 100

def black_scholes_call_dollar_delta(Notional: float, \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_call_delta(S, K, T, v, r, q)

def black_scholes_call_dollar_gamma(Notional: float, \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:

    return Notional * black_scholes_call_gamma(S, K, T, v, r, q) * S  / 100

def black_scholes_call_dollar_theta(Notional: float, \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_call_theta(S, K, T, v, r, q)

def black_scholes_call_dollar_vega(Notional: float, \
                                   S: np.ndarray,   \
                                   K: np.ndarray,   \
                                   T: np.ndarray,   \
                                   v: np.ndarray,   \
                                   r: np.ndarray,   \
                                   q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_call_vega(S, K, T, v, r, q)

def black_scholes_call_dollar_rho(Notional: float,  \
                                  S: np.ndarray,    \
                                  K: np.ndarray,    \
                                  T: np.ndarray,    \
                                  v: np.ndarray,    \
                                  r: np.ndarray,    \
                                  q: np.ndarray) -> np.ndarray:

    return Notional * black_scholes_call_rho(S, K, T, v, r, q)

def black_scholes_put_delta(S: np.ndarray, \
                            K: np.ndarray, \
                            T: np.ndarray, \
                            v: np.ndarray, \
                            r: np.ndarray, \
                            q: np.ndarray) -> np.ndarray:

    d1, d2 = black_scholes_ds(S, K, T, v, r, q)
    deltas = np.exp(- q * T) * (norm.cdf(d1) - 1)
    return deltas

def black_scholes_put_gamma(S: np.ndarray, \
                            K: np.ndarray, \
                            T: np.ndarray, \
                            v: np.ndarray, \
                            r: np.ndarray, \
                            q: np.ndarray) -> np.ndarray:

    d1, _ = black_scholes_ds(S, K, T, v, r, q)
    g1 = np.exp(- q * T) * norm.pdf(d1)
    g2 = S * v * np.sqrt(T)
    return g1 / g2

def black_scholes_put_theta(S: np.ndarray, \
                            K: np.ndarray, \
                            T: np.ndarray, \
                            v: np.ndarray, \
                            r: np.ndarray, \
                            q: np.ndarray) -> np.ndarray:

    d1, d2 = black_scholes_ds(S, K, T, v, r, q)
    first_term  = - np.exp(q * T) * S * norm.pdf(d1) * v / (2 * np.sqrt(T))
    second_term = + r * K * np.exp(-r * T) * norm.cdf(-d2)
    third_term  = - q * S * np.exp(-q * T) * norm.cdf(-d1)

    this_theta = first_term + second_term + third_term

    return this_theta / 100

def black_scholes_put_vega(S: np.ndarray, \
                           K: np.ndarray, \
                           T: np.ndarray, \
                           v: np.ndarray, \
                           r: np.ndarray, \
                           q: np.ndarray) -> np.ndarray:

    d1, _ = black_scholes_ds(S, K, T, v, r, q)
    this_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
    return this_vega / 100

def black_scholes_put_rho(S: np.ndarray, \
                          K: np.ndarray, \
                          T: np.ndarray, \
                          v: np.ndarray, \
                          r: np.ndarray, \
                          q: np.ndarray) -> np.ndarray:

    _, d2 = black_scholes_ds(S, K, T, v, r, q)
    return - K * np.exp(-r * T) * norm.cdf(-d2) / 100

def black_scholes_put_dollar_delta(Notional: float,  \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_put_delta(S, K, T, v, r, q)

def black_scholes_put_dollar_gamma(Notional: float,  \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:

    return Notional * black_scholes_put_gamma(S, K, T, v, r, q) * S  / 100

def black_scholes_put_dollar_theta(Notional: float,  \
                                    S: np.ndarray,   \
                                    K: np.ndarray,   \
                                    T: np.ndarray,   \
                                    v: np.ndarray,   \
                                    r: np.ndarray,   \
                                    q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_put_theta(S, K, T, v, r, q)

def black_scholes_put_dollar_vega(Notional: float,  \
                                   S: np.ndarray,   \
                                   K: np.ndarray,   \
                                   T: np.ndarray,   \
                                   v: np.ndarray,   \
                                   r: np.ndarray,   \
                                   q: np.ndarray) -> np.ndarray:
    return Notional * black_scholes_put_vega(S, K, T, v, r, q)

def black_scholes_put_dollar_rho(Notional: float,   \
                                  S: np.ndarray,    \
                                  K: np.ndarray,    \
                                  T: np.ndarray,    \
                                  v: np.ndarray,    \
                                  r: np.ndarray,    \
                                  q: np.ndarray) -> np.ndarray:

    return Notional * black_scholes_put_rho(S, K, T, v, r, q)
"""
