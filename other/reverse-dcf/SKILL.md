---
name: reverse-dcf
description: Use this skill to infer growth, margin, and cash-flow expectations implied by the current market price. Trigger for reverse DCF, implied expectations, market-implied growth, valuation pressure tests, or requests asking whether the stock price already embeds too much optimism.
---

# Reverse DCF Skill

## Purpose

Infer what growth, margin, and cash flow assumptions are implied by the current market price.

## Trigger Examples

- "Run a reverse DCF for NVDA."
- "What growth does the current stock price imply?"
- "Are market expectations reasonable at this price?"
- "What FCF margin is embedded in the market cap?"

## Hard Rule

If this skill is selected by the valuation router, it must either:

1. Execute Reverse DCF, or
2. Explicitly block execution and list missing/stale inputs.

Never only state that Reverse DCF should be run.

## Required Inputs

Minimum FCF-growth mode:

- Market cap or share price plus shares outstanding
- Net debt or cash / debt bridge
- Base FCF or normalized FCF
- Forecast period
- Discount rate
- Terminal growth
- Source dates for market and financial inputs

Revenue-to-FCF mode may replace base FCF with revenue and target FCF margin.

## Inputs

- Current share price
- Shares outstanding
- Market cap
- Cash and marketable securities
- Total debt
- Net debt
- Base FCF or base revenue
- Current / normalized FCF margin
- Forecast period
- Discount rate
- Terminal growth rate
- Data source dates

## Modes

### FCF Growth Reverse DCF

Use when base FCF is reliable.

### Revenue-to-FCF Reverse DCF

Use when FCF is temporarily depressed due to reinvestment.

### Scenario Reverse DCF

Use when the company has high uncertainty or multiple possible futures.

## Script Mapping

- Reverse DCF implementation: `scripts/valuation/valuation_reverse_dcf.py`
- Unified executor: `scripts/valuation/valuation_executor.py`
- Execution gate policy: `references/valuation_rules/reverse_dcf_execution_policy.md`

## Minimal Output Contract

Show only market-implied assumptions, reasonableness, source freshness, and blockers. Do not show formulas, spreadsheet rows, or solver traces unless explicitly requested.

## Output

```text
Reverse DCF Result:
- Market-implied EV:
- Base metric:
- Forecast period:
- Discount rate:
- Terminal growth:
- Implied growth:
- Implied FCF margin:
- Reasonableness:
```

## Blocking Output

```text
Reverse DCF Blocked:
- Missing data:
- Stale data:
- Required next data:
- Effect on investment conclusion:
```
