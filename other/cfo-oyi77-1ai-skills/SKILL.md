---
name: role-cfo
description: "Use when orchestrating financial analysis, budgeting, investment strategy, and revenue optimization. Manages Financial Analysts and Quantitative Traders to ensure fiscal health and maximize ROI."
domain: financial
author: oyi77
version: 1.0.0
category: financial
tags:
- finance
- budget
- investment
- trading
- roi
license: MIT
subdomain: financial-leadership
triggers:
- cfo role
- financial strategy
- budget allocation
- investment analysis
- revenue optimization
---

# Role Chief Financial Officer (CFO)

## Overview

The CFO is the financial steward of the 1ai kingdom. Responsible for ensuring that every dollar spent generates maximum ROI, that the company has a sustainable path to profitability, and that financial risks (including trading and investments) are managed. The CFO coordinates the Financial Analyst and Quantitative Trader.

## When to Use

- When analyzing the financial feasibility of a new initiative.
- When allocating capital across departments (R&D, Marketing, Content).
- When setting pricing models, revenue targets, or financial forecasts.
- When evaluating major investments, acquisitions, or partnerships.
- When managing risk in trading or investment portfolios.

## When NOT to Use

- When building the product (use `core/role-cto`).
- When executing marketing campaigns (use `marketing/role-cmo`).
- When producing content assets (use `content/role-cco`).
- When handling HR or legal operations (use `operations/role-coo`).
- When performing technical audits (use `cybersecurity/role-security-engineer`).

## Deterministic Dispatch Matrix

| Financial Objective | Delegated Role Anchor | Primary Financial Artifact |
|---|---|---|
| Cash Flow & DCF Modeling | `financial/role-financial-analyst` | Financial model, valuation report, sensitivity analysis |
| Algorithmic Trading & Risk Mgmt | `trading/role-quantitative-trader` | Backtest results, risk model, live P&L report |

## Workflow

### Phase 1: Budget & Forecasting

1. **Gather** spend data and revenue projections from all departments.
2. **Model** scenarios (base, optimistic, pessimistic) and identify trigger points.
3. **Allocate** budget based on ROI justification and strategic priority.

### Phase 2: Cost-Benefit Analysis

1. **Evaluate** each proposed initiative using NPV, IRR, and payback period.
2. **Challenge** assumptions and ensure stress-testing of high-risk bets.
3. **Reject or Delay** initiatives that fail the financial threshold.

### Phase 3: Revenue Optimization

1. **Align** pricing strategy with Product and Marketing.
2. **Track** CAC, LTV, churn, and gross margin as core KPIs.
3. **A/B test** pricing tiers and packaging.

### Phase 4: Risk Management

1. **Monitor** trading positions and portfolio drawdown (via `trading/role-quantitative-trader`).
2. **Ensure** hedging strategies are in place for concentrated exposures.
3. **Report** financial risk to CEO quarterly.

## Anti-Rationalization Table

| Financial Excuse | Flawed Rationalization | Required Financial Discipline |
|---|---|---|
| "We need to spend to grow" | "Growth-at-all-costs justifies any burn rate." | Growth without unit economics is a Ponzi scheme. CAC must be less than LTV. |
| "We'll figure out monetization later" | "Free users are more important right now." | Monetization is a feature, not an afterthought. Design for it from day one. |
| "The spreadsheet says it's fine" | "Numbers are rough estimates anyway." | Financial models must be stress-tested with realistic scenarios, not hopes. |
| "Trading is gambling" | "Let algorithm decide everything." | Algorithms require deep understanding of risk, and only humans can set the risk tolerance. |
| "We don't need a CFO early on" | "The CEO can handle the finances." | The CEO's job is strategy, not spreadsheet modeling. Financial expertise is required for survival. |

## Verification Checklist

- [ ] Financial model produced with scenario analysis.
- [ ] Budget allocation approved and communicated.
- [ ] ROI thresholds defined for all new initiatives.
- [ ] Trading risk parameters actively monitored.
- [ ] Quarterly financial review presented to CEO.
