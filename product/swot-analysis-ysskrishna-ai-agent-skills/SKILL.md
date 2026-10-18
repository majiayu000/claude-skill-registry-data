---
name: swot-analysis
description: >
  Use for SWOT analysis, or when the user wants to assess where a team, product or company stands: "strengths and weaknesses", "should we enter this market?", "review our position", "competitor comparison". Turns findings into actions. Skip for detailed planning or pure market sizing.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.10.5"
---

# SWOT Analysis

Sort what you know into **S**trengths, **W**eaknesses, **O**pportunities and **T**hreats, then turn it into actions with TOWS. A SWOT is only useful when each cell holds evidence and the result changes a decision.

## When to use

- Assessing the position of a product, team, project, company or competitor.
- A go / no-go on a market, partnership, or new initiative where internal fit and external conditions both matter.
- Preparing a strategy review or a planning session.

Skip: detailed implementation plans, market sizing, or choosing between concrete options on weighted criteria.

## Before you start

1. State in one block: **Subject** (one entity), **Scope and horizon** (for example "our API product, next 12 months"), **Decision it informs**, and **Pass** (Gather, SWOT, Prioritize, TOWS, Next steps).
2. **Gather first.** Read docs, metrics, customer feedback, competitor pages and the codebase where relevant. Every item needs a source or the label `[user stated]` or `[assumed]`. Ask up to 3 questions only for what tools cannot answer.
3. **Light path.** Small ask: 3 items per cell, top 2 per cell kept, 1 action per TOWS pair.

## Steps

### 1. SWOT
Place each item by one test:
- **Internal and within your control:** Strength or Weakness.
- **External and outside your control:** Opportunity or Threat.

Make items specific and comparative ("support answers in under 1 hour, competitors take a day" beats "great support").

| | Helpful | Harmful |
|---|---------|---------|
| **Internal** | Strengths | Weaknesses |
| **External** | Opportunities | Threats |

### 2. Prioritize
Keep the 2-4 items per cell that most affect the decision. Say why the rest are dropped.

### 3. TOWS
Pair cells to make actions:
- **SO:** use strengths to take opportunities.
- **WO:** fix weaknesses that block opportunities.
- **ST:** use strengths to reduce threats.
- **WT:** limit exposure where a weakness meets a threat.

### 4. Next steps
Name the 2-3 actions with an owner (or "to be assigned"), and the one assumption to test first.

## Pitfalls

- Items with no evidence ("strong brand"). Add a source or mark `[assumed]`.
- Mixing internal and external: "competitor launched a feature" is a Threat, not a Weakness.
- Long lists with no ranking. A SWOT that does not prioritize does not help a decision.
- Stopping at the grid. Without TOWS or next steps it records opinions and decides nothing.
- Treating one item as both a Strength and an Opportunity. Pick the cell that matches the test.

Worked example: [references/example.md](references/example.md).

## Checklist

- [ ] Subject, scope, horizon and the decision stated
- [ ] Each item sits in the right cell by the internal / external test
- [ ] Items are specific, comparative and sourced or labeled
- [ ] Priorities kept per cell
- [ ] TOWS actions and next steps with owners
