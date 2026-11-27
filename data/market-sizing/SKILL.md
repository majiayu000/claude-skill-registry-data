---
name: market-sizing
description: "Calculates Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) using both top-down and bottom-up methods, triangulates the results, and documents every assumption with its source. Use when sizing a market for a new product business case; evaluating expansion into a new segment or geography; preparing an investor or board presentation; or pressure-testing a market size someone else produced."
---

# Market Sizing

> Two independent methods, one triangulated answer, and every assumption on the page.

## What this skill is

A workflow for estimating Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) with a dual methodology. A top-down estimate narrows an industry total to the relevant segment; a bottom-up estimate multiplies out from customer counts and unit economics. Comparing the two exposes weak assumptions, and an assumption log makes the result defensible under questioning.

## What it solves

- A single headline market number pulled from one analyst report with no path to the company's segment
- TAM presented as if it were the revenue the company could capture
- Bottom-up and top-down numbers that disagree by an order of magnitude with no explanation
- Optimistic estimates that lose credibility with investors and boards
- Assumptions buried in a spreadsheet that nobody can audit or update
- Market boundaries that change between slides, so the numbers cannot be compared

## When to invoke

- Building the business case for a new product or product line
- Evaluating expansion into a new customer segment, use case, or geography
- Preparing an investor pitch, board memo, or annual plan that needs a market size
- Reviewing a market size produced by a team, consultant, or startup
- Deciding which of several segments to enter first

## Phase 1: Define market boundaries

A market size is only as good as its boundary. State each explicitly:

| Boundary | Decide | Example |
|----------|--------|---------|
| Geography | Global, regional, or country | North America only |
| Customer segment | Who buys | Mid-market companies with 100-1,000 employees |
| Use case | What job the product does | Automating vendor invoice approval |
| Buyer | Who holds the budget | Finance operations leader |
| Time frame | Which year the size applies to | 2027 |

Then define the three layers for this boundary:
- **TAM** - total annual spend on this job if every possible customer bought
- **SAM** - the part of TAM the product can serve with its current offering, channels, and geography
- **SOM** - the part of SAM the company can realistically win in a stated time frame

## Phase 2: Top-down analysis

Start from a published total and narrow it with explicit filters.

```
TAM = industry spend on the category
SAM = TAM x segment share x geography share x use-case share
SOM = SAM x achievable market share in the time frame
```

Sources: industry reports, public company filings, government statistics, trade association data. Record the report, year, and definition used, because category definitions differ between sources.

## Phase 3: Bottom-up analysis

Build from countable units.

```
TAM = number of potential customers x annual contract value
SAM = reachable customers x annual contract value
SOM = reachable customers x expected win rate x annual contract value
```

| Input | Source |
|-------|--------|
| Number of potential customers | Firmographic databases, census or registry data |
| Reachable share | Current channels and sales capacity |
| Annual contract value (deal size x purchase frequency) | Current pricing, pipeline, or comparable products |
| Win rate or adoption rate | Historical conversion or comparable benchmarks |

## Phase 4: Triangulate

Compare the two methods at each layer.

| Layer | Top-down | Bottom-up | Gap | Interpretation |
|-------|---------:|----------:|----:|----------------|
| TAM | $X | $Y | Z% | |
| SAM | $X | $Y | Z% | |
| SOM | $X | $Y | Z% | |

- **Within about 30%** - high confidence; report a range spanning both
- **Divergent** - investigate before reporting; usually a boundary mismatch, an inflated report, or an unrealistic price or adoption assumption
- Report the more conservative figure as the base case unless the gap is explained

## Phase 5: Document assumptions

Every number gets a source or an explicit assumption marker.

| # | Assumption | Value | Source or rationale | Confidence | Sensitivity |
|---|------------|-------|---------------------|------------|-------------|
| 1 | Potential customers | 42,000 | Registry data, 2026 | High | Medium |
| 2 | Win rate | 4% | Assumption: comparable product benchmarks | Low | High |

Flag the two or three assumptions that move SOM the most and show SOM at low and high values for each.

## Phase 6: Present the result

- Lead with SOM and SAM, not TAM; investors and boards discount TAM-led stories
- Show the funnel visually: TAM → SAM → SOM with the filter applied at each step
- State the time frame and boundary on the same slide as the numbers
- Be conservative: optimistic estimates lose credibility faster than conservative ones gain it

## Output

- Market boundary statement
- Top-down TAM, SAM, and SOM with sources
- Bottom-up TAM, SAM, and SOM with unit inputs
- Triangulation table with gap explanation
- Assumption log with sources, confidence, and sensitivity
- Summary range and recommended base case

## Operating rules

**Always**
- Define the boundary before calculating anything
- Run both top-down and bottom-up methods
- Give every number a source or an explicit assumption marker
- Explain any gap between methods before reporting
- Show the sensitivity of SOM to its biggest assumptions

**Never**
- Present TAM as achievable revenue
- Rely on a single analyst report without checking its category definition
- Mix boundaries or years across methods
- Hide assumptions inside formulas
- Round up to make the story more compelling
