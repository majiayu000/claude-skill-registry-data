---
name: bignum-calculator
description: Arbitrary precision integer calculator for handling extremely large numbers. Use when users need to compute with numbers that exceed standard numeric limits, including operations like factorial of large numbers (e.g., 100!), powers with large exponents (e.g., 2^1000), arithmetic on numbers with hundreds of digits, or prime checking, GCD, LCM, Fibonacci, and binomial coefficients.
---

# Big Number Calculator

Perform arbitrary precision integer arithmetic using Python's native big integer support.

## Quick Start

Run the calculator script:

```bash
python scripts/bignum_calc.py <operation> <args...>
```

## Supported Operations

| Operation | Args | Example | Description |
|-----------|------|---------|-------------|
| `add` | a b | `add 999999999999999999 1` | Addition |
| `sub` | a b | `sub 1000000000000 1` | Subtraction |
| `mul` | a b | `mul 123456789 987654321` | Multiplication |
| `div` | a b | `div 1000000000000 7` | Integer division |
| `mod` | a b | `mod 1000000000007 1000000007` | Modulo |
| `pow` | base exp | `pow 2 1000` | Power (2^1000) |
| `fact` | n | `fact 100` | Factorial (100!) |
| `gcd` | a b | `gcd 123456789 987654321` | Greatest common divisor |
| `lcm` | a b | `lcm 12345 67890` | Least common multiple |
| `prime` | n | `prime 104729` | Check if prime |
| `digits` | n | `digits 12345678901234567890` | Count digits |
| `digitsum` | n | `digitsum 12345678901234567890` | Sum of digits |
| `fib` | n | `fib 1000` | n-th Fibonacci number |
| `binomial` | n k | `binomial 100 50` | Binomial coefficient C(n,k) |

## Examples

```bash
# Calculate 2^1000
python scripts/bignum_calc.py pow 2 1000

# Calculate 100!
python scripts/bignum_calc.py fact 100

# Calculate 1000th Fibonacci number
python scripts/bignum_calc.py fib 1000

# Check if a large number is prime
python scripts/bignum_calc.py prime 104729

# Calculate C(100, 50)
python scripts/bignum_calc.py binomial 100 50
```

## Direct Python Usage

For complex calculations, use Python directly:

```python
# Large factorial
import math
result = math.factorial(1000)
print(f"1000! has {len(str(result))} digits")

# Large power
result = 2 ** 10000
print(f"2^10000 has {len(str(result))} digits")

# Modular exponentiation (efficient)
result = pow(2, 1000000, 10**9 + 7)
```
