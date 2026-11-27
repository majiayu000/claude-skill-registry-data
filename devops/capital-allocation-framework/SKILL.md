---
name: capital-allocation-framework
description: "Ranks competing investments using Net Present Value (NPV), Internal Rate of Return (IRR), payback period, Profitability Index (PI), and strategic option value - then produces a portfolio-level recommendation. Use when evaluating capital expenditure requests; comparing Mergers and Acquisitions (M&A) targets; sizing Research and Development (R&D) bets; prioritizing engineering investments; sun-setting initiatives; or preparing a board capital allocation memo."
---

# Capital Allocation Framework

> A disciplined process for ranking competing investments and producing a defensible capital plan.

## What this skill is

An end-to-end framework that combines quantitative return metrics - Net Present Value (NPV), Internal Rate of Return (IRR), payback, Profitability Index (PI) - with strategic option value and execution risk scoring. It surfaces the efficient frontier of investments, flags portfolio-level concentration risk, and produces a one-page memo a Chief Financial Officer (CFO) or board can actually approve.

## What it solves

- Ranking by IRR alone (which is scale-blind) instead of NPV
- Comparing projects of different durations without an Equivalent Annual Annuity (EAA) adjustment
- Treating "strategic" projects as exempt from financial discipline
- Approving full capital up front for unproven initiatives (no stage gates)
- Ignoring the option value of follow-on investments

## When to invoke

- Annual operating plan or capital expenditure budgeting cycle
- Mergers and Acquisitions (M&A) target ranking when multiple deals compete for the same capital
- Sun-setting decisions across a product portfolio
- Trade-offs between Research and Development (R&D), marketing, and infrastructure investment
- Pre-board preparation for any material capital deployment decision

## Phase 1: Inventory the opportunity set

Catalog every competing use of capital - including do-nothing, share buyback, dividend, and debt paydown:

| ID | Initiative | Sponsor | Ask ($M) | Horizon | Reversibility |
|----|-----------|---------|---------:|---------|---------------|
| 1 | [name] | [team] | $X | 3 years | Two-way / One-way |

Reject any submission missing sponsor, horizon, or success metric.

## Phase 2: Financial returns

**Net Present Value (NPV) - primary metric:**

```
NPV = Σ FCFt / (1 + r)^t − initial investment
```

where FCFt is the Free Cash Flow (FCF) in period t and r is the discount rate. Use the Weighted Average Cost of Capital (WACC) adjusted by project risk class (consumer versus enterprise, mature versus early-stage, geographic).

**Internal Rate of Return (IRR)** - flag multiple-IRR pitfalls for projects with interim negative cash flows.

**Payback (undiscounted and discounted)** - liquidity and execution-risk lens, not a primary ranking metric.

**Profitability Index (PI)** - use this, not NPV, when capital is rationed (ranks correctly per dollar invested).

**Equivalent Annual Annuity (EAA)** - required when comparing projects with different lifespans:

```
EAA = NPV × r / (1 − (1 + r)^−n)
```

## Phase 3: Strategic option value

NPV undervalues optionality. For each project, value each option type:

| Option type | Question | Driver |
|-------------|----------|--------|
| Expand | Does success unlock follow-on? | Decision tree or real-options model |
| Abandon | Can we kill cheaply on failure? | Limits downside |
| Defer | Can we wait for better information? | Volatility input |
| Switch | Can the asset be repurposed? | Salvage or alternative-use value |
| Scale | Are unit economics replicable across markets? | Multiplier |

Express each as a dollar range, even if rough.

## Phase 4: Risk adjustment

For each project:
- Scenario analysis: 10th-percentile (P10), median (P50), and 90th-percentile (P90) NPV
- Sensitivity tornado on top 5 drivers
- Monte Carlo simulation (≥ 1,000 trials) when inputs have known distributions
- Probability-of-success weighting for Research and Development (R&D) or venture-style bets

Decision rule: if the P10 NPV is negative, the project requires an explicit downside mitigation plan.

## Phase 5: Execution risk scoring

Score each project 1-5 on each dimension:

| Dimension | Weight |
|-----------|-------:|
| Team capability | 20% |
| Time-to-impact | 15% |
| Dependency risk | 15% |
| Capital flexibility | 15% |
| Strategic clarity | 15% |
| Competitive urgency | 10% |
| Cultural fit | 10% |

Multiply the weighted score × NPV → **risk-adjusted value**.

## Phase 6: Portfolio view

Rank opportunities and plot the efficient frontier:

| Rank | Initiative | NPV | PI | Risk-adjusted NPV | Option value | Cumulative capital |
|------|-----------|----:|---:|------------------:|-------------:|-------------------:|
| 1 | [name] | $X | x.xx | $Y | $Z | $X |

Draw cumulative capital versus cumulative NPV. The kink is the optimal capital envelope. Cross-check for:
- Concentration risk (any bet > 25% of total ask?)
- Time-bucket balance (under 2 years / 2-5 years / 5+ years)
- Capability cluster (stacking too many bets on one team?)
- Strategic theme balance (aligned with the 3 stated priorities?)

## Output

- Ranked initiative table with NPV, PI, risk-adjusted value, and option value
- Efficient-frontier chart with recommended capital envelope
- One-page memo: what's funded, what's deferred, what's killed - and why
- Capital flex scenarios (+20% / −20%) with what changes
- Stage-gate triggers for the top 3 bets
- Pre-mortem for each top-3 initiative

## Operating rules

**Always**
- Include "do nothing" as an option
- Show every input that produced the NPV
- Apply project-specific WACC, not blended
- Use PI when capital is constrained
- Quantify option value, even approximately
- Stage-gate large bets

**Never**
- Rank by IRR alone
- Compare different-horizon projects without EAA
- Treat strategic projects as exempt from NPV
- Hide downside scenarios
- Approve full capital up front for unproven initiatives
