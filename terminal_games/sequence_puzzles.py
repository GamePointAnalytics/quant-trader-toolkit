import random
import sys
import time

def seq_alternating_operations():
    # Example: *2, -3, *2, -3 or +5, /2, +5, /2
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
        # alternate based on index
        op = op1_type if i % 2 == 0 else op2_type
        val = op1_val if i % 2 == 0 else op2_val
        
        if op == '*': next_v = current * val
        elif op == '+': next_v = current + val
        elif op == '-': next_v = current - val
        seq.append(next_v)
        
    return seq[:-1], seq[-1], f"Alternating Operations: first '{op1_type}{op1_val}', then '{op2_type}{op2_val}'"

def seq_digit_sums():
    # X_n = X_{n-1} + sum of digits of X_{n-1}
    start = random.randint(15, 50)
    seq = [start]
    for _ in range(5):
        val = seq[-1]
        digit_sum = sum(int(d) for d in str(val))
        seq.append(val + digit_sum)
    return seq[:-1], seq[-1], "Recursive Digit Sums: Next = Current + Sum of its digits."

def seq_powers_variant():
    # n^3 - n, or 2^n - n, or n^2 + p_n
    var_type = random.choice(['cubic', 'exp2_offset', 'square_plus_prime'])
    seq = []
    
    if var_type == 'cubic':
        offset = random.randint(-5, 5)
        for n in range(2, 8):
            seq.append((n**3) - n + offset)
        return seq[:-1], seq[-1], "Algebraic: n^3 - n + offset"
        
    elif var_type == 'exp2_offset':
        offset = random.randint(1, 10) * random.choice([1, -1])
        for n in range(1, 7):
            seq.append((2**n) + offset)
        return seq[:-1], seq[-1], "Exponential offset: 2^n + constant"
        
    else:
        primes = [2, 3, 5, 7, 11, 13, 17]
        for n in range(1, 7):
            seq.append((n**2) + primes[n-1])
        return seq[:-1], seq[-1], "Squares + corresponding Prime number (e.g. 1^2+2, 2^2+3, 3^2+5...)"

def seq_fractional_multiplier():
    # e.g., multiply by 1.5, then 2.0, then 2.5
    start = random.choice([4, 6, 8, 12, 16])
    step = 0.5
    current_mult = random.choice([0.5, 1.0, 1.5])
    
    seq = [start]
    for _ in range(5):
        v = seq[-1] * current_mult
        seq.append(int(v)) # should stay integer if chosen carefully, else will truncate
        current_mult += step
        
    return seq[:-1], seq[-1], "Increasing Fractional Multiplier (e.g. *1.0, *1.5, *2.0, *2.5...)"

def seq_interleaving_hard():
    # One is arithmetic, one is geometric or powers
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
    # The differences between numbers form a Fibonacci sequence
    start = random.randint(2, 10)
    seq = [start]
    fib = [1, 1, 2, 3, 5, 8, 13, 21]
    
    for i in range(5):
        seq.append(seq[-1] + fib[i])
        
    return seq[:-1], seq[-1], "Fibonacci Differences: The differences between elements form a Fibonacci sequence."

def seq_polynomial_cubic():
    # Difference of difference of differences is constant
    a = random.randint(1, 2)
    b = random.randint(-3, 3)
    c = random.randint(-5, 5)
    d = random.randint(-10, 10)
    
    seq = []
    for x in range(1, 7):
        val = (a*(x**3)) + (b*(x**2)) + (c*x) + d
        seq.append(val)
        
    return seq[:-1], seq[-1], "Cubic Polynomial: a*x^3 + b*x^2 + c*x + d"


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
    
    # Header block
    print("\n" + "="*60)
    print("      ADVANCED QUANT SEQUENCE DRILLS (Hardcore Mode)")
    print("="*60)
    print("Find the next number. The patterns are extremely niche.")
    print("Look for interleaving, digit sums, and mixed operations.")
    print("Type 'q' to quit at any time.\n")
    
    score = 0
    start_time = time.time()
    
    for i in range(num_questions):
        gen = random.choice(generators)
        seq, ans, explanation = gen()
        
        # Spacer for visibility / scrolling
        print("-" * 60)
        seq_str = "  ,  ".join(map(str, seq)) + "  ,  ???"
        
        print(f"QUESTION [{i+1}/{num_questions}]")
        print(f"\n   >>>   {seq_str}   <<<\n")
        
        sys.stdout.flush() # Force flush to terminal
        
        user_input = input("Your Guess: ")
        if user_input.strip().lower() == 'q':
            print("\nQuitting game early...")
            break
            
        try:
            if int(user_input.strip()) == ans:
                print("✅ CORRECT!")
                score += 1
            else:
                print(f"❌ WRONG! The correct answer was: {ans}")
                print(f"   [Logic] {explanation}")
        except ValueError:
            print(f"❌ INVALID INPUT! The answer was: {ans}")
            
        # Short pause so it doesn't instantly scroll away
        time.sleep(1.0)
        print("\n") # Extra lines for massive scroll distinction
            
    elapsed = time.time() - start_time
    print("+"*60)
    print(f"FINAL SCORE: {score}/{i+1 if user_input.lower()=='q' else num_questions}")
    print(f"TOTAL TIME:  {elapsed:.1f} seconds")
    if elapsed > 0 and score > 0:
        print(f"SPEED:       {(elapsed/score):.1f} sec / correct answer")
    print("+"*60)

if __name__ == "__main__":
    try:
        play_sequence_game()
    except KeyboardInterrupt:
        print("\nExiting game.")
