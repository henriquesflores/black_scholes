# Vanilla Black and Scholes Formulas

This repository implements in python the vanilla black and scholes
formula for calls and puts as well as some of the greeks.

A basic introduction can be found at wikipedia: 
[black scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) 

## Linux

To run tests type 

```console
make test
```

## TODOs

### First project
 - [x]  rho
 - [x]  Initialization via dict
 - [x]  Put payoff
 - [x]  Check equations
    - [x] Rho, Vega and Theta might need scale adjustment
 - [x]  Implement tests
 - [x]  Dividend yield assets
 - [ ] Greeks do not match BBG.
 
### Later
 - [ ]  American options
 - [ ]  Implied Volatility 


## Data

Test parameters were copied from 
[Zsolt-Forray/options-calculator](https://github.com/Zsolt-Forray/options-calculator)
