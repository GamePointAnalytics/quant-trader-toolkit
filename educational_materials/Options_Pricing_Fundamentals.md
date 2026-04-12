# Options Pricing & The Greeks

While QT interviews won't ask you to derive Black-Scholes from scratch via Ito's Lemma (that's for QR), you must have an absolute, intuitive understanding of Put-Call Parity, Arbitrage, and the Greeks.

## 1. Core Intuition
- **Call Option:** The right to *buy* a stock at strike $K$. You want the stock to go UP.
- **Put Option:** The right to *sell* a stock at strike $K$. You want the stock to go DOWN.
- **Payoff at Expiration (Time $T$):**
  - Call: $\max(0, S_T - K)$
  - Put: $\max(0, K - S_T)$

## 2. Put-Call Parity
This is the most tested concept in options interviews. It describes the no-arbitrage relationship between the price of a European call and a European put with the same strike, expiration, and underlying asset.

**Formula:**
$C - P = S - K \cdot e^{-rT}$
*(Call Price - Put Price = Spot Price - Present Value of Strike)*

**Intuition:** 
Owning a Call and shorting a Put ($C - P$) gives you the exact same payoff at expiration as simply owning the Stock and borrowing the present value of the Strike price. If this relationship breaks, an arbitrage opportunity exists.

**Interview Application:** 
"If a Call is trading at $\$5$, the Put is trading at $\$3$, the stock is at $\$100$, and the strike is $\$100$ (assume 0 interest rates), is there an arbitrage?"
- $C - P = 5 - 3 = 2$
- $S - K = 100 - 100 = 0$
- $2 \neq 0$. Therefore, Arbitrage exists. The "synthetic forward" ($C - P$) is overpriced relative to the actual stock.
- **Trade:** Sell the Synthetic (Sell Call, Buy Put) and Buy the Stock. Profit = $\$2$ risk-free.

## 3. The Greeks
Greeks measure how an option's price changes relative to different variables.

### Delta ($\Delta$)
- **Definition:** Change in option price per $\$1$ change in underlying price. The "hedge ratio".
- **Call Delta:** $0$ to $1$. (At-The-Money $\approx 0.5$)
- **Put Delta:** $-1$ to $0$. (At-The-Money $\approx -0.5$)
- **Intuition:** If you own 1 Call with a Delta of $0.5$, and you want to be "Delta Neutral" (immune to tiny stock movements), you must short $0.5$ shares of the underlying stock.

### Gamma ($\Gamma$)
- **Definition:** Change in Delta per $\$1$ change in underlying. It is the *convexity* of the option.
- **Always positive for long options** (both Calls and Puts).
- **Intuition:** Gamma is highest for At-The-Money (ATM) options close to expiration. It represents your "scalping" potential. Being long Gamma means you get longer as the market goes up, and shorter as the market goes down (you are buying dips and selling rips dynamically if delta hedging).

### Theta ($\Theta$)
- **Definition:** Change in option price per 1 day passing (Time Decay).
- **Usually negative for long options.** You pay a premium for time value.
- **Intuition:** Gamma and Theta are two sides of the same coin. If you are long Gamma (convexity), you are paying for it with Theta (bleeding money every day).

### Vega ($\nu$)
- **Definition:** Change in option price per 1% change in Implied Volatility (IV).
- **Always positive for long options.**
- **Intuition:** If you think the market is going to be wildly unpredictable but don't know the direction, you want to be long Vega (long options).

## Summary Table for Traders

| Component | Variable | Call Price Impact | Put Price Impact |
| :--- | :--- | :--- | :--- |
| **Spot Price** ($S$) | Goes Up | $\uparrow$ Increases | $\downarrow$ Decreases |
| **Strike Price** ($K$) | Higher Strike | $\downarrow$ Decreases | $\uparrow$ Increases |
| **Time to Expiry** ($T$) | More Time | $\uparrow$ Increases | $\uparrow$ Increases |
| **Volatility** ($\sigma$) | Higher Vol | $\uparrow$ Increases | $\uparrow$ Increases |
| **Interest Rate** ($r$) | Higher Rates | $\uparrow$ Increases | $\downarrow$ Decreases |
