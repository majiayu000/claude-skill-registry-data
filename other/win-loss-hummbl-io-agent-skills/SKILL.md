---
name: win-loss
description: Analyze won and lost deals for patterns, competitor displacement, and improvement opportunities
version: 0.1.0
execution-mode: advisory
argument-hint: "[--period MONTHS] [--filter won|lost|all]"
category: sales-marketing
status: candidate
---
# Win/Loss Analysis

Analyze won and lost deals over a specified period to identify patterns in what works and what does not. Examines deal size, sales cycle length, competitor presence, objections encountered, and decision factors to inform strategy.

## When to Use
- During quarterly business reviews to assess pipeline effectiveness
- When win rate drops and you need to understand why
- When entering a new market segment and need baseline data
- When refining pricing, positioning, or competitive strategy

## Execution
1. Parse `$ARGUMENTS` for period (default: 6 months) and filter (default: all)
2. Pull deal data from CRM records and engagement tracker
3. Categorize deals by outcome (won, lost, stalled, disqualified)
4. For won deals: identify common success factors, average cycle length, deal size distribution
5. For lost deals: identify primary loss reasons, competitor displacement, common objections
6. Calculate win rate, average deal size, and cycle length trends
7. Generate actionable recommendations based on patterns

## Output Format
```
Win/Loss Analysis | <period>
==============================

## Summary
- Total deals: N (W won, L lost, S stalled)
- Win rate: X%
- Avg deal size: $X (won) / $Y (lost)
- Avg cycle: X days (won) / Y days (lost)

## Win Patterns
| Factor | Frequency | Impact |
|--------|-----------|--------|
| ... | N/W deals | HIGH/MED/LOW |

## Loss Patterns
| Reason | Frequency | Lost To |
|--------|-----------|---------|
| ... | N/L deals | <competitor or internal> |

## Competitive Displacement
| Competitor | Deals Lost | Common Objection |
|------------|-----------|-----------------|
| ... | N | ... |

## Recommendations
1. ...
2. ...

## Next Action
- ...
```

## Skill Chains
| After this skill... | Consider... |
|--------------------|-------------|
| Need CRM data first | `[crm]` to pull pipeline data |
| Competitor patterns emerge | `[competitive-intel]` for deeper analysis |
| Pricing issues identified | `[pricing-model]` to adjust (if available) |
| Results inform pitch strategy | `[pitch]` to refine messaging |
