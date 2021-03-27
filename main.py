#!usr/bin/env python3
from dataclasses import dataclass
from enum import Enum

import numpy as np
from scipy.stats import norm

"""
TODO:
    [ ] - Implement rho
    [ ] - Implement Put payoff
    [ ] - Check equations
    [ ] - Implement dividend yield assets
    [ ] - Implement American options
"""

class Payoff(Enum):
    CALL = 1,
    PUT  = 2

@dataclass
class Option: 
    St:     float 
    K:      float    
    dT:     float
    sigma:  float
    r:      float
#    payoff: Payoff

    def ds(self) -> tuple:
        """
        returns d1, d2 of Black and Scholes solution

        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
    
        sigma_term = self.sigma * np.sqrt(self.dT)
        log_term   = np.log(self.St / self.K)
        drift_term = (self.r + self.sigma * self.sigma / 2) 
        
        d1 = 1 / sigma_term * (log_term + drift_term * self.dT)
        d2 = d1 - sigma_term
    
        return d1, d2


    def price_option(self) -> float:
        """
        returns price of call option

        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
    
        d1, d2 = self.ds() 
        return norm.cdf(d1) * self.St - norm.cdf(d2) * self.K * np.exp(-self.r * self.dT)

    def delta(self) -> float:
        """
        returns delta of call option
    
        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        d1, _ = self.ds() 
        return norm.cdf(d1)

    def theta(self) -> float:
        """
        returns theta of call option
    
        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        d1, d2 = self.ds() 
        first_term  = - self.St * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.dT))
        second_term = - self.r * self.K * np.exp(-self.r * self.dT) * norm.cdf(d2)

        return first_term + second_term

    def gamma(self) -> float:
        """
        returns gamma of call option
    
        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """

        d1, _ = self.ds()
        return norm.pdf(d1) / (self.St * self.sigma * np.sqrt(self.dT))

    def vega(self) -> float:
        """
        returns vega of call option
    
        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """

        d1, _ = self.ds()
        return self.St * norm.pdf(d1) * np.sqrt(self.dT)


    def portfolio(self) -> float:
        """
        returns value of a hedged portfolio 
    
        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        return self.price_option() - self.delta() * self.St

    def print(self) -> None:
        """
        prints to stdout the price and greeks of option

        receives Option object with the following attributes:
            St: float            spot price,
            K:  float            option strike,
            dT: float            delta time until maturity,
            sigma: float         volatility (implied or realized),
            r: float             interest rate
        """
        option_data = { 'price' : self.price_option(),    \
                        'delta' : self.delta(),           \
                        'gamma' : self.gamma(),           \
                        'theta' : self.theta(),           \
                      }
        
        for k, v in option_data.items():
            print("{:} = {:.2f}".format(k, v))


def main():
    call = Option(215.99, 215, 0.15, 0.1 / np.sqrt(252), 0.09 / 100)
    call.print()

if __name__ == "__main__": main()
