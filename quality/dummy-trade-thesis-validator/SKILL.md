---
name: trade-thesis-validator
description: Review daily trade journal entries for thesis completeness. Use when a trader submits a journal entry and needs validation that the thesis meets the minimum standard for entry.
license: MIT
---

# Trade Thesis Validator

Reviews trade journal entries and validates each thesis against minimum entry standards.

## A valid thesis must include

1. **Strategy tag** — `[MR]` (Mean Reversion) or `[MOM]` (Momentum) clearly stated
2. **At least one indicator value** — a specific number for RSI, SMA_20, SMA_50, distance to 52w high/low, or volume trend
3. **A directional rationale** — why the setup justifies entry at this time

## Output format

```
Entry: <ticker>
Result: VALID | NEEDS_REVISION
Reason: <one line — either "Meets minimum standards" or the specific gap>
```

## Rules

- Flag NEEDS_REVISION if any of the three required elements is absent
- NEEDS_REVISION reason must name the specific missing element — not just "incomplete thesis"
- Do not flag NEEDS_REVISION for style or formatting preferences — only for missing required elements
- If the thesis contains a strategy tag but no indicator value, that is a NEEDS_REVISION — "no indicator value cited"
