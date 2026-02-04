---
name: lp-duality
description: Takes the dual of a linear program (LP). Use when the user provides an LP in LaTeX or markdown and wants its dual, or asks about LP duality transformations.
---

# Taking the Dual of a Linear Program

Transform a primal LP into its dual using a systematic 7-step procedure that preserves interpretability at each step.

## When to Use

- User provides an LP (in LaTeX or markdown) and asks for its dual
- User wants to derive complementary slackness conditions
- User needs to verify primal-dual relationships

## Input Format

The primal LP should specify:
- Objective: `max` or `min` of a linear function
- Variables with sign constraints (non-negative, non-positive, or unrestricted)
- Linear constraints (inequalities `<=`, `>=`, or equalities `=`)

## Important Guidelines

1. **Work through all steps explicitly**: Do not skip steps or jump directly to the final dual. Each intermediate step must be shown to ensure correctness. The regrouping step (Step 5) especially requires careful attention to signs.

2. **Use suggestive variable names from the primal**: If the primal LP indicates names for dual variables (e.g., in brackets or parentheses next to constraints like `[λ_i]` or `(p_j)`), use those names in the dual derivation.

## The 7-Step Procedure

### Step 1: Rewrite as Minimization
If the objective is a maximization, negate it to get a minimization. This doesn't change optimal solutions.

### Step 2: Canonical Form
- Rewrite each inequality as `<= 0`
- Rearrange equalities so right-hand side is 0
- Keep variable sign constraints (under min/max) unchanged

### Step 3: Define Dual Variables
For each constraint, define a dual variable:
- **Inequality constraint** → non-negative dual variable (λ >= 0)
- **Equality constraint** → unrestricted dual variable

### Step 4: Form the Lagrangian
Remove each constraint and add to the objective:
```
(dual variable) × (left-hand side of constraint)
```
Maximize over dual variables, minimize over primal variables.

### Step 5: Regroup by Primal Variables
Rewrite the objective so each term has the form:
```
(primal variable) × (expression in dual variables)
```
plus terms involving only dual variables.

**This step requires great care with signs.**

### Step 6: Replace Terms with Dual Constraints
For each term `x × (expression)`:
- If x >= 0: constraint `expression >= 0`
- If x <= 0: constraint `expression <= 0`
- If x unrestricted: constraint `expression = 0`

**Intuition**: If the constraint were violated, the inner player could drive the objective to -∞.

### Step 7: Final Form
If the original was a maximization (converted in Step 1), convert back to minimization by negating.

Optionally rearrange constraints and substitute `λ ← -λ` for cleaner presentation.

## Key Correspondences

| Primal | Dual |
|--------|------|
| n variables | n constraints |
| m constraints | m variables |
| max objective | min objective |
| variable >= 0 | constraint >= |
| variable <= 0 | constraint <= |
| variable unrestricted | constraint = |
| constraint <= | variable >= 0 |
| constraint >= | variable <= 0 (or negate to >= 0) |
| constraint = | variable unrestricted |

## Output Format

Provide:
1. The primal in canonical form (after Steps 1-2)
2. The Lagrangian with dual variables identified (Step 4)
3. The regrouped form showing complementary slackness structure (Step 5)
4. The final dual LP (Step 7)

Format all LPs in the same notation style as the input (LaTeX or markdown).

## Complementary Slackness Conditions

The intermediate forms from Steps 4-5 directly yield complementary slackness conditions:

**From Step 4** (primal slackness): Each term `λ × (primal constraint LHS)` gives condition:
```
λ × (constraint expression) = 0
```

**From Step 5** (dual slackness): Each term `x × (dual constraint LHS)` gives condition:
```
x × (constraint expression) = 0
```

These can be written equivalently as implications (e.g., `λ > 0 ⟹ constraint is tight`).

## Worked Example

**Primal:**
```latex
\max_{x_1 \geq 0,\, x_2 \leq 0,\, x_3} v_1 x_1 + v_2 x_2 + v_3 x_3
\text{s.t.} \quad a_1 x_1 + x_2 + x_3 \leq b_1
\quad x_1 + a_2 x_2 = b_2
\quad a_3 x_3 \geq b_3
```

**After Steps 1-2** (canonical form):
```latex
\min_{x_1 \geq 0,\, x_2 \leq 0,\, x_3} -v_1 x_1 - v_2 x_2 - v_3 x_3
\text{s.t.} \quad a_1 x_1 + x_2 + x_3 - b_1 \leq 0
\quad x_1 + a_2 x_2 - b_2 = 0
\quad -a_3 x_3 + b_3 \leq 0
```

**Step 3**: Define λ_1 >= 0 (ineq), λ_2 unrestricted (eq), λ_3 >= 0 (ineq).

**Step 4** (Lagrangian):
```latex
\max_{\lambda_1 \geq 0, \lambda_2, \lambda_3 \geq 0} \min_{x_1 \geq 0, x_2 \leq 0, x_3}
-v_1 x_1 - v_2 x_2 - v_3 x_3
+ \lambda_1(a_1 x_1 + x_2 + x_3 - b_1)
+ \lambda_2(x_1 + a_2 x_2 - b_2)
+ \lambda_3(-a_3 x_3 + b_3)
```

**Step 5** (regrouped):
```latex
-b_1 \lambda_1 - b_2 \lambda_2 + b_3 \lambda_3
+ x_1(a_1 \lambda_1 + \lambda_2 - v_1)
+ x_2(\lambda_1 + a_2 \lambda_2 - v_2)
+ x_3(\lambda_1 - a_3 \lambda_3 - v_3)
```

**Step 6**: Apply constraint rules based on variable signs:
- x_1 >= 0 → a_1 λ_1 + λ_2 - v_1 >= 0
- x_2 <= 0 → λ_1 + a_2 λ_2 - v_2 <= 0
- x_3 unrestricted → λ_1 - a_3 λ_3 - v_3 = 0

**Step 7** (final dual):
```latex
\min_{\lambda_1 \geq 0, \lambda_2, \lambda_3 \geq 0}
b_1 \lambda_1 + b_2 \lambda_2 - b_3 \lambda_3
\text{s.t.} \quad a_1 \lambda_1 + \lambda_2 \geq v_1
\quad \lambda_1 + a_2 \lambda_2 \leq v_2
\quad \lambda_1 - a_3 \lambda_3 = v_3
```

## Key Theorems

**Strong Duality**: If an LP has an optimal solution, so does its dual, and the optimal values are equal (V_P = V_D).

**Complementary Slackness**: Feasible primal and dual solutions are both optimal if and only if all complementary slackness conditions hold.

| Primal Status | Dual Status |
|---------------|-------------|
| Finite optimum | Finite optimum |
| Unbounded | Infeasible |
| Infeasible | Unbounded or Infeasible |
