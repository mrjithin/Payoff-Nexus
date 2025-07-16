# Payoff Nexus - Project Report

This project implements a hybrid option pricing model combining the Cox-Ross-Rubinstein (CRR) binomial tree with game theory concepts. Using Apple Inc. (AAPL) historical data from 2022, we price a 1-year European call option by modeling the interaction between option holders and writers as a zero-sum game solved via linear programming at each lattice node. The Nash equilibrium strategy enriches classical risk-neutral pricing by incorporating strategic behavior.

## Methodology
### Data Pipeline
Data Source: Yahoo Finance (AAPL daily closes: 2022-01-01 to 2023-01-01)

Volatility Calculation: Annualized standard deviation of log returns (σ ≈ 25%)

Key Parameters:

- Strike price: $130

- Risk-free rate: 4.43%

- Time to expiration: 1 year

- Binomial steps: 100

### Model Architecture

CRR Binomial Tree:

- Simulates potential price paths

- Calculates risk-neutral probabilities

Game-Theoretic Layer:

- Players: Option holder (buyer) vs. writer (seller)

Strategies:

- Holder: Hold or Exercise

- Writer: 6 hedge ratios {1.0, 0.67, 0.33, 0, -0.33, -0.67}

Payoff Matrix: Quantifies outcomes for all strategy combinations

Nash Equilibrium: Solved via linear programming at each node

Backward Induction:

- Starts at expiration with intrinsic values

- Replaces classical expectation with game value at each node

- Propagates strategic values to root node

## Results

- Underlying : AAPL
- Strike Price : \$130
- Maturity : 1 year
- Historical Volatility: Varies with dates pulled.
- Risk-Free Rate : 4.43%
- Strategic Price	Varies with data pulled. 

## Limitations

Market Assumptions:

- Constant volatility

- Flat risk-free term structure

- European exercise only

Model Simplifications:

- Discrete hedge ratios

- No transaction costs

- Single-period games

## References
- Bao, Z. (2024). Application of Game Theory in Option Pricing: A Binomial Tree Model Approach