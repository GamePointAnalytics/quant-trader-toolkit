"""
Sequence Puzzles with ML Hint Mode
====================================
The same hardcore sequence drill, but now with an optional ML-powered
hint system. When you're stuck, type 'h' and a trained Random Forest
classifier will tell you what pattern type it thinks the sequence is,
along with its confidence score.

This trains you to recognize the same structural features the ML model
uses (differences, ratios, interleaving patterns).
"""

import random
import sys
import os
import time
import pickle
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ml.sequence_classifier import extract_features, LABELS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "sequence_classifier.pkl")

# ---------------------------------------------------------------------------
# Sequence Generators (same as sequence_puzzles.py)
# ---------------------------------------------------------------------------

def seq_alternating_operations():
    start = random.randint(2, 20)
    op1_type = random.choice(['*', '+', '-'])
    op1_val = random.randint(2, 5) if op1_type in ['*', '/'] else random.randint(3, 15)
    op2_type = random.choice(['*', '+', '-'])
    while op2_type == op1_type:
        op2_type = random.choice(['*', '+', '-'])
    op2_val = random.randint(2, 4) if op2_type in ['*', '/'] else random.randint(3, 15)
    seq = [start]
    for i in range(5):
        current = seq[-1]
        op = op1_type if i % 2 == 0 else op2_type
        val = op1_val if i % 2 == 0 else op2_val
        if op == '*': next_v = current * val
        elif op == '+': next_v = current + val
        elif op == '-': next_v = current - val
        seq.append(next_v)
    return seq[:-1], seq[-1], f"Alternating Operations: first '{op1_type}{op1_val}', then '{op2_type}{op2_val}'"

def seq_digit_sums():
    start = random.randint(15, 50)
    seq = [start]
    for _ in range(5):
        val = seq[-1]
        digit_sum = sum(int(d) for d in str(val))
        seq.append(val + digit_sum)
    return seq[:-1], seq[-1], "Recursive Digit Sums: Next = Current + Sum of its digits."

def seq_powers_variant():
    var_type = random.choice(['cubic', 'exp2_offset', 'square_plus_prime'])
    seq = []
    if var_type == 'cubic':
        offset = random.randint(-5, 5)
        for n in range(2, 8): seq.append((n**3) - n + offset)
        return seq[:-1], seq[-1], "Algebraic: n^3 - n + offset"
    elif var_type == 'exp2_offset':
        offset = random.randint(1, 10) * random.choice([1, -1])
        for n in range(1, 7): seq.append((2**n) + offset)
        return seq[:-1], seq[-1], "Exponential offset: 2^n + constant"
    else:
        primes = [2, 3, 5, 7, 11, 13, 17]
        for n in range(1, 7): seq.append((n**2) + primes[n-1])
        return seq[:-1], seq[-1], "Squares + corresponding Prime number"

def seq_fractional_multiplier():
    start = random.choice([4, 6, 8, 12, 16])
    step = 0.5
    current_mult = random.choice([0.5, 1.0, 1.5])
    seq = [start]
    for _ in range(5):
        v = seq[-1] * current_mult
        seq.append(int(v))
        current_mult += step
    return seq[:-1], seq[-1], "Increasing Fractional Multiplier (e.g. *1.0, *1.5, *2.0, *2.5...)"

def seq_interleaving_hard():
    startA = random.randint(1, 10)
    diffA = random.randint(5, 15)
    startB = random.randint(2, 5)
    ratioB = random.randint(2, 4)
    seqA = [startA + (i * diffA) for i in range(4)]
    seqB = [startB * (ratioB ** i) for i in range(4)]
    woven = []
    for i in range(4):
        woven.append(seqA[i])
        woven.append(seqB[i])
    return woven[:-1], woven[-1], "Interleaved Hard: Sequence A is Arithmetic, Sequence B is Geometric."

def seq_running_diff_fibonacci():
    start = random.randint(2, 10)
    seq = [start]
    fib = [1, 1, 2, 3, 5, 8, 13, 21]
    for i in range(5):
        seq.append(seq[-1] + fib[i])
    return seq[:-1], seq[-1], "Fibonacci Differences: The differences between elements form a Fibonacci sequence."

def seq_polynomial_cubic():
    a = random.randint(1, 2)
    b = random.randint(-3, 3)
    c = random.randint(-5, 5)
    d = random.randint(-10, 10)
    seq = []
    for x in range(1, 7):
        val = (a*(x**3)) + (b*(x**2)) + (c*x) + d
        seq.append(val)
    return seq[:-1], seq[-1], "Cubic Polynomial: a*x^3 + b*x^2 + c*x + d"


# ---------------------------------------------------------------------------
# Game Loop
# ---------------------------------------------------------------------------

def load_classifier():
    """Load the pre-trained sequence classifier."""
    if not os.path.exists(MODEL_PATH):
        print("  [!] No trained classifier found.")
        print("  [!] Run `python -m ml.sequence_classifier` to train it first.")
        return None
    
    with open(MODEL_PATH, "rb") as f:
        clf = pickle.load(f)
    print(f"  ML Classifier loaded ({clf.n_estimators} trees).")
    return clf


def get_ml_hint(clf, seq):
    """Ask the ML classifier what pattern type this sequence is."""
    feats = extract_features(seq).reshape(1, -1)
    proba = clf.predict_proba(feats)[0]
    pred_idx = np.argmax(proba)
    confidence = proba[pred_idx]
    
    # Get top 3 predictions
    top3_idx = np.argsort(proba)[::-1][:3]
    
    print("\n  ┌─────────────────────────────────────────┐")
    print("  │           🤖 ML PATTERN HINT            │")
    print("  ├─────────────────────────────────────────┤")
    for rank, idx in enumerate(top3_idx):
        bar_len = int(proba[idx] * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        marker = " ◄" if rank == 0 else ""
        print(f"  │ {LABELS[idx]:>21s}  {bar} {proba[idx]*100:5.1f}%{marker} │")
    print("  └─────────────────────────────────────────┘\n")


def play_sequence_game(num_questions=15):
    generators = [
        seq_alternating_operations,
        seq_digit_sums,
        seq_powers_variant,
        seq_fractional_multiplier,
        seq_interleaving_hard,
        seq_running_diff_fibonacci,
        seq_polynomial_cubic
    ]
    
    print("\n" + "=" * 60)
    print("   ADVANCED SEQUENCE DRILLS  (ML Hint Mode)")
    print("=" * 60)
    
    clf = load_classifier()
    hint_mode = clf is not None
    
    if hint_mode:
        print("  Type 'h' at any time to get an ML-powered pattern hint.")
    print("  Type 'q' to quit.\n")
    
    score = 0
    hints_used = 0
    start_time = time.time()
    last_input = ""
    
    for i in range(num_questions):
        gen = random.choice(generators)
        seq, ans, explanation = gen()
        
        print("-" * 60)
        seq_str = "  ,  ".join(map(str, seq)) + "  ,  ???"
        
        print(f"QUESTION [{i+1}/{num_questions}]")
        print(f"\n   >>>   {seq_str}   <<<\n")
        sys.stdout.flush()
        
        used_hint = False
        
        while True:
            user_input = input("Your Guess (or 'h' for hint): ").strip()
            
            if user_input.lower() == 'q':
                last_input = 'q'
                print("\nQuitting game early...")
                break
            
            if user_input.lower() == 'h' and hint_mode:
                get_ml_hint(clf, seq)
                hints_used += 1
                used_hint = True
                continue
            
            # Attempt to answer
            try:
                if int(user_input) == ans:
                    if used_hint:
                        print("✅ CORRECT! (with hint)")
                    else:
                        print("✅ CORRECT!")
                    score += 1
                else:
                    print(f"❌ WRONG! The correct answer was: {ans}")
                    print(f"   [Logic] {explanation}")
                last_input = user_input
                break
            except ValueError:
                print(f"❌ INVALID INPUT! The answer was: {ans}")
                last_input = user_input
                break
        
        if last_input == 'q':
            break
        
        time.sleep(0.8)
        print("\n")
    
    elapsed = time.time() - start_time
    answered = i + 1 if last_input != 'q' else i
    
    print("+" * 60)
    print(f"  FINAL SCORE:    {score}/{answered}")
    print(f"  TOTAL TIME:     {elapsed:.1f} seconds")
    print(f"  HINTS USED:     {hints_used}")
    if elapsed > 0 and score > 0:
        print(f"  SPEED:          {(elapsed/score):.1f} sec / correct answer")
    if hints_used > 0:
        print(f"  HINT RELIANCE:  {hints_used/max(answered,1)*100:.0f}% of questions")
    print("+" * 60)


if __name__ == "__main__":
    try:
        play_sequence_game()
    except KeyboardInterrupt:
        print("\nExiting game.")
