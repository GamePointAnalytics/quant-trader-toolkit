"""
Market Making vs. RL Agent — Terminal Game
============================================
Play a multi-round market-making game against a pre-trained 
Q-learning adversary that has learned to exploit common quoting
patterns (tight spreads, biased midpoints, slow inventory adjustment).

The agent gets harder as you play more sessions because it continues
to learn from your specific habits.
"""

import sys
import os
import time
import random

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ml.market_maker_rl import MarketMakerRLAgent, ACTIONS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "market_maker_qtable.pkl")
ROUNDS_PER_GAME = 10


def play_game(agent, train_live=True):
    """Play one full game against the RL agent."""
    
    # Generate a hidden true value (sum of 100 draws from U(0,10), EV = 500)
    true_value = sum(random.uniform(0, 10) for _ in range(100))
    
    player_cash = 0.0
    agent_cash = 0.0
    player_inventory = 0
    trades = []
    
    print("\n" + "=" * 60)
    print("  NEW GAME — MARKET MAKING vs. RL AGENT")
    print("=" * 60)
    print("The hidden value is the sum of 100 draws from U(0,10).")
    print(f"(Hint: The theoretical EV is 500. Actual value is hidden.)")
    print(f"You will play {ROUNDS_PER_GAME} rounds. Quote wisely.\n")
    
    for r in range(1, ROUNDS_PER_GAME + 1):
        print("-" * 60)
        print(f"ROUND {r}/{ROUNDS_PER_GAME}")
        print(f"  Your Cash: ${player_cash:>+10.2f}  |  Inventory: {player_inventory}")
        print(f"  Agent Cash: ${agent_cash:>+10.2f}")
        print()
        
        # Get player's quote
        while True:
            bid_str = input("  Enter your BID (or 'q' to quit): ").strip()
            if bid_str.lower() == 'q':
                print("\nQuitting game early...")
                return None
            
            ask_str = input("  Enter your ASK: ").strip()
            
            try:
                bid = float(bid_str)
                ask = float(ask_str)
                if bid >= ask:
                    print("  [!] Bid must be strictly less than Ask. Try again.\n")
                    continue
                break
            except ValueError:
                print("  [!] Invalid numbers. Try again.\n")
                continue
        
        spread = ask - bid
        midpoint = (bid + ask) / 2.0
        
        # Agent decides
        state = agent.get_state(bid, ask, true_value, player_inventory, r, ROUNDS_PER_GAME)
        action_idx = agent.choose_action(state, training=train_live)
        action_name = ACTIONS[action_idx]
        reward = agent.calculate_reward(action_idx, bid, ask, true_value)
        
        print(f"\n  Agent is thinking", end="")
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print()
        
        if action_name == "hit_bid":
            print(f"  >>> Agent SELLS to you at your bid: ${bid:.2f}")
            player_inventory += 1
            player_cash -= bid
            agent_cash += bid
        elif action_name == "lift_offer":
            print(f"  >>> Agent BUYS from you at your ask: ${ask:.2f}")
            player_inventory -= 1
            player_cash += ask
            agent_cash -= ask
        else:
            print(f"  >>> Agent PASSES. No trade this round.")
        
        trades.append({
            "round": r,
            "bid": bid,
            "ask": ask,
            "spread": spread,
            "midpoint": midpoint,
            "action": action_name,
            "agent_reward": reward
        })
        
        # Live training: update Q-table with this interaction
        if train_live:
            next_state = agent.get_state(bid, ask, true_value, player_inventory, r + 1, ROUNDS_PER_GAME)
            agent.update(state, action_idx, reward, next_state)
        
        print()
    
    # --- Game Over: Mark to Market ---
    print("=" * 60)
    print("  GAME OVER — FINAL SETTLEMENT")
    print("=" * 60)
    print(f"\n  TRUE VALUE: ${true_value:.2f}\n")
    
    # Mark remaining inventory to market
    inventory_value = player_inventory * true_value
    final_pnl = player_cash + inventory_value
    agent_inventory_value = -player_inventory * true_value
    agent_final_pnl = agent_cash + agent_inventory_value
    
    print(f"  YOUR RESULTS:")
    print(f"    Cash from trades:  ${player_cash:>+10.2f}")
    print(f"    Inventory:         {player_inventory} units @ ${true_value:.2f} = ${inventory_value:>+10.2f}")
    print(f"    ----------------------------------")
    print(f"    FINAL P&L:         ${final_pnl:>+10.2f}")
    
    print(f"\n  AGENT RESULTS:")
    print(f"    Cash from trades:  ${agent_cash:>+10.2f}")
    print(f"    Inventory:         {-player_inventory} units @ ${true_value:.2f} = ${agent_inventory_value:>+10.2f}")
    print(f"    ----------------------------------")
    print(f"    FINAL P&L:         ${agent_final_pnl:>+10.2f}")
    
    if final_pnl > 0:
        print(f"\n  🏆 YOU WIN! You made ${final_pnl:.2f}")
    elif final_pnl < 0:
        print(f"\n  💀 AGENT WINS. You lost ${abs(final_pnl):.2f}")
    else:
        print(f"\n  🤝 DRAW. Zero P&L.")
    
    # --- Post-Game Analytics ---
    print("\n" + "-" * 60)
    print("  POST-GAME ANALYTICS")
    print("-" * 60)
    
    spreads = [t["spread"] for t in trades]
    midpoints = [t["midpoint"] for t in trades]
    actions = [t["action"] for t in trades]
    
    print(f"  Avg Spread:       {sum(spreads)/len(spreads):.2f}")
    print(f"  Avg Midpoint:     {sum(midpoints)/len(midpoints):.2f} (true value: {true_value:.2f})")
    print(f"  Times Hit:        {actions.count('hit_bid')} bids hit, {actions.count('lift_offer')} offers lifted")
    print(f"  Times Passed:     {actions.count('pass')}")
    
    pick_off_rate = (actions.count('hit_bid') + actions.count('lift_offer')) / len(actions) * 100
    print(f"  Pick-off Rate:    {pick_off_rate:.0f}%")
    
    if pick_off_rate > 70:
        print("\n  [Feedback] You are getting picked off constantly.")
        print("  Consider widening your spreads or adjusting your midpoint.")
    elif pick_off_rate < 30:
        print("\n  [Feedback] The agent is mostly passing on your quotes.")
        print("  Your spreads might be too wide — you're leaving edge on the table.")
    else:
        print("\n  [Feedback] Decent balance between getting filled and staying safe.")
    
    return final_pnl


def main():
    print("\n" + "+" * 60)
    print("  ADVERSARIAL MARKET MAKING SIMULATOR")
    print("  Powered by Q-Learning Reinforcement Learning")
    print("+" * 60)
    
    # Load pre-trained agent
    agent = MarketMakerRLAgent()
    if os.path.exists(MODEL_PATH):
        agent.load(MODEL_PATH)
        print(f"  Loaded pre-trained agent ({len(agent.q_table)} states).")
    else:
        print("  [!] No pre-trained agent found. Starting with random agent.")
        print("  [!] Run `python -m ml.market_maker_rl` to pre-train first.\n")
    
    # Set epsilon low for play mode (mostly exploit, slight exploration)
    agent.epsilon = 0.08
    
    session_pnls = []
    
    while True:
        result = play_game(agent, train_live=True)
        if result is None:
            break
        session_pnls.append(result)
        
        # Save agent after each game (it learned from you)
        agent.save(MODEL_PATH)
        
        print(f"\n  Session record: {len(session_pnls)} games | "
              f"Total P&L: ${sum(session_pnls):.2f} | "
              f"Win rate: {sum(1 for p in session_pnls if p > 0)/len(session_pnls)*100:.0f}%")
        
        again = input("\n  Play another game? (y/n): ").strip().lower()
        if again != 'y':
            break
    
    print("\n" + "=" * 60)
    print("  SESSION SUMMARY")
    print("=" * 60)
    if session_pnls:
        print(f"  Games Played:   {len(session_pnls)}")
        print(f"  Total P&L:      ${sum(session_pnls):+.2f}")
        print(f"  Best Game:      ${max(session_pnls):+.2f}")
        print(f"  Worst Game:     ${min(session_pnls):+.2f}")
        print(f"  Win Rate:       {sum(1 for p in session_pnls if p > 0)/len(session_pnls)*100:.0f}%")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
