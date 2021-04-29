# Vanilla Black and Scholes Formulas

This repository implements in python the vanilla black and scholes
formula for calls and puts as well as some of the greeks.

A basic introduction can be found at wikipedia: 
[black scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) 

## Structure 

The main executable is `main.py`. It should output a heatmap of deltas and gammas obtained from
`data/plan_base.xlsx`. It also saves both heatmaps as png images in the `data` folder.

```
.
├── black_scholes.py
├── data
│   ├── plan_base.xlsx
│   ├── plan_resultados.xlsm
├── LICENSE
├── main.py
├── Makefile
├── README.md
├── test.py
└── utils
    ├── data_handling.py
    ├── dates.py
    ├── __init__.py
    ├── option.py
    └── tables.py

4 directories, 14 files
```

If you are in Linux you can type

```console
$ make
```

to generate these heatmaps.

**ALL DATA CONTAINED IN THE XLSX FILE IS FAKE** 

## Tests on Linux

Type in terminal

```console
$ make test
```

Test parameters were copied from 
[Zsolt-Forray/options-calculator](https://github.com/Zsolt-Forray/options-calculator)

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
