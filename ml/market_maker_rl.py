"""
Adversarial Market Making RL Agent
===================================
A tabular Q-learning agent that learns to exploit a human market maker's
quoting patterns. The agent plays the role of the "interviewer" — it 
observes the player's bid/ask spreads and decides whether to hit the bid,
lift the offer, or pass.

This is a zero-sum game: the agent's profit is the player's loss.
"""

import numpy as np
import pickle
import os
import random
from collections import defaultdict

# ---------------------------------------------------------------------------
# State Discretization
# ---------------------------------------------------------------------------
# We bin continuous values into discrete buckets so we can use a Q-table.

def discretize_spread(spread):
    """Bin the bid-ask spread width."""
    if spread < 10:
        return "tight"
    elif spread < 30:
        return "medium"
    elif spread < 60:
        return "wide"
    else:
        return "very_wide"

def discretize_midpoint_error(midpoint, true_value):
    """Bin how far the player's midpoint is from the true value."""
    error = midpoint - true_value
    if error < -20:
        return "very_low"
    elif error < -5:
        return "low"
    elif error < 5:
        return "fair"
    elif error < 20:
        return "high"
    else:
        return "very_high"

def discretize_inventory(inventory):
    """Bin the player's current inventory position."""
    if inventory <= -2:
        return "very_short"
    elif inventory == -1:
        return "short"
    elif inventory == 0:
        return "neutral"
    elif inventory == 1:
        return "long"
    else:
        return "very_long"

def discretize_round(round_num, total_rounds):
    """Bin the round number into early/mid/late."""
    frac = round_num / total_rounds
    if frac < 0.33:
        return "early"
    elif frac < 0.66:
        return "mid"
    else:
        return "late"


# ---------------------------------------------------------------------------
# Q-Learning Agent
# ---------------------------------------------------------------------------

ACTIONS = ["hit_bid", "lift_offer", "pass"]

class MarketMakerRLAgent:
    """
    Tabular Q-learning agent that acts as an adversarial counterparty
    in a market-making game.
    
    State:  (spread_bin, midpoint_error_bin, inventory_bin, round_bin)
    Action: hit_bid | lift_offer | pass
    Reward: Agent's P&L from the trade
    """
    
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.15):
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = defaultdict(lambda: np.zeros(len(ACTIONS)))
        self.training_history = []  # Track agent P&L per episode
        
    def get_state(self, bid, ask, true_value, inventory, round_num, total_rounds):
        """Convert continuous game state into a discrete tuple."""
        spread = ask - bid
        midpoint = (bid + ask) / 2.0
        
        return (
            discretize_spread(spread),
            discretize_midpoint_error(midpoint, true_value),
            discretize_inventory(inventory),
            discretize_round(round_num, total_rounds)
        )
    
    def choose_action(self, state, training=True):
        """Epsilon-greedy action selection."""
        if training and random.random() < self.epsilon:
            return random.randint(0, len(ACTIONS) - 1)
        else:
            return int(np.argmax(self.q_table[state]))
    
    def update(self, state, action, reward, next_state):
        """Standard Q-learning update rule."""
        best_next = np.max(self.q_table[next_state])
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error
    
    def get_action_name(self, action_idx):
        return ACTIONS[action_idx]
    
    def calculate_reward(self, action_idx, bid, ask, true_value):
        """
        Calculate the agent's P&L from its action.
        
        - hit_bid: Agent sells to player at bid. Agent profits if true_value < bid.
        - lift_offer: Agent buys from player at ask. Agent profits if true_value > ask.
        - pass: No trade, no P&L.
        """
        action = ACTIONS[action_idx]
        
        if action == "hit_bid":
            # Agent sells at bid price. Agent is short from bid.
            # Agent profit = bid - true_value (sold high, value is lower)
            return bid - true_value
        elif action == "lift_offer":
            # Agent buys at ask price. Agent is long from ask.
            # Agent profit = true_value - ask (bought low, value is higher)
            return true_value - ask
        else:
            return 0.0
    
    def save(self, filepath):
        """Save Q-table to disk."""
        data = {
            "q_table": dict(self.q_table),
            "alpha": self.alpha,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "training_history": self.training_history
        }
        with open(filepath, "wb") as f:
            pickle.dump(data, f)
        print(f"[RL] Agent saved to {filepath}")
    
    def load(self, filepath):
        """Load Q-table from disk."""
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        self.q_table = defaultdict(lambda: np.zeros(len(ACTIONS)), data["q_table"])
        self.alpha = data["alpha"]
        self.gamma = data["gamma"]
        self.epsilon = data["epsilon"]
        self.training_history = data.get("training_history", [])
        print(f"[RL] Agent loaded from {filepath} ({len(self.q_table)} states learned)")


# ---------------------------------------------------------------------------
# Simulated Player (for pre-training)
# ---------------------------------------------------------------------------

class SimulatedPlayer:
    """
    A configurable 'dummy' player used to pre-train the RL agent.
    Models different human quoting habits so the agent learns to
    exploit a range of strategies.
    """
    
    def __init__(self, style="balanced"):
        self.style = style
    
    def quote(self, true_value, round_num):
        """Generate a bid/ask quote based on player style."""
        noise = random.gauss(0, 10)
        
        if self.style == "tight":
            half_spread = random.uniform(3, 8)
        elif self.style == "wide":
            half_spread = random.uniform(25, 50)
        elif self.style == "biased_high":
            half_spread = random.uniform(8, 20)
            noise = abs(noise) + 10  # Midpoint always above true value
        elif self.style == "biased_low":
            half_spread = random.uniform(8, 20)
            noise = -(abs(noise) + 10)  # Midpoint always below
        elif self.style == "adaptive":
            # Gets tighter over rounds
            half_spread = max(5, 30 - round_num * 3)
            noise = random.gauss(0, 5)
        else:  # balanced
            half_spread = random.uniform(8, 25)
        
        midpoint = true_value + noise
        bid = midpoint - half_spread
        ask = midpoint + half_spread
        return bid, ask


def pretrain_agent(num_episodes=1500, rounds_per_game=10):
    """
    Pre-train the RL agent against simulated players with 
    different quoting styles so it arrives ready to exploit patterns.
    """
    agent = MarketMakerRLAgent(alpha=0.1, gamma=0.95, epsilon=0.2)
    styles = ["tight", "wide", "biased_high", "biased_low", "adaptive", "balanced"]
    
    print("="*60)
    print("   PRE-TRAINING RL MARKET MAKER AGENT")
    print("="*60)
    
    for episode in range(num_episodes):
        style = random.choice(styles)
        player = SimulatedPlayer(style=style)
        
        # Generate a true value for this game
        true_value = sum(random.uniform(0, 10) for _ in range(100))
        
        episode_pnl = 0.0
        inventory = 0
        
        for r in range(1, rounds_per_game + 1):
            bid, ask = player.quote(true_value, r)
            
            # Ensure bid < ask
            if bid >= ask:
                bid, ask = ask - 1, ask
            
            state = agent.get_state(bid, ask, true_value, inventory, r, rounds_per_game)
            action = agent.choose_action(state, training=True)
            reward = agent.calculate_reward(action, bid, ask, true_value)
            
            # Update inventory for next state
            action_name = ACTIONS[action]
            if action_name == "hit_bid":
                inventory += 1  # Player bought (player is long)
            elif action_name == "lift_offer":
                inventory -= 1  # Player sold (player is short)
            
            # Get next state (approximation: use same bid/ask since we don't know future quotes)
            next_state = agent.get_state(bid, ask, true_value, inventory, r + 1, rounds_per_game)
            agent.update(state, action, reward, next_state)
            
            episode_pnl += reward
        
        agent.training_history.append(episode_pnl)
        
        # Decay epsilon over time
        if episode % 200 == 0 and episode > 0:
            agent.epsilon = max(0.05, agent.epsilon * 0.8)
            
        # Progress logging
        if (episode + 1) % 300 == 0:
            recent_pnl = np.mean(agent.training_history[-300:])
            print(f"  Episode {episode+1}/{num_episodes} | "
                  f"Avg Agent P&L (last 300): ${recent_pnl:.2f} | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"States learned: {len(agent.q_table)}")
    
    # Save
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    save_path = os.path.join(model_dir, "market_maker_qtable.pkl")
    agent.save(save_path)
    
    print(f"\n  Training complete. Final avg P&L: ${np.mean(agent.training_history[-500:]):.2f}")
    print(f"  Total unique states explored: {len(agent.q_table)}")
    
    return agent


if __name__ == "__main__":
    pretrain_agent()
