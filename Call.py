import numpy as np
from scipy.stats import norm

class Call: 
    __slots__ = ('S', 'K', 'T', 'v', 'r')
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __ds(self) -> tuple:
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
        drift_term = (self.r + self.v * self.v / 2) 
        
        d1 = (1 / sigma_term) * (log_term + drift_term * self.T)
        d2 = d1 - sigma_term
    
        return d1, d2

    def price(self) -> float:
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
        return norm.cdf(d1) * self.S - norm.cdf(d2) * self.K * np.exp(-self.r * self.T)

    def delta(self) -> float:
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
        return norm.cdf(d1)

    def theta(self) -> float:
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
        first_term  = - self.S * norm.pdf(d1) * self.v / (2 * np.sqrt(self.T))
        second_term = - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

        return first_term + second_term

    def gamma(self) -> float:
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
        return norm.pdf(d1) / (self.S * self.v * np.sqrt(self.T))

    def vega(self) -> float:
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
        return self.S * norm.pdf(d1) * np.sqrt(self.T)

    def rho(self) -> float:
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
        return self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def greeks(self) -> None:
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

    def dollar_delta(self, Notional: float):
       return Notional * self.delta()

    def dollar_gamma(self, Notional: float):
        return Notional * 0.5 * self.gamma() * np.power(self.S / 100, 2)

    def dollar_theta(self, Notional: float):
        return Notional * self.theta()

    def dollar_vega(self, Notional: float):
        return Notional * self.vega()
    
    def dollar_rho(self, Notional: float):
        return Notional * self.rho()
