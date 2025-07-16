import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import linprog

stock=yf.Ticker('AAPL')
prices= stock.history(start='2022-01-01', end='2023-01-01')['Close']
log_returns = np.log(prices / prices.shift(1)).dropna()
sigma=log_returns.std()* np.sqrt(252)
K=130
T=1
r=0.0443
N=100
dt=T/N

hedge_levels=np.array([1.0, 2/3, 1/3, 0.0, -1/3, -2/3])

def nash_value(E,I):
    A = np.vstack([np.full(hedge_levels.size, E),(1 - hedge_levels)*I])
    m, n = A.shape
    c = np.zeros(m + 1);  c[-1] = -1 
    A_ub = np.hstack([-A.T, np.ones((n, 1))])
    b_ub = np.zeros(n)
    A_eq = np.zeros((1, m + 1));  
    A_eq[0,:m] = 1
    b_eq = np.array([1])
    bounds = [(0, 1)]*m+[(None, None)]

    res = linprog(c, A_ub, b_ub, A_eq, b_eq,bounds=bounds, method="highs")
    if res.success:
        return -res.fun
    return 0.0


def build(S0, sigma, dt, r, N=100):
    u=np.exp(sigma*np.sqrt(dt))
    d=1/u
    p=(np.exp(r*dt)-d)/(u-d)
    S=np.zeros((N+1, N+1))
    S[0, 0] = S0
    for i in range(N+1):
        for j in range(i+1):
            S[i, j]=S0*(u**j)*(d**(i-j))
    
    return S, p

S, p = build(prices.iloc[-1], sigma, dt=dt, r=r, N=N)

def strategic_price(S, p, dt, r, K):
    disc=np.exp(-r * dt)
    pay=np.maximum(S[-1] - K, 0.0)
    for i in range(S.shape[0] - 2, -1, -1):
        nxt = []
        for j in range(i + 1):
            E = disc * (p*pay[j + 1] + (1 - p)*pay[j])
            I = max(S[i, j] - K, 0.0)
            nxt.append(nash_value(E, I))
        pay = np.array(nxt)
    return pay[0]

price=strategic_price(S, p, dt, r, K)
print(f"The price of the option is: {price:.2f}")