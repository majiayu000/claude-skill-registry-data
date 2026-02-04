---
name: mip-modeling-expert
description: Use when formulating mixed integer programming (MIP) models, handling discontinuous variables, modeling logical constraints (either-or, conditional), or linearizing nonlinear terms
---

# MIP Modeling Expert

## When to Use This Skill

Use this skill when you need help with:
- **Modeling discontinuous variables** (variables that must be 0 or within specific bounds)
- **Handling fixed costs** or setup costs in optimization models
- **Formulating either-or constraints** (at least one of two constraints must hold)
- **Conditional constraints** (if constraint A holds, then constraint B must hold)
- **Piecewise linear approximations** of nonlinear functions
- **Special Ordered Sets** (SOS1, SOS2) for efficient branch-and-bound
- **Linearizing products of variables** (binary × binary, binary × continuous, continuous × continuous)
- **Converting nonlinear models to MIP** formulations

## Overview

This skill provides expert guidance on **Integer Linear Programming Tricks** based on the AIMMS Modeling Guide. These techniques transform complex, nonlinear, or logical requirements into linear integer programming formulations that can be solved by modern MIP solvers (CPLEX, Gurobi, etc.).

**Core Principle:** Many practical optimization problems cannot be formulated as pure linear programs because they involve:
- Discontinuities (jumps in cost functions or variable bounds)
- Logical decisions (either-or, if-then relationships)
- Nonlinear terms (products of variables, quadratic functions)

These challenges can be addressed using **indicator variables** (binary 0-1 variables) and **Big-M formulations**.

## Key Techniques

### 1. Indicator Variables

**Binary indicator variables** are the foundation of most MIP tricks. An indicator variable `y ∈ {0,1}` signals a specific state:

```
y = 0  →  State A
y = 1  →  State B
```

### 2. Discontinuous Variables

**Problem:** A variable must be either 0 OR within bounds [l, u]:

```
x = 0  or  l ≤ x ≤ u
```

**Solution:** Introduce binary indicator `y`:

```
x ≤ uy
x ≥ ly
y binary
```

When `y=0`: `x=0`. When `y=1`: `l ≤ x ≤ u`.

**Applications:**
- Batch size restrictions (suppliers require minimum order quantities)
- Setup costs in manufacturing

### 3. Fixed Costs

**Problem:** Cost function with a jump discontinuity:

```
C(x) = {  0        if x = 0
       {  k + cx   if x > 0
```

where `k` is the fixed cost and `c` is the variable cost.

**Solution:** Introduce binary `y` and upper bound `u`:

```
Minimize:  ky + cx

Subject to:
    x ≤ uy
    x ≥ 0
    y binary
```

When `y=0`: forces `x=0`, cost is 0. When `y=1`: allows `x>0`, cost is `k + cx`.

**Applications:**
- Equipment setup costs
- Opening a facility or warehouse

### 4. Either-Or Constraints

**Problem:** At least one of two constraints must hold:

```
Constraint (1): Σ a₁ⱼxⱼ ≤ b₁   OR
Constraint (2): Σ a₂ⱼxⱼ ≤ b₂
```

**Solution:** Use binary `y` and Big-M constants `M₁`, `M₂`:

```
Σ a₁ⱼxⱼ ≤ b₁ + M₁y
Σ a₂ⱼxⱼ ≤ b₂ + M₂(1-y)
y binary
```

When `y=0`: Constraint (1) is enforced, (2) is relaxed
When `y=1`: Constraint (2) is enforced, (1) is relaxed

**Critical:** Choose `M` values as tight as possible while ensuring they don't restrict feasible solutions.

**Applications:**
- Alternative production modes
- Route selection

### 5. Conditional Constraints (If-Then)

**Problem:** If constraint (1) holds, then constraint (2) must hold:

```
If  Σ a₁ⱼxⱼ ≤ b₁  then  Σ a₂ⱼxⱼ ≤ b₂
```

**Logical Equivalence:**
```
(A → B)  ≡  (¬A ∨ B)
```

This translates to: "Either constraint (1) is violated OR constraint (2) holds"

**Solution:** Use binary `y`, Big-M `M`, lower bound `L`, and small tolerance `ε`:

```
Σ a₁ⱼxⱼ ≥ b₁ + ε - Ly
Σ a₂ⱼxⱼ ≤ b₂ + M(1-y)
y binary
```

**Applications:**
- Safety constraints that activate when production exceeds thresholds
- Regulatory requirements

### 6. Special Ordered Sets (SOS)

#### SOS Type 1 (SOS1)

**Definition:** At most ONE variable in the set can be nonzero.

```
Σᵢ yᵢ ≤ 1   (where yᵢ are 0-1 variables)
```

More generally, for continuous variables `0 ≤ xᵢ ≤ uᵢ`:
```
Σᵢ aᵢxᵢ ≤ b   with at most one xᵢ nonzero
```

**Performance:** When variables have a natural ordering, solvers use specialized branching strategies that reduce the search tree.

**Example:** Warehouse size must be exactly one of: {10000, 20000, 40000, 50000} sq ft.

```
x₁ + x₂ + x₃ + x₄ = 1  (SOS1)
size = 10000x₁ + 20000x₂ + 40000x₃ + 50000x₄
```

#### SOS Type 2 (SOS2)

**Definition:** At most TWO variables can be nonzero, and they must be **adjacent** in the ordering.

Used extensively in piecewise linear approximations (see below).

### 7. Piecewise Linear Approximations

**Problem:** Approximate a nonlinear function `f(x)` with a piecewise linear function.

**Requirements:**
- Function must be **separable**: `F(x₁, x₂, ...) = f₁(x₁) + f₂(x₂) + ...`
- Define **breakpoints**: `x₁, x₂, x₃, ..., xₙ`

**λ-Formulation:**

For breakpoints `x₁, x₂, x₃, x₄` with function values `f(x₁), f(x₂), f(x₃), f(x₄)`:

```
x = λ₁x₁ + λ₂x₂ + λ₃x₃ + λ₄x₄
f̃(x) = λ₁f(x₁) + λ₂f(x₂) + λ₃f(x₃) + λ₄f(x₄)
λ₁ + λ₂ + λ₃ + λ₄ = 1
λᵢ ≥ 0
```

Plus the **adjacency requirement:** At most two adjacent λᵢ can be nonzero.

This is exactly a **SOS2 constraint**.

**When Adjacency is Redundant:**
- **Minimizing convex functions** (slopes are non-decreasing)
- **Maximizing concave functions** (slopes are non-increasing)

In these cases, the LP relaxation automatically satisfies adjacency, and no MIP solve is needed!

**When MIP is Required:**
- Non-convex functions (adjacency must be enforced with SOS2)

**Example:** Approximate `f(x) = ½x²` on [0,4] with breakpoints at 0, 1, 2, 4:

```
Breakpoints:     x:  0   1   2   4
Function values: f:  0  0.5  2   8

x = λ₁·0 + λ₂·1 + λ₃·2 + λ₄·4
f̃ = λ₁·0 + λ₂·0.5 + λ₃·2 + λ₄·8
λ₁ + λ₂ + λ₃ + λ₄ = 1  (SOS2)
```

### 8. Eliminating Products of Variables

#### Product of Two Binary Variables

**Problem:** Linearize `y = x₁x₂` where `x₁, x₂ ∈ {0,1}`

**Solution:**
```
y ≤ x₁
y ≤ x₂
y ≥ x₁ + x₂ - 1
y binary
```

#### Product of Binary and Continuous

**Problem:** Linearize `y = x₁x₂` where `x₁ ∈ {0,1}` and `0 ≤ x₂ ≤ u`

**Solution:**
```
y ≤ ux₁
y ≤ x₂
y ≥ x₂ - u(1 - x₁)
y ≥ 0
```

Verification:
- If `x₁=0`: constraints force `y=0`
- If `x₁=1`: constraints force `y=x₂`

#### Product of Two Continuous Variables

**Problem:** Linearize `x₁x₂` where both are continuous

**Solution:** Convert to separable form using:
```
y₁ = ½(x₁ + x₂)
y₂ = ½(x₁ - x₂)

Then: x₁x₂ = y₁² - y₂²
```

Now approximate `y₁²` and `y₂²` using piecewise linear functions.

**Special Case:** If `l₁, l₂ ≥ 0` and `x₁` appears ONLY in products, substitute `z = x₁x₂` and add:
```
l₁x₂ ≤ z ≤ u₁x₂
```

## Quick Reference Patterns

### Pattern 1: Binary Indicator Linking

```
Variable x must satisfy:  x = 0  OR  l ≤ x ≤ u

Formulation:
    x ≤ uy
    x ≥ ly
    y ∈ {0,1}
```

### Pattern 2: Big-M Constraint Activation

```
Binary y controls whether constraint is active:

y=0: Constraint enforced
y=1: Constraint relaxed

Formulation:
    Σ aⱼxⱼ ≤ b + My
```

### Pattern 3: SOS2 Piecewise Linear

```
For convex minimization or concave maximization:
    Just use λ-formulation (adjacency is automatic)

For non-convex:
    Mark the convexity constraint as SOS2 property
```

### Pattern 4: Product Linearization

```
Binary × Binary:      3 constraints + 1 binary variable
Binary × Continuous:  4 constraints + 1 continuous variable
Continuous × Continuous: Convert to separable, then use piecewise linear
```

## Common Applications

1. **Production Planning**
   - Setup costs (fixed cost trick)
   - Batch size restrictions (discontinuous variables)
   - Minimum production runs

2. **Logistics**
   - Facility location with fixed opening costs
   - Route selection (either-or constraints)
   - Vehicle capacity restrictions

3. **Scheduling**
   - Machine setup times
   - Conditional precedence constraints
   - Time windows

4. **Finance**
   - Portfolio optimization with transaction costs
   - Quantity discounts (piecewise linear)
   - Conditional investments

5. **Energy Systems**
   - Unit commitment (generators on/off with startup costs)
   - Alternative fuel sources (either-or)
   - Nonlinear efficiency curves

## Best Practices

1. **Choose Big-M Values Carefully**
   - Too large: numerical instability, weak LP relaxation
   - Too small: may cut off feasible solutions
   - Best: Derive from problem-specific bounds

2. **Use SOS When Natural Ordering Exists**
   - Dramatically reduces branch-and-bound nodes
   - Don't force SOS on unordered sets

3. **Exploit Convexity**
   - Check if piecewise linear functions are convex/concave
   - If yes, solve as LP (no MIP needed)

4. **Minimize Binary Variables**
   - Each binary variable roughly doubles potential search nodes
   - Look for reformulations that reduce binary count

5. **Preprocessing**
   - Tighten variable bounds before modeling
   - Enables smaller Big-M values
   - Improves solver performance

## Implementation in Modeling Languages

### AIMMS
- Use `Property` attribute for SOS1/SOS2 constraints
- Solver automatically recognizes and exploits SOS structure

### AMPL/Pyomo/JuMP
- Explicitly declare SOS sets
- Solver interfaces pass SOS information to solver

### GAMS
- Special syntax for SOS1/SOS2 sets
- Integrated with major solvers

## Further Reading

See reference files for detailed examples:
- `references/indicator_variables.md` - Binary indicator techniques
- `references/either_or_conditional.md` - Logical constraints
- `references/sos_sets.md` - Special Ordered Sets
- `references/piecewise_linear.md` - Nonlinear approximation
- `references/product_elimination.md` - Linearization techniques
- `references/examples.md` - Complete worked examples

## References

Based on Chapter 7 "Integer Linear Programming Tricks" from **AIMMS Modeling Guide** (AIMMS 4, 1993-2018)

Key sources:
- E.M.L. Beale and J.A. Tomlin (1969) - Special Ordered Sets
- H.P. Williams (1990) - Model Building in Mathematical Programming
