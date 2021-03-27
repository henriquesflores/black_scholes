#!usr/bin/env python3
from dataclasses import dataclass
from enum import Enum

import numpy as np
from scipy.stats import norm

class Payoff(Enum):
    CALL = 1,
    PUT = 2

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
    
        A = self.sigma * np.sqrt(self.dT)
        log_term   = np.log(self.St / self.K)
        drift_term = (self.r + self.sigma * self.sigma / 2) 
        
        d1 = 1 / A * (log_term + drift_term * self.dT)
        d2 = d1 - A
    
        return d1, d2


    def price_option(self) -> float:
        """
        price_option returns price of a call option

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

        return first_term - second_term

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

def main():
    call = Option(1, 1, 1, 1, 1)
    print(call.price_option())
    print(call.delta())
    print(call.vega())
    print(call.portfolio())

if __name__ == "__main__": main()
