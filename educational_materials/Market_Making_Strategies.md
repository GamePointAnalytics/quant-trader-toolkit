# Market Making Strategies & Games

In a quantitative trading interview, you will often play "Market Making Games." The interviewer has a secret number (e.g., the exact length of the Mississippi River, or an expected value of a complex dice game). Your goal is to make a market on that value.

## The Core Concept
A market consists of a **Bid** and an **Ask**.
- **Bid:** The price you are willing to *buy* the underlying asset for.
- **Ask (or Offer):** The price you are willing to *sell* the underlying asset for.
- **Spread:** Ask - Bid. (Your edge).
- **Fair Value (Theoretical Value):** Your best estimate of the true expected value of the asset.

Your ideal market is centered around your Fair Value:
`Bid = Fair Value - Edge`
`Ask = Fair Value + Edge`

## How the Game Works
1. Interviewer asks a question with an unknown numerical answer (e.g., "Make me a market on the number of gas stations in the US").
2. You provide a Bid and an Ask. Let's say you say "90,000 at 120,000".
3. The interviewer decides either to **Buy** (they buy from you at your Ask price) or **Sell** (they sell to you at your Bid price).
4. If they Buy, you are short the asset at the Ask price. If they Sell, you are long the asset at your Bid price.
5. The true value is revealed. Your P&L is calculated.

### The Interviewer's Edge
The interviewer knows the true value perfectly (or much better than you). This is called **Adverse Selection**. If you quote a market that does not contain the true value, the interviewer will trade with you, and you will guarantee a loss. 
- *Example:* True value is 150,000. You quote "90,000 at 120,000". The interviewer buys from you at 120,000. You sold an asset worth 150,000 for 120,000. Your P&L = -30,000.

## Rules of Thumb for Market Making Interviews

1. **Quote Wide:** Most candidates fail because they quote spreads that are too tight. A 90% confidence interval means if you play this game 100 times, you will lose 10 times to adverse selection. That is often too risky in a game where the opponent has perfect information. Quote wide enough so you aren't immediately picked off.
2. **Move Your Market (Inventory Management):**
   - If the interviewer "hits your bid" (they sell to you), you are now holding inventory. You must assume their action contained information (they think the true value is lower than your bid).
   - *Reaction:* You must dramatically lower your subsequent market. If you bought at 90,000, your next market should probably be something like "60,000 at 85,000". Do NOT hold onto your original fair value.
3. **Never Cross Markets:** Do not make a Bid higher than your previous Ask unless you have gained significant new information. 
4. **Be aware of expected values:** For math puzzles, quickly calculate the EV. If the EV is exactly 50, a tight market is safe (e.g. 49.5 at 50.5).

## Math Application: Edge Calculation
If playing an EV game (like guessing the sum of rolling a die 100 times):
- The true EV is $100 \times 3.5 = 350$.
- Standard deviation of one die is $\approx 1.7$. For 100 dice, variance is $100 \times 2.91 = 291$. Std Dev is $\approx 17$.
- To quote a 95% confidence interval ($\approx 2$ Std Devs), you want roughly $\pm 34$.
- Market: "316 at 384".

*Pro Tip: Interviewers want to see how you react when you realize you guessed completely wrong. Don't freeze. Systematically adjust your quotes.*
