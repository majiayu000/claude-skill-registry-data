---
name: investor-action-framework
description: Use this skill to translate completed valuation and risk analysis into position-aware action zones, tranche plans, add/hold/trim/sell rules, and price triggers. Trigger when the user asks what to do with empty, partial, full, or overweight positions, cost basis, owned shares, sell levels, trim levels, or pre-committed action prices.
---

# Investor Action Framework Skill

## Purpose

Translate completed investment analysis into position-aware action guidance.

## Trigger Examples

- "I own UNH at 360. What sell levels should I use?"
- "What price should I add, hold, trim, or exit?"
- "Give me price zones for an empty / half / full position."
- "Using Jin Jiancheng, what should I pre-commit to?"

## Trigger Conditions

Activate after:

- A full stock analysis is completed
- Intrinsic value range is estimated
- Margin of safety is calculated
- Risk analysis is completed
- User asks what empty / half / full position investors should do
- User asks what price is suitable for entry, adding, trimming, or selling
- User provides cost basis, position size, owned shares, or target allocation

## Inputs

- Current price
- Intrinsic value low / mid / high
- Margin of safety
- Downside value
- Business quality rating
- Risk rating
- Investor position status
- Time horizon
- Max allocation guideline

## Required Inputs

Minimum usable action framework:

- Current price
- Bear / Base / Bull intrinsic value range or explicit valuation blocker
- Downside value or downside case
- Risk rating or key thesis-break risks
- Investor position status, cost basis, or stated position context when available

If position context is incomplete, still provide generic empty / half / full / overweight guidance and flag missing context.

## Hard Rule

This module must not be executed before valuation and risk analysis are complete.

If valuation range or current price is missing, output:

```text
Investor Action Framework Blocked
```

## Script Mapping

- Action framework reference: `references/action_policy/investor_action_framework.md`
- Scoring / price-zone helper: `scripts/scoring/investor_action_framework.py`
- Jin Jiancheng action lens: `references/masters/jin_jiancheng.md`

## Minimal Output Contract

Return price zones, position-aware suggestions, tranche plan, trim/sell framework, and thesis-change triggers. Use conditional language; never tell the user they must buy or sell.

## Output

1. Price zone table
2. Empty-position investor suggestion
3. Half-position investor suggestion
4. Full-position investor suggestion
5. Overweight investor suggestion
6. Tranche-based entry plan
7. Trim / sell framework
8. Conditions that would change the view

## Language Rule

Use conditional decision language, not absolute personalized financial advice.
