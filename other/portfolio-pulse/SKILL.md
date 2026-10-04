---
name: portfolio-pulse
description: Snapshot of ALL products — one table, one recommendation. The "where should I focus today" command.
---

# /portfolio-pulse

Usage: `/portfolio-pulse`

## What this does
Reads all `products/*/product.config.json`, pulls telemetry, runs `agents/portfolio/portfolio-conductor/`, returns:

```
## Portfolio — <date>

### One sentence
Focus on <product> today, specifically <task>, because <reason>.

### Snapshot
| Product | Stage | MRR | 7d Δ | Errors 24h | Today's action |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

### Top 3 priorities
1. **<product>** — <task> (Xh) — why now
2. **<product>** — <task> (Xh) — why now
3. **<product>** — <task> (Xh) — why now

### On fire
- <product>: <issue>

### Don't touch today
- <product>: <reason>
```

## What you do as the assistant
1. Read all `products/*/product.config.json`. Skip products with `status: "killed"`.
2. Invoke telemetry-aggregator to populate the snapshot table.
3. Invoke portfolio-conductor for the prioritization.
4. Output the standardized format.
5. If user has indicated available time today (in a previous message), tune recommendations to that budget.

## Output discipline
- Table fits one screen
- Top 3 priorities, max
- On-fire list ideally empty
- Don't-touch list usually has 3-5 entries — that's the discipline working
