# Expected Value & Probability Cheatsheet

Expected Value (EV) is the cornerstone of all quantitative trading. Every trade is essentially a proposition: "Is the expected value of this action strictly greater than 0?"

## Core Definitions

**Expected Value (Discrete):**
The sum of all possible outcomes multiplied by their respective probabilities.
$E[X] = \sum_{x} x \cdot P(X=x)$

**Expected Value (Continuous):**
$E[X] = \int_{-\infty}^{\infty} x \cdot f(x) dx$

**Linearity of Expectation (Crucial Concept!):**
The expected value of a sum is equal to the sum of their expected values, **regardless of whether the variables are independent**.
$E[X + Y] = E[X] + E[Y]$
$E[cX] = cE[X]$

*Traders heavily rely on this principle to simplify complex, dependent events by treating them as sums of simpler events or indicator variables.*

---

## Classic Interview Problem Frameworks

### 1. Stopping Rule Games ("Roll a die until...")
**Scenario:** You roll a fair 6-sided die. You can stop at any time and get paid the face value of the die in dollars. You can roll up to $N$ times. What is the optimal strategy, and what is the expected value?

**Framework: Backward Induction**
Always work backwards from the last possible roll.
- **Roll $N$ (Last Roll):** You must accept whatever you roll. The EV is $E[X] = 3.5$.
- **Roll $N-1$:** You will roll the die. Before looking at the result, you know that if you roll again, your expectation is $3.5$. Therefore, you should only stop now if you roll a $4, 5, \text{ or } 6$.
  - EV of Roll $N-1 = P(\text{roll } \ge 4) \times E[X | X \ge 4] + P(\text{roll } < 4) \times (\text{EV of Roll } N)$
  - EV $= (3/6) \times 5 + (3/6) \times 3.5 = 2.5 + 1.75 = 4.25$
- **Roll $N-2$:** Your expected value for continuing is now $4.25$. Therefore, you should only stop if you roll a $5 \text{ or } 6$.
  - EV $= (2/6) \times 5.5 + (4/6) \times 4.25 = 1.833 + 2.833 = 4.66$

### 2. The St. Petersburg Paradox
**Scenario:** A coin is flipped until a heads appears. If Heads appears on the $n$-th flip, you are paid $2^n$ dollars. How much would you pay to play this game?

**Expected Value Calculation:**
$P(\text{Heads on flip } n) = (1/2)^n$
Payout $= 2^n$
$E[\text{Payout}] = \sum_{n=1}^{\infty} ((1/2)^n \times 2^n) = \sum_{n=1}^{\infty} 1 = \infty$

*Note: In an interview setting, the interviewer will likely introduce a finite bankroll (e.g., the casino only has $1,000,000$). You must be able to recalculate the truncated expected value.*

### 3. Coin Flipping & Combinatorics
Whenever looking for combinations of sequences (e.g. "Probability of getting exactly 3 heads in 10 flips"), use the binomial coefficient.

**Binomial Formula:**
$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$
Where $\binom{n}{k} = \frac{n!}{k!(n-k)!}$

**Waiting Time for Sequences (Martingale Approach):**
"What is the expected number of coin flips to see Heads then Tails (HT) vs Heads then Heads (HH)?"
- **For HT:** Once you get an H, you are "halfway" there. If you get another H, you are still "halfway" there. Every H keeps you one step away. $E[HT] = 4$.
- **For HH:** Once you get an H, if you get a T, you lose all progress and start from scratch. Therefore it takes longer! $E[HH] = 6$.
- *This is often solved using state transition probabilities, but knowing the intuition that HH requires restarting is key.*

### 4. Continuous Math: Uniform Distributions
"If you draw 3 random variables from a Uniform(0,1) distribution, what is the expected value of the maximum?"
- **Rule of Thumb:** If you draw $n$ independent samples from $U(0,1)$, they partition the unit interval into $n+1$ equal expected segments.
- Expected value of the minimum (1st order statistic): $\frac{1}{n+1}$
- Expected value of the $k$-th order statistic: $\frac{k}{n+1}$
- Expected value of the maximum ($n$-th order statistic): $\frac{n}{n+1}$
- For $n=3$, EV of maximum is $3/4$.
