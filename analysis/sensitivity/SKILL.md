---
description: Analyze the impact of individual variables on financial outcomes
---

# Sensitivity

Analyze variable sensitivity for "$ARGUMENTS". Determine which inputs have the greatest impact on key financial outputs to prioritize risk management and decision-making.

## Prerequisites

None — utility skill, run anytime. Works best when financial data exists in `.metapowers/finance/$ARGUMENTS/`.

## Process

1. **Gather context:**
   - If prior phase artifacts exist, read them for baseline assumptions
   - Identify the output metrics to test (revenue, EBITDA, cash runway, valuation)
   - Determine the base case values for all input variables

2. **Select variables to test:**
   - Revenue drivers: growth rate, churn rate, ARPU, conversion rate
   - Cost drivers: headcount, cost per hire, vendor costs, COGS
   - Capital drivers: payment terms, collection period, funding timing
   - Choose 6-10 variables with the most uncertainty

3. **Run one-at-a-time analysis:**
   - For each variable, calculate the output when the variable moves +/- 10%, 20%, 30%
   - Hold all other variables constant at base case
   - Rank variables by impact magnitude (tornado chart data)

4. **Run two-variable data tables:**
   - Pick the top 2-3 most impactful variables
   - Create data tables showing output for combinations of values
   - Identify "danger zones" where combinations produce unacceptable outcomes

5. **Identify breakeven thresholds:**
   - For each key variable, find the value at which the business breaks even
   - Calculate the margin of safety (how far current value is from breakeven)

6. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/sensitivity.md` with sections:
   - **Variables Tested** — list of inputs, base values, and ranges
   - **Tornado Chart Data** — ranked impact of each variable on key outputs
   - **Data Tables** — two-variable sensitivity matrices
   - **Breakeven Thresholds** — critical values for each variable
   - **Risk Prioritization** — which variables to monitor most closely

## Output

The sensitivity analysis written to `.metapowers/finance/$ARGUMENTS/sensitivity.md`. Present a summary highlighting:
- Top 3 most impactful variables
- Breakeven thresholds for critical inputs
- Highest-risk combinations
