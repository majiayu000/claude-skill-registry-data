---
name: mean-variance-optimization
description: Performs mean-variance portfolio optimization to find the tangency portfolio. This skill should be used when users want to calculate optimal portfolio weights, the tangency portfolio, or perform mean-variance optimization with multiple assets. The skill interactively collects expected returns, standard deviations, correlations, and the risk-free rate, then computes and explains the tangency portfolio that maximizes the Sharpe ratio.
---

# Mean-Variance Optimization

## Purpose

This skill helps users perform mean-variance portfolio optimization to identify the tangency portfolio—the portfolio that maximizes the Sharpe ratio (reward-to-risk). The skill interactively gathers asset characteristics, constructs the covariance matrix, calculates optimal portfolio weights (allowing short sales), and provides detailed explanations of the results grounded in modern portfolio theory.

## When to Use This Skill

Use this skill when users want to:
- Calculate the tangency portfolio for multiple risky assets
- Determine optimal portfolio weights using mean-variance optimization
- Understand which assets to hold long or short and why
- Compute portfolio expected return, standard deviation, and Sharpe ratio
- Learn about the efficient frontier and capital allocation line

## Workflow

### 1. Gather Input Data Interactively

Ask the user for the following information in order:

1. **Number of assets** (n): "How many assets do you want to include in the portfolio?"

2. **For each asset i** (from 1 to n):
   - Expected return: "What is the expected return for Asset {i}? (Enter as a decimal, e.g., 0.10 for 10%)"
   - Standard deviation: "What is the standard deviation for Asset {i}? (Enter as a decimal, e.g., 0.20 for 20%)"

3. **Risk-free rate**: "What is the risk-free rate? (Enter as a decimal, e.g., 0.03 for 3%)"

4. **Correlations**: For n assets, collect n(n-1)/2 unique pairwise correlations
   - Explain: "I need the correlations between each pair of assets. For {n} assets, I need {n(n-1)/2} correlations."
   - For each pair (i, j) where i < j: "What is the correlation between Asset {i} and Asset {j}? (Enter a value between -1 and 1)"

**Input Validation:**
- Verify standard deviations are positive
- Verify correlations are between -1 and 1
- Verify the risk-free rate is reasonable

### 2. Construct the Covariance Matrix

Use the `scripts/optimize_portfolio.py` script to:
1. Build the n×n covariance matrix Σ where:
   - Diagonal elements: Σ_ii = σ_i² (variance)
   - Off-diagonal elements: Σ_ij = ρ_ij × σ_i × σ_j (covariance)
2. Display the covariance matrix clearly
3. Verify the matrix is positive definite

If the matrix is not positive definite, explain to the user that the correlation structure is inconsistent and optimization cannot proceed.

### 3. Calculate the Tangency Portfolio

Execute the optimization script to compute:

**Tangency portfolio weights** using the formula:
```
w* = Σ^(-1) × (μ - r_f × 1) / [1^T × Σ^(-1) × (μ - r_f × 1)]
```
where:
- μ is the vector of expected returns
- r_f is the risk-free rate
- 1 is a vector of ones
- Σ^(-1) is the inverse of the covariance matrix

**Portfolio statistics:**
- Expected return: E[R_p] = w^T × μ
- Standard deviation: σ_p = sqrt(w^T × Σ × w)
- Sharpe ratio: (E[R_p] - r_f) / σ_p

Display:
- Each asset's weight (rounded to 4 decimal places)
- Sum of weights (should equal 1.0000)
- Long positions (positive weights) and short positions (negative weights)
- Portfolio expected return, standard deviation, and Sharpe ratio

### 4. Explain the Results

Provide a comprehensive explanation covering:

**Why This is the Tangency Portfolio:**
- It maximizes the Sharpe ratio (reward per unit of risk)
- It represents the optimal risky portfolio for all risk-averse investors
- It's the point where the Capital Allocation Line (CAL) is tangent to the efficient frontier
- All investors should hold some combination of this portfolio and the risk-free asset

**Interpretation of Weights:**
- Identify which assets have positive weights (long positions) and explain why:
  - High expected returns relative to risk
  - Favorable correlation structure (low or negative correlations with other assets)
  - Strong contribution to diversification
- Identify which assets have negative weights (short positions) and explain why:
  - Low expected returns relative to risk
  - Can be used to fund purchases of better-performing assets
  - May have unfavorable correlations

**Economic Intuition:**
- Discuss why certain assets receive larger absolute allocations
- Explain the role of diversification in reducing portfolio risk below the weighted average of individual asset risks
- Highlight how correlations affect optimal weights (low/negative correlations increase diversification benefits)
- Discuss the impact of the risk-free rate on the optimal portfolio composition

**Mathematical Context:**
- Note that short sales are allowed (this is the unconstrained optimization)
- Mention that the tangency portfolio is part of the efficient frontier
- Explain that any efficient portfolio can be formed by combining the tangency portfolio with the risk-free asset

## Using the Optimization Script

The skill includes `scripts/optimize_portfolio.py` which performs all calculations. Execute it with:

```bash
python .claude/skills/mean-variance-optimization/scripts/optimize_portfolio.py
```

The script:
- Takes inputs for returns, standard deviations, correlations, and risk-free rate
- Constructs the covariance matrix
- Computes tangency portfolio weights
- Calculates portfolio statistics
- Outputs results in a clear, formatted manner

Read the script output and use it to formulate the explanation to the user.

## Key Financial Concepts

**Sharpe Ratio:** Measures excess return per unit of risk. Higher is better.

**Efficient Frontier:** The set of portfolios that offer the highest expected return for each level of risk.

**Tangency Portfolio:** The portfolio on the efficient frontier with the highest Sharpe ratio. It's "tangent" to the Capital Allocation Line.

**Capital Allocation Line (CAL):** The line connecting the risk-free asset to the tangency portfolio. All efficient portfolios lie on this line.

**Short Selling:** Selling borrowed assets (negative weights). Proceeds are used to buy more of other assets.

## Important Notes

- Always validate that the covariance matrix is positive definite before attempting optimization
- If optimization fails, explain the mathematical reason (e.g., singular matrix, numerical instability)
- Round displayed values to 4 decimal places for readability while maintaining precision in calculations
- Emphasize that this is a theoretical framework; practical implementation requires considering transaction costs, liquidity, and other real-world constraints
