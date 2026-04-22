"""
Sequence Pattern Classifier
============================
A supervised ML pipeline that classifies numerical sequences by their
underlying mathematical pattern. Uses the same generators from
sequence_puzzles.py to create labeled training data, engineers features
from the raw numbers, and trains a Random Forest classifier.

Classes:
  0: alternating_ops
  1: digit_sums
  2: powers_variant
  3: fractional_multiplier
  4: interleaved
  5: fibonacci_diff
  6: cubic_polynomial
"""

import numpy as np
import pickle
import os
import random
from collections import Counter

# Attempt sklearn import
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("[!] scikit-learn not installed. Run: pip install scikit-learn")

# ---------------------------------------------------------------------------
# Sequence Generators (mirrored from sequence_puzzles.py)
# ---------------------------------------------------------------------------

LABELS = [
    "alternating_ops",
    "digit_sums",
    "powers_variant",
    "fractional_multiplier",
    "interleaved",
    "fibonacci_diff",
    "cubic_polynomial"
]

def gen_alternating_ops():
    start = random.randint(2, 20)
    op1 = random.choice(['*', '+', '-'])
    op1_val = random.randint(2, 5) if op1 == '*' else random.randint(3, 15)
    op2 = random.choice(['*', '+', '-'])
    while op2 == op1:
        op2 = random.choice(['*', '+', '-'])
    op2_val = random.randint(2, 4) if op2 == '*' else random.randint(3, 15)
    
    seq = [start]
    for i in range(5):
        c = seq[-1]
        op, val = (op1, op1_val) if i % 2 == 0 else (op2, op2_val)
        if op == '*': seq.append(c * val)
        elif op == '+': seq.append(c + val)
        elif op == '-': seq.append(c - val)
    return seq

def gen_digit_sums():
    start = random.randint(15, 50)
    seq = [start]
    for _ in range(5):
        v = seq[-1]
        seq.append(v + sum(int(d) for d in str(abs(v))))
    return seq

def gen_powers_variant():
    var = random.choice(['cubic', 'exp', 'sq_prime'])
    seq = []
    if var == 'cubic':
        off = random.randint(-5, 5)
        for n in range(2, 8): seq.append(n**3 - n + off)
    elif var == 'exp':
        off = random.randint(-10, 10)
        for n in range(1, 7): seq.append(2**n + off)
    else:
        primes = [2, 3, 5, 7, 11, 13]
        for n in range(1, 7): seq.append(n**2 + primes[n-1])
    return seq

def gen_fractional_multiplier():
    start = random.choice([4, 6, 8, 12, 16])
    step = 0.5
    mult = random.choice([0.5, 1.0, 1.5])
    seq = [start]
    for _ in range(5):
        seq.append(int(seq[-1] * mult))
        mult += step
    return seq

def gen_interleaved():
    sA = random.randint(1, 10)
    dA = random.randint(5, 15)
    sB = random.randint(2, 5)
    rB = random.randint(2, 4)
    seqA = [sA + i*dA for i in range(3)]
    seqB = [sB * rB**i for i in range(3)]
    woven = []
    for i in range(3):
        woven.append(seqA[i])
        woven.append(seqB[i])
    return woven

def gen_fibonacci_diff():
    start = random.randint(2, 10)
    seq = [start]
    fib = [1, 1, 2, 3, 5, 8, 13]
    for i in range(5):
        seq.append(seq[-1] + fib[i])
    return seq

def gen_cubic_poly():
    a = random.randint(1, 2)
    b = random.randint(-3, 3)
    c = random.randint(-5, 5)
    d = random.randint(-10, 10)
    return [a*x**3 + b*x**2 + c*x + d for x in range(1, 7)]


GENERATORS = [
    gen_alternating_ops,
    gen_digit_sums,
    gen_powers_variant,
    gen_fractional_multiplier,
    gen_interleaved,
    gen_fibonacci_diff,
    gen_cubic_poly
]


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def extract_features(seq):
    """
    Given a raw numerical sequence, compute a feature vector that captures
    the mathematical structure without revealing the raw numbers.
    """
    seq = [float(x) for x in seq]
    n = len(seq)
    features = []
    
    # 1. First differences
    d1 = [seq[i+1] - seq[i] for i in range(n-1)]
    features.append(np.mean(d1) if d1 else 0)
    features.append(np.std(d1) if d1 else 0)
    features.append(max(d1) - min(d1) if d1 else 0)  # range of d1
    
    # 2. Second differences
    d2 = [d1[i+1] - d1[i] for i in range(len(d1)-1)]
    features.append(np.mean(d2) if d2 else 0)
    features.append(np.std(d2) if d2 else 0)
    
    # 3. Third differences
    d3 = [d2[i+1] - d2[i] for i in range(len(d2)-1)]
    features.append(np.mean(d3) if d3 else 0)
    features.append(np.std(d3) if d3 else 0)
    
    # 4. Ratios between consecutive terms
    ratios = []
    for i in range(n-1):
        if seq[i] != 0:
            ratios.append(seq[i+1] / seq[i])
        else:
            ratios.append(0)
    features.append(np.mean(ratios) if ratios else 0)
    features.append(np.std(ratios) if ratios else 0)
    
    # 5. Are first differences constant? (low std = arithmetic)
    features.append(1.0 if (d1 and np.std(d1) < 0.01) else 0.0)
    
    # 6. Are ratios constant? (low std = geometric)
    features.append(1.0 if (ratios and np.std(ratios) < 0.01) else 0.0)
    
    # 7. Are second differences constant? (low std = quadratic)
    features.append(1.0 if (d2 and np.std(d2) < 0.01) else 0.0)
    
    # 8. Are third differences constant? (low std = cubic)
    features.append(1.0 if (d3 and np.std(d3) < 0.01) else 0.0)
    
    # 9. Sequence length
    features.append(float(n))
    
    # 10. Do differences look Fibonacci-like? (d[i] ≈ d[i-1] + d[i-2])
    fib_score = 0
    if len(d1) >= 3:
        for i in range(2, len(d1)):
            if abs(d1[i] - (d1[i-1] + d1[i-2])) < 0.5:
                fib_score += 1
        fib_score /= (len(d1) - 2)
    features.append(fib_score)
    
    # 11. Alternating sign in differences?
    alt_score = 0
    if len(d1) >= 2:
        for i in range(1, len(d1)):
            if d1[i] * d1[i-1] < 0:
                alt_score += 1
        alt_score /= (len(d1) - 1)
    features.append(alt_score)
    
    # 12. Even/odd index patterns (for interleaved detection)
    if n >= 4:
        even_vals = [seq[i] for i in range(0, n, 2)]
        odd_vals = [seq[i] for i in range(1, n, 2)]
        even_d = [even_vals[i+1] - even_vals[i] for i in range(len(even_vals)-1)]
        odd_d = [odd_vals[i+1] - odd_vals[i] for i in range(len(odd_vals)-1)]
        features.append(np.std(even_d) if even_d else 999)
        features.append(np.std(odd_d) if odd_d else 999)
    else:
        features.append(999)
        features.append(999)
    
    # 13. Digit sum correlation
    digit_sums = [sum(int(c) for c in str(abs(int(x)))) for x in seq[:-1]]
    actual_diffs = [seq[i+1] - seq[i] for i in range(n-1)]
    ds_match = sum(1 for ds, ad in zip(digit_sums, actual_diffs) if abs(ds - ad) < 0.5) / max(len(digit_sums), 1)
    features.append(ds_match)
    
    return np.array(features, dtype=np.float64)


# ---------------------------------------------------------------------------
# Dataset Generation
# ---------------------------------------------------------------------------

def generate_dataset(num_samples_per_class=2000):
    """Generate labeled training data from our sequence generators."""
    X = []
    y = []
    
    for label_idx, gen in enumerate(GENERATORS):
        for _ in range(num_samples_per_class):
            try:
                seq = gen()
                feats = extract_features(seq)
                if not np.any(np.isnan(feats)) and not np.any(np.isinf(feats)):
                    X.append(feats)
                    y.append(label_idx)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
    
    return np.array(X), np.array(y)


# ---------------------------------------------------------------------------
# Training Pipeline
# ---------------------------------------------------------------------------

def train_classifier():
    """Train and save the sequence pattern classifier."""
    if not HAS_SKLEARN:
        print("[!] Cannot train without scikit-learn. Install it first.")
        return None
    
    print("=" * 60)
    print("   TRAINING SEQUENCE PATTERN CLASSIFIER")
    print("=" * 60)
    
    print("\n  Generating dataset (14,000 sequences)...")
    X, y = generate_dataset(num_samples_per_class=2000)
    print(f"  Dataset size: {len(X)} samples, {X.shape[1]} features")
    print(f"  Class distribution: {dict(Counter(y))}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest
    print("\n  Training Random Forest (200 trees)...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n  TEST ACCURACY: {acc*100:.1f}%\n")
    print(classification_report(y_test, y_pred, target_names=LABELS))
    
    # Feature importances
    importances = clf.feature_importances_
    feature_names = [
        "d1_mean", "d1_std", "d1_range",
        "d2_mean", "d2_std",
        "d3_mean", "d3_std",
        "ratio_mean", "ratio_std",
        "is_arithmetic", "is_geometric",
        "is_quadratic", "is_cubic",
        "seq_length",
        "fib_score", "alt_sign_score",
        "even_idx_std", "odd_idx_std",
        "digit_sum_match"
    ]
    
    print("  TOP 5 FEATURES:")
    top_idx = np.argsort(importances)[::-1][:5]
    for i, idx in enumerate(top_idx):
        print(f"    {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    save_path = os.path.join(model_dir, "sequence_classifier.pkl")
    
    with open(save_path, "wb") as f:
        pickle.dump(clf, f)
    print(f"\n  Model saved to {save_path}")
    
    return clf


def predict_pattern(clf, seq):
    """Given a trained classifier and a raw sequence, predict the pattern type."""
    feats = extract_features(seq).reshape(1, -1)
    proba = clf.predict_proba(feats)[0]
    pred_idx = np.argmax(proba)
    confidence = proba[pred_idx]
    return LABELS[pred_idx], confidence, dict(zip(LABELS, proba))


if __name__ == "__main__":
    train_classifier()
