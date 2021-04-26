import numpy as np 
from scipy.stats import norm

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

