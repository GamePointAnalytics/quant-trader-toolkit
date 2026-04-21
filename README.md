# Quant Trader Toolkit 📈

An institutional-grade portfolio project and training environment designed to prepare for Quantitative Trading (QT) interviews at top-tier proprietary trading firms and hedge funds (e.g., Jane Street, Citadel, Optiver, HRT, SIG).

This repository contains educational cheat sheets, interactive Jupyter notebook simulations, and high-performance terminal games that mimic the exact Online Assessments (OAs) and phone screen brainteasers used in the industry.

---

## 🏗️ Project Structure

The toolkit is divided into three core pillars: **Theory**, **Notebook Simulations**, and **Terminal Games**.

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
- **`sequence_puzzles.py`**: Mimics Akuna Capital and TradingScreen sequence OAs. Generates vicious patterns including:
  - Recursive digit sums
  - Cubic polynomials
  - Alternating operations (e.g., `*2, -3, *2...`)
  - Interleaved arithmetic/geometric sequences
  - Fibonacci-difference sequences

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/GamePointAnalytics/quant-trader-toolkit.git
   cd quant-trader-toolkit
   ```
2. **For the Notebooks**: Open the `.ipynb` files in Visual Studio Code (requires the Jupyter extension) or run a Jupyter server.
3. **For the Terminal Games**: 
   ```bash
   cd terminal_games
   python sequence_puzzles.py
   ```

## 🛠️ Tech Stack
- **Language**: Python 3.8+
- **Libraries**: `numpy`, `matplotlib`, `scipy` (for Options visualizations)
- **Environment**: Jupyter Notebooks, Command Line Interface (CLI)

---
*Built for speed, accuracy, and positive expected value.*
