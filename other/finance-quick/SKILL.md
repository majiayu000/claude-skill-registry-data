---
name: finance-quick
description: 60-Second Financial Snapshot — fast assessment of financial health based on six core inputs (income, expenses, savings, debt, age, retirement goal). No subagents. Produces a compact terminal scorecard with savings rate, DTI ratio, emergency fund coverage, retirement on-track status, and top 3 priority actions in under 40 lines.
---

# /finance quick — 60-Second Financial Snapshot

**DISCLAIMER: For educational/informational purposes only. Not financial advice.**

## Purpose

Deliver a high-signal financial health scorecard in under 60 seconds without launching the full 5-agent analysis. Use this when the user wants a quick read on where they stand before committing to a deeper audit.

## When To Trigger

- User types `/finance quick`
- User asks "how am I doing financially?", "what's my financial health?", "quick check on my finances"
- User wants a baseline before deciding to run `/finance analyze`

## DO NOT Launch Subagents

This skill must complete in a single response after collecting inputs. No parallel agents. No external API calls. All math is done inline by Claude.

## Required Inputs

Ask the user for these six numbers in a single prompt. Accept rough estimates — precision is not required for a snapshot.

1. **Monthly take-home income** (after-tax dollars hitting their account)
2. **Monthly expenses** (rent/mortgage + utilities + food + transport + everything else)
3. **Total liquid savings** (checking + savings + brokerage cash, NOT retirement accounts)
4. **Total debt** (credit cards + student loans + auto + mortgage balance)
5. **Current age**
6. **Target retirement age**

If the user only provides partial data, compute what you can and flag missing fields in the output.

## Calculations

### 1. Savings Rate
```
savings_rate = (monthly_income - monthly_expenses) / monthly_income * 100
```
**Benchmarks:**
- 20%+ → Excellent
- 15-19% → Good
- 10-14% → Fair
- 5-9% → Weak
- <5% → Critical

### 2. Debt-to-Income Ratio (DTI)
```
monthly_debt_payments = estimate as ~2% of total_debt (rough proxy)
DTI = monthly_debt_payments / monthly_income * 100
```
**Benchmarks:**
- <15% → Excellent
- 15-28% → Healthy
- 28-36% → Manageable
- 36-43% → Stressed
- >43% → Critical

### 3. Emergency Fund Coverage
```
months_covered = total_savings / monthly_expenses
```
**Benchmarks:**
- 6+ months → Excellent
- 3-5.9 months → Good
- 1-2.9 months → Weak
- <1 month → Critical

### 4. Retirement On-Track Status
Use the rule-of-thumb multiplier of current annual income by age:
- Age 30 → 1x income saved
- Age 35 → 2x income
- Age 40 → 3x income
- Age 45 → 4x income
- Age 50 → 6x income
- Age 55 → 7x income
- Age 60 → 8x income
- Age 67 → 10x income

Compare user's actual retirement savings (if provided; otherwise assume liquid savings as a floor) to the age benchmark. Compute years until retirement = target_retirement_age - current_age.

### 5. Composite Quick Score (0-100)
```
quick_score = (savings_rate_score + dti_score + emergency_score + retirement_score) / 4
```
Each subscore is 0-100 based on the benchmarks above.

**Grade:**
- 85-100 → A
- 70-84 → B
- 55-69 → C
- 40-54 → D
- <40 → F

## Output Format

Keep output under 40 lines total. Use plain ASCII (no markdown tables for the terminal version, but include a compact table format).

```
================================================
  60-SECOND FINANCIAL SNAPSHOT
================================================

Financial Health: [Grade] ([score]/100)
Life Stage: [Early/Mid/Pre-Retirement/etc]

CORE METRICS
- Savings Rate:        [X]%   [Excellent/Good/Fair/Weak/Critical]
- Debt-to-Income:      [X]%   [status]
- Emergency Fund:      [X.X] months   [status]
- Retirement Track:    [On / Behind / Critically Behind]

TOP 3 PRIORITY ACTIONS
1. [Highest impact action — specific dollar amount + this week]
2. [Second priority — specific action]
3. [Third priority — specific action]

KEY NUMBER TO IMPROVE FIRST
[The single metric that will move the score most]

================================================
Run `/finance analyze` for full multi-agent analysis
DISCLAIMER: For educational/informational purposes
only. Not financial advice.
================================================
```

## Priority Action Logic

Rank actions by which metric is weakest:

- **If emergency fund < 1 month** → Top action: "Build emergency fund to $X (1 month minimum) before any other moves"
- **If DTI > 43%** → Top action: "Aggressive debt paydown — list highest APR debt first, target $X extra/month"
- **If savings rate < 5%** → Top action: "Audit top 3 expense categories — find $X cuttable this month"
- **If retirement critically behind** → Top action: "Open or increase retirement contribution by $X/month (target 15% of gross income)"
- **If high-interest debt exists (assume credit cards if total_debt > 0 and user has any reported)** → "Pay down highest-APR debt before incremental investing"

If all four metrics are healthy, surface optimization actions:
- "Increase retirement contribution to capture full employer match"
- "Shift emergency fund to high-yield savings (4-5% APY vs 0.01%)"
- "Diversify beyond cash — start dollar-cost averaging into index funds"

## Example Walkthrough

**User inputs:**
- Income: $7,500/mo
- Expenses: $6,200/mo
- Savings: $8,000
- Debt: $32,000 (mostly student loans)
- Age: 31
- Target retirement: 65

**Computed:**
- Savings rate: 17.3% → Good
- DTI: ~8.5% → Excellent
- Emergency fund: 1.29 months → Weak
- Retirement: 34 years to retirement, $8K saved, benchmark at 31 is ~$90K → Critically Behind

**Score:** (75 + 95 + 35 + 25) / 4 = 57.5 → C

**Top 3 actions:**
1. Build emergency fund from $8K to $18,600 (3 months) — redirect $1,000/mo for 11 months
2. Open Roth IRA, contribute $583/mo ($7,000/yr max) starting this month
3. Refinance/consolidate student loans if APR > 6% — could save $X/year

## Edge Cases

- **User provides no debt** → Skip DTI scoring, weight others equally
- **User is retired** → Replace retirement track with withdrawal sustainability (4% rule check)
- **User is under 25** → Use lower retirement benchmarks (0.5x at 25); emphasize starting now
- **User has very high income (>$300K/yr)** → Add note: tax-advantaged accounts may be capped; mention backdoor Roth, mega-backdoor, HSA
- **User declines to share numbers** → Offer 3 hypothetical scenarios (struggling / average / strong) and let them self-identify

## Hand-Off

End every snapshot with the line:
> Run `/finance analyze` for the full 5-agent deep dive, or `/finance debt` / `/finance retirement` for focused work.

## Tone

Direct. Quantitative. No hedging language like "you might consider." Say "do X this week" with specific dollar amounts. Acknowledge wins ("17% savings rate is above the US median") before flagging gaps.

**DISCLAIMER: For educational/informational purposes only. Not financial advice. Consult a licensed financial advisor, CPA, or tax professional before making major financial decisions.**
