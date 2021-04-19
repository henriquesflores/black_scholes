from __future__ import annotations

import numpy as np
from scipy.stats import norm

class Call: 
    RHO_NORMALIZATION   = 1 / 100
    VEGA_NORMALIZATION  = 1 / 100
    THETA_NORMALIZATION = 1 / 252

    __slots__ = ('S', 'K', 'T', 'v', 'r', 'q')
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update_spot(self: Call, S: float) -> Call: 
        self.S = S
        return self 

    @staticmethod
    def scale(factor: float, number: float) -> float:
        return factor * number 

    def __ds(self: Call) -> tuple:
        """
        returns d1, d2 of Black and Scholes solution

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        sigma_term = self.v * np.sqrt(self.T)
        log_term   = np.log(self.S / self.K)
        interest_term = self.r - self.q
        drift_term = (interest_term + self.v * self.v / 2) 
        
        d1 = (1 / sigma_term) * (log_term + drift_term * self.T)
        d2 = d1 - sigma_term
    
        return d1, d2

    def price(self: Call) -> float:
        """
        returns price of call option

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, d2 = self.__ds() 
        return norm.cdf(d1) * self.S * np.exp(-self.q * self.T) - norm.cdf(d2) * self.K * np.exp(-self.r * self.T)

    def delta(self: Call) -> float:
        """
        returns delta of call option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, _ = self.__ds() 
        return np.exp(-self.q * self.T) * norm.cdf(d1)
 
    def gamma(self: Call) -> float:
        """
        returns gamma of call option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, _ = self.__ds()
        return np.exp(-self.q * self.T) * norm.pdf(d1) / (self.S * self.v * np.sqrt(self.T))

    def theta(self: Call) -> float:
        """
        returns theta of call option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, d2 = self.__ds() 
        first_term  = - self.S * np.exp(-self.q * self.T) * norm.pdf(d1) * self.v / (2 * np.sqrt(self.T))
        second_term = - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        third_term = self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(d1)

        this_theta = first_term + second_term + third_term

        return Call.scale(Call.THETA_NORMALIZATION, this_theta)

    def vega(self: Call) -> float:
        """
        returns vega of call option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """

        d1, _ = self.__ds()
        this_vega = self.S * np.exp(-self.q * self.T) * norm.pdf(d1) * np.sqrt(self.T)
        return Call.scale(Call.VEGA_NORMALIZATION, this_vega)

    def rho(self: Call) -> float:
        """
        returns rho of call option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        _, d2 = self.__ds() 
        return Call.scale(Call.RHO_NORMALIZATION, self.K * np.exp(-self.r * self.T) * norm.cdf(d2))

    def greeks(self: Call) -> None:
        """
        prints to stdout the price and greeks of option

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        option_data = { 'delta' : self.delta(),           \
                        'gamma' : self.gamma(),           \
                        'theta' : self.theta(),           \
                        'vega'  : self.vega(),            \
                        'rho'   : self.rho()              }
        
        for k, v in option_data.items():
            print("{:} = {:.2f}".format(k, v))

        return None 

    def dollar_delta(self: Call, Notional: float) -> float:
        """
        returns dollar delta for a given Notional 

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Notional * self.delta() 

    def dollar_gamma(self: Call, Notional: float) -> float:
        """
        returns dollar gamma for a given Notional 

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Notional * self.gamma() * self.S / 100

    def dollar_theta(self: Call, Notional: float) -> float:
        """
        returns dollar theta for a given Notional 

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Notional * self.theta()

    def dollar_vega(self: Call, Notional: float) -> float:
        """
        returns dollar vega for a given Notional 

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Notional * self.vega()
    
    def dollar_rho(self: Call, Notional: float) -> float:
        """
        returns dollar rho for a given Notional 

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Notional * self.rho()

class Put(Call): 

    __slots__ = ('S', 'K', 'T', 'v', 'r', 'q')
    def __init__(self: Put, **kwargs):
        Call.__init__(self, **kwargs)

    def price(self: Put) -> float:
        """
        returns price of call option

        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, d2 = self._Call__ds() 
        return norm.cdf(-d2) * self.K * np.exp(- self.r * self.T) - norm.cdf(-d1) * self.S * np.exp(-self.q * self.T)

    def delta(self: Put) -> float:
        """
        returns delta of put option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return np.exp(self.q * self.T) * (Call.delta(self) - 1)

    def theta(self: Put) -> float:
        """
        returns theta of put option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        d1, d2 = self._Call__ds() 
        first_term  = - np.exp(self.q * self.T) * self.S * norm.pdf(d1) * self.v / (2 * np.sqrt(self.T))
        second_term = + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        third_term = - self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(-d1)

        this_theta = first_term + second_term + third_term

        return Call.scale(Call.THETA_NORMALIZATION, this_theta) 

    def gamma(self: Put) -> float:
        """
        returns gamma of put option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Call.gamma(self)

    def vega(self: Put) -> float:
        """
        returns vega of put option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        return Call.vega(self)

    def rho(self: Put) -> float:
        """
        returns rho of put option
    
        receives Option object with the following attributes:
            S: float            spot price,
            K: float            option strike,
            T: float            delta time until expire,
            v: float            volatility (implied or realized),
            r: float            interest rate
        """
        _, d2 = self._Call__ds() 
        return Call.scale(Call.RHO_NORMALIZATION, - self.K * np.exp(-self.r * self.T) * norm.cdf(-d2))


