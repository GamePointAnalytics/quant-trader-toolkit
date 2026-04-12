# Mental Math and Estimation Tricks

Quantitative trading interviews famously test your ability to perform rapid mental arithmetic. This is not just a parlor trick; traders need to quickly compute expected values, edge, and Greeks intuitively when markets are moving.

## 1. The Zetamac Drill
[Zetamac](https://arithmetic.zetamac.com/) is the gold standard for rapid mental math practice. It tests addition, subtraction, multiplication, and division under severe time pressure. A strong score is typically 60+ in 120 seconds, with top candidates easily scoring 80-100+.

### Multiplication Tricks (Crucial for Zetamac)

#### Multiplying numbers close to 100
Example: $96 \times 97$
1. Find differences from 100: $100 - 96 = 4$, $100 - 97 = 3$.
2. The last two digits are the product of differences: $4 \times 3 = 12$.
3. The first two digits are 100 minus the sum of differences: $100 - (4+3) = 93$.
**Answer: 9312**

#### Squaring numbers ending in 5
Example: $65^2$
1. Multiply the first digit by itself plus one: $6 \times (6+1) = 42$.
2. Append 25.
**Answer: 4225**

#### Multiplying by 11
Example: $43 \times 11$
1. Keep the first digit: $4$
2. Find the sum of the digits: $4+3=7$
3. Keep the last digit: $3$
**Answer: 473** *(Note: If the sum is $\geq 10$, carry over the 1).*

#### Difference of Squares (Highly tested!)
Whenever you see numbers equidistant from a "round" number.
Example: $48 \times 52$
1. Recognize this as $(50 - 2)(50 + 2)$.
2. Calculate $50^2 - 2^2 = 2500 - 4$.
**Answer: 2496**

## 2. Fractions to Decimals Cheatsheet
You must know these instantly to convert odds/probabilities to percentages:
- $1/6 \approx 16.67\%$
- $1/7 \approx 14.28\%$ (Double 7 is 14, double 14 is 28)
- $1/8 = 12.5\%$
- $1/9 \approx 11.11\%$
- $1/11 \approx 9.09\%$
- $1/12 \approx 8.33\%$

## 3. Estimation & Fermi Problems
Interviewers may ask questions with no exact answer to test your logic and approximation skills.

**Example:** "How many ping pong balls can fit in a Boeing 747?"
- **Always break it down into explicit assumptions.**
- "Assume a ping pong ball has a radius of $1.5 \text{ cm}$. Volume is roughly $4/3 \times \pi \times r^3 \approx 14 \text{ cm}^3$."
- "Assume a 747 is essentially a cylinder. It is $70 \text{ m}$ long with a $6 \text{ m}$ diameter..."
- Calculate the volume of the plane in cubic meters, convert to cubic cm.
- **Critical adjustment:** Add a packing fraction. Spheres do not pack perfectly; the optimal packing fraction is about $74\%$ ($\frac{\pi}{3\sqrt{2}}$), but simple cubic packing is $\approx 52\%$. Use something like $65\%$ to be realistic.

### The Rule of 72
To find out how many years it takes an investment to double given a fixed annual rate of interest, divide $72$ by the annual rate of return.
- If $r = 8\%$, it takes $72/8 = 9$ years to double.

## 4. Expected Value Quick Mental Shortcuts

**Sum of 1 to N:** $\frac{N(N+1)}{2}$
- Example: Sum of a 6-sided die = $21$.

**Expected value of a uniform discrete distribution 1 to N:** $\frac{N+1}{2}$
- Example: EV of a 6-sided die roll = $7/2 = 3.5$.

**Expected value of a uniform continuous distribution $[A, B]$:** $\frac{A+B}{2}$
- EV of $U(0, 1) = 0.5$.
