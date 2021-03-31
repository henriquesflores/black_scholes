import numpy as np
import pandas as pd
from scipy.stats import norm


class Call: 
    __slots__ = ('PX', 'K', 'dT', 'sigma', 'r')
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __ds(self) -> tuple:
        """
        returns d1, d2 of Black and Scholes solution

        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
    
        sigma_term = self.sigma * np.sqrt(self.dT)
        log_term   = np.log(self.PX / self.K)
        drift_term = (self.r + self.sigma * self.sigma / 2) 
        
        d1 = 1 / sigma_term * (log_term + drift_term * self.dT)
        d2 = d1 - sigma_term
    
        return d1, d2

    def price_option(self) -> float:
        """
        returns price of call option

        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
    
        d1, d2 = self.__ds() 
        return norm.cdf(d1) * self.PX - norm.cdf(d2) * self.K * np.exp(-self.r * self.dT)

    def delta(self) -> float:
        """
        returns delta of call option
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        d1, _ = self.__ds() 
        return norm.cdf(d1)

    def theta(self) -> float:
        """
        returns theta of call option
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        d1, d2 = self.__ds() 
        first_term  = - self.PX * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.dT))
        second_term = - self.r * self.K * np.exp(self.r * self.dT) * norm.cdf(d2)

        return first_term + second_term

    def gamma(self) -> float:
        """
        returns gamma of call option
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """

        d1, _ = self.__ds()
        return norm.pdf(d1) / (self.PX * self.sigma * np.sqrt(self.dT))

    def vega(self) -> float:
        """
        returns vega of call option
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """

        d1, _ = self.__ds()
        return self.PX * norm.pdf(d1) * np.sqrt(self.dT)

    def rho(self) -> float:
        """
        returns rho of call option
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        _, d2 = self.__ds() 
        return self.K * np.exp(-self.r * self.dT) * norm.cdf(d2)

    def portfolio(self) -> float:
        """
        returns value of a hedged portfolio 
    
        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        return self.price_option() - self.delta() * self.PX

    def show(self) -> None:
        """
        prints to stdout the price and greeks of option

        receives Option object with the following attributes:
            PX: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        option_data = { 'price' : self.price_option(),    \
                        'delta' : self.delta(),           \
                        'gamma' : self.gamma(),           \
                        'theta' : self.theta(),           \
                        'rho'   : self.rho(),             \
                      }
        
        for k, v in option_data.items():
            print("{:} = {:.2f}".format(k, v))


