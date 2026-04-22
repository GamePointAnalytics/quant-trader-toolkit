# Quant Trader Toolkit 📈

An institutional-grade portfolio project and training environment designed to prepare for Quantitative Trading (QT) interviews at top-tier proprietary trading firms and hedge funds (e.g., Jane Street, Citadel, Optiver, HRT, SIG).

This repository contains educational cheat sheets, interactive Jupyter notebook simulations, ML-powered adversarial training environments, and high-performance terminal games that mimic the exact Online Assessments (OAs) and phone screen brainteasers used in the industry.

---

## 🏗️ Project Structure

The toolkit is divided into four core pillars: **Theory**, **Notebook Simulations**, **Terminal Games**, and **ML Modules**.

### 1. Educational Materials (`educational_materials/`)
Rapid-review Markdown cheat sheets covering the mathematical and strategic fundamentals of the job:
- **`Mental_Math_Tricks.md`**: Estimation frameworks (Fermi problems), fraction-to-decimal conversions, and rapid arithmetic shortcuts (Zetamac prep).
- **`Expected_Value_Cheatsheet.md`**: Stopping-rule games, backward induction, linearity of expectation, and continuous uniform distributions.
- **`Market_Making_Strategies.md`**: Bid/Ask quoting strategies, adverse selection, and inventory management.
- **`Options_Pricing_Fundamentals.md`**: Intuitive Black-Scholes, Put-Call Parity (arbitrage detection), and practical definitions of the Greeks (Delta, Gamma, Theta, Vega).

### 2. Interactive Notebook Simulations (`notebooks/`)
Jupyter Notebooks used to simulate games, visualize pricing models, and prove mathematical theorems via the Law of Large Numbers.
- **`01_Mental_Math_and_Estimation.ipynb`**: Basic Zetamac clone and Fermi question generators.
- **`02_Expected_Value_Puzzles.ipynb`**: Python solvers for classic dice games and the St. Petersburg Paradox.
- **`03_Market_Making_Games.ipynb`**: Interactive text-based game where you quote a market against a bot that attempts to pick you off if your edge is too tight.
- **`04_Options_and_Greeks.ipynb`**: Visualizes Delta decay as an option approaches expiration using `scipy.stats` and `matplotlib`.
- **`05_Optiver_80_in_8.ipynb`**: A punishing simulator that mimics the Optiver 80-in-8 test (decimals, fractions, and percentages under extreme time pressure).
- **`06_Urn_Draw_EV_Engine.ipynb`**: Simulates the classic "Urn" game with a built-in Dynamic Programming engine that calculates the true Expected Value of your decisions in real-time.
- **`07_Numerical_Sequence_Patterns.ipynb`**: Logic puzzle generators for sequence tests.

### 3. Terminal Games (`terminal_games/`)
Because Jupyter Notebooks struggle with latency-sensitive `input()` loops, the hardcore speed drills are written as pure Python scripts designed to be executed directly in your terminal.
- **`sequence_puzzles.py`**: Mimics Akuna Capital and TradingScreen sequence OAs. Generates vicious patterns including recursive digit sums, cubic polynomials, alternating operations, interleaved sequences, and Fibonacci-difference sequences.
- **`sequence_with_hints.py`**: Enhanced version with an ML-powered hint system. Type `h` when stuck to get the trained classifier's prediction of the pattern type with a confidence score.
- **`market_maker_vs_rl.py`**: Play a multi-round market-making game against an adversarial RL agent that learns your quoting habits in real-time.

### 4. Machine Learning Modules (`ml/`)
The ML layer that transforms this from a static drill tool into an adaptive training environment.

#### Adversarial Market Making Agent (`ml/market_maker_rl.py`)
A **tabular Q-learning** reinforcement learning agent that plays the role of an adversarial counterparty:
- **State Space**: Discretized spread width, midpoint error, player inventory, and round number.
- **Action Space**: Hit bid, lift offer, or pass.
- **Reward**: Zero-sum P&L against the player.
- Pre-trained against 1,500 episodes of simulated players with diverse quoting styles (tight, wide, biased, adaptive). The agent continues to learn from *your* specific habits during live play.

#### Sequence Pattern Classifier (`ml/sequence_classifier.py`)
A **Random Forest classifier** (200 trees) that identifies which mathematical pattern generated a numerical sequence:
- **19 engineered features**: Difference analysis (1st/2nd/3rd order), ratio stability, Fibonacci correlation, interleave detection, digit-sum matching.
- **7 pattern classes**: Alternating operations, digit sums, powers/exponentials, fractional multipliers, interleaved sequences, Fibonacci differences, cubic polynomials.
- **99.9% test accuracy** on 14,000 generated sequences.

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/GamePointAnalytics/quant-trader-toolkit.git
   cd quant-trader-toolkit
   pip install -r requirements.txt
   ```

2. **Pre-train the ML models** (one-time setup):
   ```bash
   python -m ml.market_maker_rl        # Train the RL market maker (~5 sec)
   python -m ml.sequence_classifier    # Train the pattern classifier (~15 sec)
   ```

3. **Play the Terminal Games**:
   ```bash
   cd terminal_games
   python market_maker_vs_rl.py       # Market making vs. RL agent
   python sequence_with_hints.py      # Sequence drills with ML hints
   python sequence_puzzles.py         # Raw sequence drills (no hints)
   ```

4. **For the Notebooks**: Open the `.ipynb` files in Visual Studio Code (requires the Jupyter extension) or run a Jupyter server.

## 🛠️ Tech Stack
- **Language**: Python 3.8+
- **ML**: scikit-learn (Random Forest), tabular Q-learning (pure NumPy)
- **Libraries**: `numpy`, `matplotlib`, `scipy`
- **Environment**: Jupyter Notebooks, Command Line Interface (CLI)

---
*Built for speed, accuracy, and positive expected value.*
