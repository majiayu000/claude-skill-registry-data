---
name: saas-valuation-compression
description: >
  Analyze how a private SaaS company's ARR valuation multiple changed across funding
  rounds, and attribute the compression or expansion to rate cycles and macro
  selloffs, growth deceleration, narrative shifts (including an AI premium),
  competition, and investor demand, benchmarked against private-market medians and
  peers. Use this skill whenever the user asks about valuation compression, ARR
  multiples, round-to-round valuation or multiple changes, down rounds, or wants to
  compare a VC-backed software company's funding rounds. Research the rounds rather
  than answering from memory.
---

# SaaS Valuation Compression Analyzer

## What This Skill Does

For a given SaaS company, research its funding history and compute ARR-based valuation
multiples at each round. Then explain the compression (or expansion) using a structured
framework that covers macro rates, growth trajectory, narrative shifts, and comparables.

Render the output as an inline visualization (using the Visualizer tool) plus a concise
prose explanation, rather than a wall of numbers.

---

## Workflow

### 1. Gather Data via Web Search

Research these, running independent searches in parallel:

- **Each funding round of the target company** — round name, date, amount raised, post-money valuation, and lead investor.
- **ARR at or near each round date** — from press coverage, founder interviews, or investor posts; note when a figure is estimated.
- **Growth and retention around each round** — ARR growth rate, NRR, churn, notable customers.
- **Narrative context** — AI positioning and product launches, category leadership, competitive moves.
- **Private-market SaaS multiples at each round date** — fall back on the dated tables in `references/benchmarks.md` when search is thin.

### 2. Build the Data Model

For each funding round, extract or estimate:

| Field | How to get it |
|---|---|
| Round name | Direct from search |
| Date | Direct from search |
| Amount raised | Direct from search |
| Post-money valuation | Direct or compute from ownership %; if unavailable, note as estimated |
| ARR at round date | Search explicitly; if not found, estimate from customer count x ARPC or interpolate |
| ARR multiple | `valuation / ARR` |
| Lead investor | Direct |

**ARR estimation heuristics (when not public):**
- Seed/Series A: ARR often $500K–$3M
- Series B: typically $5M–$20M
- Series C: typically $20M–$60M
- Cross-check against customer count x average deal size if available

### 3. Compute Compression Metrics

For each consecutive round pair (e.g., B → C):

```
multiple_compression_pct = (later_multiple - earlier_multiple) / earlier_multiple × 100
valuation_growth_pct = (later_val - earlier_val) / earlier_val × 100
arr_growth_pct = (later_arr - earlier_arr) / earlier_arr × 100
```

The three changes multiply rather than add: `valuation multiplier = ARR multiplier × multiple multiplier`, i.e. `(1 + valuation_growth) = (1 + arr_growth) × (1 + multiple_change)`. They are additive only in log terms, so use log changes wherever the decomposition needs to sum (for example, stacked bars). If ARR grows faster than the multiple compresses, absolute valuation still rises.

### 4. Attribute Compression to Causes

Use this checklist. For each cause, rate it: Primary / Contributing / Not applicable. `references/benchmarks.md` has dated private-market median multiples by period, public-software drawdowns, and known round-pair comparables for context.

**Macro / Rate Environment**
- Was the earlier round priced during the 2020–2021 ZIRP bubble? (typically a ~2–5x artificial premium)
- Was the later round priced during the 2022–2023 rate hikes? (removes the bubble premium)
- Was the later round priced during or just after a sector-wide public-software selloff, such as the April 2026 meltdown? Private marks typically lag public ones by 1–2 quarters.
- How does each round's multiple compare with the private-market median for its date?

**Growth Deceleration**
- Did YoY ARR growth rate slow materially between rounds? (most common cause)
- Did NRR/net retention drop?

**Narrative Shift**
- Did the company lose a major product story (e.g., lost PLG thesis, missed category leadership)?
- Did competitors emerge or incumbents catch up?

**AI Premium (positive or negative)**
- Does the company serve AI-native companies (OpenAI, Anthropic, etc.) as customers? → premium
- Did the company pivot to AI narrative credibly? → premium
- Did the company fail to articulate AI story? → discount vs peers
- In a macro-driven selloff an AI premium may be necessary but not sufficient — the April 2026 drawdowns in `references/benchmarks.md` show strong AI names falling with the sector.

**Competitive / Market**
- Market saturation signal (e.g., Okta pressure on WorkOS, Auth0 competition)
- Customer concentration risk revealed

**Investor Supply / Demand**
- Was the later round smaller and more selective? → price discipline
- New tier of lead investor (e.g., Tier 1 growth fund vs seed fund)? → may signal higher or lower conviction

### 5. Build the Visualization

Use the Visualizer tool to render:

1. **Metric cards row** — valuation at each round, ARR at each round, multiple at each round, compression %
2. **Line chart** — ARR multiple over time for the company vs macro SaaS median
3. **Bar chart** — valuation growth vs ARR growth vs multiple change (decomposition, in log terms so the parts add up)
4. **Comparison bar** — company compression vs 2–3 peer comparables (Vercel, Netlify, Fastly, or sector peers)
5. **Cause attribution table** inline in prose (Primary / Contributing / N/A per factor)

See design guidance: use teal for positive/growth, coral for compression/negative, gray for macro baseline, blue for valuation figures. Follow the CSS variable system throughout.

### 6. Write the Prose Summary

Cover, in order:
1. **Verdict** — one sentence, e.g., "The multiple compressed 36% but ARR grew 5x, so absolute valuation still rose about 3.2x."
2. **Primary cause** — the #1 factor explaining compression
3. **Narrative premium/discount** — AI story, category leadership, or lack thereof
4. **Comparable context** — how this company's compression compares to peers
5. **Forward implication** — what would need to be true for the multiple to expand at the next round

---

## Output Format

Put the inline visualization first, followed by the prose summary. Flag your data confidence when ARR had to be estimated.

---

## Edge Cases

- **Down round**: Multiple and absolute valuation both dropped. Note dilution implications.
- **No public ARR**: Use customer count x estimated ARPC, and label as estimate with +/- range.
- **Single round only**: Compute multiple vs sector median for that date; can't do compression analysis. Explain this.
- **Pre-revenue**: Use forward ARR or GMV multiple if applicable; note the different basis.
- **Acqui-hire / strategic acquisition**: Acquisition price often reflects strategic premium or distress, not pure ARR multiple — flag this.

## Reference Files

- `references/benchmarks.md` — Dated private-market ARR multiples by period, April 2026 public SaaS drawdowns, and known round-pair comparables
