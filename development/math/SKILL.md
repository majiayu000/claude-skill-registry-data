---
name: math
description: General mathematical methods skill for symbolic and numerical work; use when solving equations or deriving relationships.
---

# Skill: Math

Domain: `build` | Depth: `axiom`

## Capabilities
- Symbolic computation: algebra, calculus, differential equations, series, limits (sympy)
- Arbitrary precision arithmetic (mpmath)
- Linear algebra: eigenvalues, SVD, matrix decomposition (numpy)
- Number theory: primes, modular arithmetic, combinatorics (sympy)
- Tensor operations and autograd (torch)

## Libraries
| Library | Purpose |
|---------|---------|
| sympy   | Symbolic math — exact, not approximate |
| mpmath  | Arbitrary precision floats |
| numpy   | Fast numerical arrays and linear algebra |
| torch   | Tensor math + autograd |

## Module
`agents/skills/math.py`

## Key Functions
- `symbolic(expr)` — parse and simplify symbolic expression
- `differentiate(expr, var)` — symbolic derivative
- `integrate(expr, var)` — symbolic integral
- `solve(expr, var)` — solve equation
- `eigenvalues(matrix)` — compute eigenvalues
- `precision_compute(expr, dps)` — arbitrary precision evaluation
